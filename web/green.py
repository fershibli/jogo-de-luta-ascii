"""Cooperative threads for the browser, where real threads do not exist.

The old games start several threads with thread.start_new_thread() or
threading.Thread and let each one loop with time.sleep() and msvcrt.getch().
Before running the game, transform() rewrites every function that can block
(or that is started as a thread) into a generator: the blocking calls become
yields that tell the scheduler what the function is waiting for. The main
program keeps running as normal code; whenever it sleeps, busy-waits or
calls one of the rewritten functions, the scheduler runs the other
"threads" in the meantime, in the same order and at the same pace as the
originals did on Windows.
"""
import ast
import sys
import time
import traceback

_SLEEP = ('sleep',)
_KEY = ('getch', 'getche', 'getwch', 'getwche')
_THREAD_STARTERS = ('start_new_thread', 'start_new')
_IO = ('recv', 'recvfrom', 'accept')


# ---- source rewriting -----------------------------------------------------

def _call_name(call):
    f = call.func
    if isinstance(f, ast.Name):
        return None, f.id
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        return f.value.id, f.attr
    return None, None


def _blocking_kind(call):
    mod, name = _call_name(call)
    if name in _SLEEP and mod in ('time', None):
        return 'sleep'
    if name in _KEY and mod in ('msvcrt', None):
        return 'getch'
    if isinstance(call.func, ast.Attribute) and call.func.attr in _IO:
        return 'io'
    return None


def _thread_targets(tree):
    targets = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        _, name = _call_name(node)
        if name in _THREAD_STARTERS and node.args and isinstance(node.args[0], ast.Name):
            targets.add(node.args[0].id)
        if name == 'Thread':
            for kw in node.keywords:
                if kw.arg == 'target' and isinstance(kw.value, ast.Name):
                    targets.add(kw.value.id)
    return targets


def _own_nodes(fn):
    """Nodes of a function body, without descending into nested functions."""
    stack = list(fn.body)
    while stack:
        node = stack.pop()
        yield node
        for child in ast.iter_child_nodes(node):
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                stack.append(child)


def uses_threads(tree):
    return bool(_thread_targets(tree))


def _green_functions(tree):
    defs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    green = set(_thread_targets(tree)) & set(defs)
    for name, fn in defs.items():
        if any(isinstance(n, ast.Call) and _blocking_kind(n) for n in _own_nodes(fn)):
            green.add(name)
    changed = True
    while changed:
        changed = False
        for name, fn in defs.items():
            if name in green:
                continue
            for n in _own_nodes(fn):
                if isinstance(n, ast.Call) and _call_name(n)[0] is None and _call_name(n)[1] in green:
                    green.add(name)
                    changed = True
                    break
    return green


def _req(*parts):
    return ast.Tuple([ast.Constant(p) if not isinstance(p, ast.AST) else p for p in parts], ast.Load())


class _InGreen(ast.NodeTransformer):
    """Inside a generator function: blocking calls become yields."""

    def __init__(self, green, outer):
        self.green, self.outer = green, outer
        self.loop_depth = 0

    def visit_FunctionDef(self, node):
        return self.outer.visit_FunctionDef(node)  # nested functions are judged on their own

    def visit_Lambda(self, node):
        return node

    def visit_ClassDef(self, node):
        return self.outer.visit(node)

    def visit_Call(self, node):
        self.generic_visit(node)
        kind = _blocking_kind(node)
        if kind == 'sleep':
            return ast.copy_location(ast.Yield(_req('sleep', node.args[0] if node.args else ast.Constant(0))), node)
        if kind == 'getch':
            return ast.copy_location(ast.Yield(_req('getch', _call_name(node)[1])), node)
        mod, name = _call_name(node)
        if isinstance(node.func, ast.Attribute) and node.func.attr in _IO:
            args = ast.Tuple(list(node.args), ast.Load())
            req = _req('io', node.func.value, node.func.attr, args)
            return ast.copy_location(ast.Yield(req), node)
        if mod == 'os' and name == 'system' and node.args:
            return ast.copy_location(ast.Yield(_req('system', node.args[0])), node)
        if mod is None and name in self.green:
            return ast.copy_location(ast.YieldFrom(node), node)
        return node

    def _loop(self, node):
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            # a real thread can spin in a loop that only waits now and then;
            # here every turn of an outer loop has to give the others a chance
            node.body.insert(0, ast.Expr(ast.Yield(_req('tick'))))
        return node

    visit_While = visit_For = _loop


class _InMain(ast.NodeTransformer):
    """Outside the generators: calls to them run them to the end, and busy
    waits let the other threads work."""

    def __init__(self, green):
        self.green = green

    def visit_FunctionDef(self, node):
        if node.name in self.green:
            node.body = [_InGreen(self.green, self).visit(s) for s in node.body]
            if not any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in _own_nodes(node)):
                node.body.append(ast.If(ast.Constant(False), [ast.Expr(ast.Yield(None))], []))
            return node
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        mod, name = _call_name(node)
        if mod is None and name in self.green:
            call = ast.Call(ast.Name('__green_join__', ast.Load()), [node], [])
            return ast.copy_location(call, node)
        return node

    def visit_While(self, node):
        self.generic_visit(node)
        busy = all(isinstance(s, ast.Pass) for s in node.body)
        tick = ast.Expr(ast.Call(ast.Name('__green_tick__', ast.Load()), [ast.Constant(busy)], []))
        node.body = [s for s in node.body if not (busy and isinstance(s, ast.Pass))] + [tick]
        return node


def transform(tree):
    green = _green_functions(tree)
    return _InMain(green).visit(tree), green


# ---- scheduler -------------------------------------------------------------

