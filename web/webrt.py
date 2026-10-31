"""Browser runtime for the old Windows-console games (Pyodide + xterm.js).

Keeps the original code untouched in behaviour: Python 2 integer division,
blocking input(), msvcrt.getch(), time.sleep(), Windows console commands
(cls, color, pause) and Windows-style, case-insensitive file paths.
"""
import ast
import builtins
import io
import os
import pickle
import sys
import time
import warnings

import webterm

warnings.filterwarnings('ignore', category=SyntaxWarning)

_ANSI = {'0': 0, '1': 4, '2': 2, '3': 6, '4': 1, '5': 5, '6': 3, '7': 7,
         '8': 60, '9': 64, 'a': 62, 'b': 66, 'c': 61, 'd': 65, 'e': 63, 'f': 67}


class _Out(io.TextIOBase):
    encoding = 'utf-8'

    def write(self, s):
        s = str(s)
        if s:
            webterm.write(s)
        return len(s)

    def isatty(self):
        return True


sys.stdout = sys.stderr = _Out()

# ---- keyboard -------------------------------------------------------------

_pending = []


def readkey(timeout=-1):
    """One key as text; arrows and other escape sequences are returned whole."""
    if _pending:
        return _pending.pop(0)
    b = webterm.readbyte(timeout)
    if b < 0:
        return None
    if b == 27:
        seq = b'\x1b'
        while webterm.avail() > 0 or len(seq) == 1:
            nb = webterm.readbyte(15)
            if nb < 0:
                break
            seq += bytes([nb])
            if len(seq) > 2 and 64 <= nb <= 126:
                break
        return seq.decode('latin-1')
    raw = bytes([b])
    if b >= 0xC0:
        need = 1 if b < 0xE0 else 2 if b < 0xF0 else 3
        for _ in range(need):
            nb = webterm.readbyte(50)
            if nb >= 0:
                raw += bytes([nb])
    return raw.decode('utf-8', 'replace')


def keys_waiting():
    return bool(_pending) or webterm.avail() > 0


def _input(prompt=''):
    sys.stdout.write(str(prompt))
    buf = ''
    while True:
        k = readkey()
        if k in ('\r', '\n'):
            sys.stdout.write('\r\n')
            return buf
        if k in ('\x7f', '\b'):
            if buf:
                buf = buf[:-1]
                sys.stdout.write('\b \b')
        elif k == '\x03':
            raise KeyboardInterrupt
        elif k and not k.startswith('\x1b') and k >= ' ':
            buf += k
            sys.stdout.write(k)


builtins.input = _input
builtins.raw_input = _input

# ---- time, console commands ----------------------------------------------

time.sleep = lambda s: webterm.sleep(int(max(0, s) * 1000))


_pace_clear = None


def _system(cmd):
    c = str(cmd).strip()
    low = c.lower()
    if low in ('cls', 'clear'):
        if _pace_clear:
            _pace_clear()
        sys.stdout.write('\x1b[2J\x1b[3J\x1b[H')
    elif low.startswith('color'):
        arg = (c[5:].strip() + '07')[:2].lower()
        bg, fg = _ANSI.get(arg[0], 0), _ANSI.get(arg[1], 7)
        sys.stdout.write('\x1b[%d;%dm\x1b[2J\x1b[H' % (40 + bg, 30 + fg))
    elif low.startswith('title'):
        webterm.title(c[5:].strip())
    elif low == 'pause':
        sys.stdout.write('Pressione qualquer tecla para continuar. . . ')
        readkey()
        sys.stdout.write('\r\n')
    return 0


os.system = _system

# ---- Windows-style paths --------------------------------------------------


_exists = os.path.exists


def _resolve(path):
    if not isinstance(path, str):
        return path
    p = path.replace('\\', '/')
    if _exists(p):
        return p
    parts = [x for x in p.split('/')]
    cur = '/' if p.startswith('/') else '.'
    out = []
    for part in parts:
        if part in ('', '.'):
            continue
        try:
            match = next((n for n in os.listdir(cur) if n.lower() == part.lower()), part)
        except OSError:
            match = part
        out.append(match)
        cur = os.path.join(cur, match)
    return ('/' if p.startswith('/') else '') + '/'.join(out)


_open = builtins.open
builtins.open = lambda f, *a, **k: _open(_resolve(f), *a, **k)
os.path.exists = lambda p: _exists(_resolve(p))

_pload, _ploads = pickle.load, pickle.loads
pickle.load = lambda f, **k: _pload(f, **{'encoding': 'latin1', **k})
pickle.loads = lambda s, **k: _ploads(s, **{'encoding': 'latin1', **k})

# ---- Python 2 division ----------------------------------------------------


def _py2div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a // b
    return a / b


builtins.__py2div__ = _py2div


class _Py2Division(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Div):
            call = ast.Call(ast.Name('__py2div__', ast.Load()), [node.left, node.right], [])
            return ast.copy_location(call, node)
        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Div):
            load = ast.parse(ast.unparse(node.target), mode='eval').body
            call = ast.Call(ast.Name('__py2div__', ast.Load()), [load, node.value], [])
            return ast.copy_location(ast.Assign([node.target], call), node)
        return node


def _use_green(green):
    import msvcrt
    real_sleep = time.sleep

    def wait_event(seconds):
        seq = webterm.evseq()
        if keys_waiting():
            return
        webterm.waitev(seq, int(seconds * 1000) + 1)

    keys = {n: getattr(msvcrt, n) for n in ('getch', 'getche', 'getwch', 'getwche', 'kbhit')}
    green.install(real_sleep, wait_event, keys, builtins)
    global _pace_clear
    _pace_clear = green.pace_clear
    time.sleep = green.sleep

    def blocking(fn):
        def wrapper():
            if green._threads:
                green.block_until(keys['kbhit'])
            return fn()
        return wrapper

    for n in ('getch', 'getche', 'getwch', 'getwche'):
        setattr(msvcrt, n, blocking(keys[n]))


def run(main):
    os.chdir('/game')
    sys.path.insert(0, '/game')
    src = _open(main, encoding='utf-8').read()
    tree = _Py2Division().visit(ast.parse(src, main))
    import green
    if 'socket' in src:
        import netsock
        sys.modules['socket'] = netsock
    if green.uses_threads(tree):
        tree, _ = green.transform(tree)
        _use_green(green)
    tree = ast.fix_missing_locations(tree)
    code = compile(tree, main, 'exec')
    g = {'__name__': '__main__', '__file__': main}
    try:
        exec(code, g)
    except SystemExit:
        pass
    sys.stdout.write('\x1b[0m\r\n\r\n[fim do jogo]\r\n')
