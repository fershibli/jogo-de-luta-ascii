"""msvcrt for the browser terminal: getch() blocks for a key, kbhit() polls."""
import webrt

_ARROWS = {'\x1b[A': 'H', '\x1b[B': 'P', '\x1b[C': 'M', '\x1b[D': 'K'}
_queue = []


def getch():
    if _queue:
        return _queue.pop(0)
    k = webrt.readkey()
    if k in _ARROWS:
        _queue.append(_ARROWS[k])
        return '\xe0'
    if k == '\x7f':
        return '\b'
    if k == '\n':
        return '\r'
    return k[0] if k else ''


def getche():
    c = getch()
    webrt.sys.stdout.write(c)
    return c


def kbhit():
    return bool(_queue) or webrt.keys_waiting()


getwch, getwche = getch, getche