class _Thread:
    __slots__ = ('gen', 'wake', 'want', 'name', 'call')

    def __init__(self, gen, name):
        self.gen, self.wake, self.want, self.name, self.call = gen, 0.0, None, name, None


# A thread that redraws the whole screen in a loop ran as fast as the Windows
# console could print; a browser terminal would get thousands of frames a
# second, so clearing the screen is held to this rate.
FRAME = 1 / 30.0
_last_clear = [0.0]

_threads = []
_pollers = []        # called before every round (e.g. to read network messages)
_real_sleep = None   # set by install()
_wait_event = None   # wait_event(seconds): returns early on a key or network message
_keys = None         # the msvcrt functions


def _is_clear(cmd):
    return str(cmd).strip().lower() in ('cls', 'clear')


def _step(t, value=None):
    try:
        req = t.gen.send(value)
    except StopIteration:
        _threads.remove(t)
        return
    except SystemExit:
        raise
    except BaseException:
        _threads.remove(t)
        sys.stderr.write('Unhandled exception in thread started by %s\n' % t.name)
        traceback.print_exc()
        return
    now = time.monotonic()
    t.want, t.call, t.wake = None, None, now
    if req is None:
        pass
    elif req[0] == 'tick':
        t.wake = now + 0.001
    elif req[0] == 'sleep':
        t.wake = now + max(0.0, float(req[1]))
    elif req[0] == 'getch':
        t.want = ('getch', req[1])
    elif req[0] == 'io':
        t.want = req
    elif req[0] == 'system':
        t.call = req[1]
        if _is_clear(req[1]):
            t.wake = max(now, _last_clear[0] + FRAME)


def _ready(t):
    """(True, value) when what the thread waits for is there."""
    w = t.want
    if w[0] == 'getch':
        if _keys['kbhit']():
            return True, _keys[w[1]]()
        return False, None
    _, obj, method, args = w
    ready = getattr(obj, '_green_ready', None)
    if ready is None or ready(method):
        return True, getattr(obj, method)(*args)
    return False, None


_in_pump = [0]


def pace_clear():
    """The main program clears the screen: hold it to FRAME like the threads."""
    if not _threads or _in_pump[0]:
        return
    wait = _last_clear[0] + FRAME - time.monotonic()
    if wait > 0:
        sleep(wait)
    _last_clear[0] = time.monotonic()


def pump():
    """Runs every thread that is due once. True if any of them ran."""
    _in_pump[0] += 1
    try:
        return _pump()
    finally:
        _in_pump[0] -= 1


def _pump():
    for p in _pollers:
        p()
    ran = False
    now = time.monotonic()
    for t in list(_threads):
        if t not in _threads:
            continue
        if t.want:
            try:
                ok, value = _ready(t)
            except Exception as e:  # the call itself failed: raise it in the thread
                ok, value = True, None
                try:
                    t.gen.throw(e)
                except StopIteration:
                    _threads.remove(t)
                continue
            if ok:
                _step(t, value)
                ran = True
        elif t.wake <= now:
            result = None
            if t.call is not None:
                cmd, t.call = t.call, None
                if _is_clear(cmd):
                    _last_clear[0] = time.monotonic()
                import os
                result = os.system(cmd)
            _step(t, result)
            ran = True
    return ran


def _idle(limit):
    """Nothing is due: wait for the next wake-up, a key, a message, or `limit` seconds."""
    now = time.monotonic()
    wakes = [t.wake for t in _threads if not t.want]
    delay = min([limit] + [w - now for w in wakes])
    if delay > 0:
        _wait_event(delay)


def block_until(pred, timeout=None):
    """Main program waits for something; the threads keep running meanwhile."""
    end = None if timeout is None else time.monotonic() + timeout
    while True:
        for p in _pollers:
            p()
        if pred():
            return True
        if not pump():
            left = 0.05 if end is None else min(0.05, end - time.monotonic())
            if left <= 0:
                return False
            _idle(left)
        elif end is not None and time.monotonic() >= end:
            return pred()


def sleep(seconds):
    if not _threads:
        return _real_sleep(seconds)
    end = time.monotonic() + max(0.0, float(seconds))
    while True:
        pump()
        left = end - time.monotonic()
        if left <= 0:
            return
        _idle(left)


def tick(busy=False):
    if _threads and not pump() and busy:
        _idle(0.05)


def join(gen):
    """Main program calls a rewritten function: run it (with the others) to the end."""
    if not hasattr(gen, 'send'):
        return gen
    result = []

    def runner():
        result.append((yield from gen))

    t = _Thread(runner(), getattr(gen, '__name__', 'call'))
    _threads.append(t)
    _step(t)
    while t in _threads:
        if not pump():
            _idle(0.05)
    return result[0] if result else None


def spawn(fn, args=(), kwargs=None):
    out = fn(*args, **(kwargs or {}))
    if hasattr(out, 'send'):
        t = _Thread(out, getattr(fn, '__name__', repr(fn)))
        _threads.append(t)
        _step(t)
    return len(_threads)


def install(real_sleep, wait_event, keys, builtins):
    global _real_sleep, _wait_event, _keys
    _real_sleep, _wait_event, _keys = real_sleep, wait_event, keys
    builtins.__green_join__ = join
    builtins.__green_tick__ = tick

    import _thread
    import threading
    _thread.start_new_thread = _thread.start_new = lambda f, a=(), k=None: spawn(f, a, k)

    def _start(self):
        if getattr(self, '_target', None):
            spawn(self._target, self._args, self._kwargs)
        else:
            spawn(self.run)

    threading.Thread.start = _start
    threading.Thread.join = lambda self, timeout=None: None
    sys.modules['thread'] = _thread
