"""socket module for the browser: the old games' UDP traffic travels over WebRTC.

A browser cannot open UDP sockets, so the page connects the players with
PeerJS data channels instead. Each player gets a short room number from the
signalling server, and that number takes the place of the IP address: the
games print "your IP" and ask for "your friend's IP" exactly as before, but
both are room numbers now. sendto()/recvfrom() keep their old meaning, with
the message text as the payload. The channel is reliable and ordered, so the
games' key-by-key lockstep does not drift the way it could over real UDP.
"""
import json
import time

import green
import webterm

AF_INET, AF_INET6 = 2, 10
SOCK_STREAM, SOCK_DGRAM = 1, 2
SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST = 1, 2, 6
IPPROTO_UDP = 17
error = OSError
herror = gaierror = OSError
timeout = TimeoutError
_PORT = 20134

_inbox = []
_me = []


def _poll():
    while True:
        raw = webterm.netrecv()
        if not raw:
            return
        m = json.loads(raw)
        if m['t'] == 'pkt':
            _inbox.append((m['f'], m['d']))
        elif m['t'] == 'id':
            _me.append(m['code'])
        elif m['t'] == 'err':
            raise OSError(m.get('m', 'network error'))


green._pollers.append(_poll)


def _wait(pred, seconds=None):
    if green._wait_event is not None:
        return green.block_until(pred, seconds)
    end = None if seconds is None else time.monotonic() + seconds
    while not pred():
        _poll()
        if pred():
            break
        left = 0.05 if end is None else end - time.monotonic()
        if left <= 0:
            return False
        webterm.waitev(webterm.evseq(), int(min(left, 0.05) * 1000) + 1)
    return True


def _room():
    if not _me:
        webterm.netopen()
        _wait(lambda: bool(_me))
    return _me[0]


def gethostname():
    return 'sala'


def gethostbyname(name):
    return _room()


def gethostbyname_ex(name):
    return name, [], [_room()]


def _text(data):
    if isinstance(data, (bytes, bytearray)):
        return bytes(data).decode('latin-1')
    return str(data)


class socket:
    def __init__(self, family=AF_INET, type=SOCK_DGRAM, proto=0, *a):
        self._timeout = None
        self._peer = None
        self._last = (None, None, 0.0)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

    # setup calls the games make; nothing to do for a data channel
    def bind(self, addr):
        _room()

    def setsockopt(self, *a):
        pass

    def settimeout(self, value):
        self._timeout = value

    def setblocking(self, flag):
        self._timeout = None if flag else 0.0

    def gettimeout(self):
        return self._timeout

    def close(self):
        pass

    def listen(self, *a):
        _room()

    def connect(self, addr):
        self._peer = addr

    def getsockname(self):
        return (_room(), _PORT)

    def fileno(self):
        return -1

    # traffic
    def sendto(self, data, addr):
        _room()
        to, text = str(addr[0]).strip(), _text(data)
        now = time.monotonic()
        last_to, last_text, last_at = self._last
        # the games resend in tight loops while waiting for an answer; one
        # copy every few milliseconds is plenty
        if (to, text) == (last_to, last_text) and now - last_at < 0.02:
            return len(text)
        self._last = (to, text, now)
        webterm.netsend(to, text)
        return len(text)

    def send(self, data):
        return self.sendto(data, self._peer)

    sendall = send

    def _green_ready(self, method):
        _poll()
        return bool(_inbox) or self._timeout == 0.0

    def recvfrom(self, size=1024, *a):
        if not _inbox:
            if self._timeout == 0.0:
                _poll()
                if not _inbox:
                    raise BlockingIOError('no message')
            elif not _wait(lambda: bool(_inbox), self._timeout):
                raise timeout('timed out')
        sender, text = _inbox.pop(0)
        return text[:size], (sender, _PORT)

    def recv(self, size=1024, *a):
        return self.recvfrom(size)[0]
