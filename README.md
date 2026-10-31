# Absurdo - ASCII fighting game

A two-player fighting game drawn entirely in ASCII art in the Windows console: a court-like arena, life bars for P1 and P2, attacks and blocks read straight from the keyboard. Later it got a **networked version over UDP**, so two friends could fight from different PCs.

## History

- **Oct 2013**: `teste_luta` prototypes, then the "absurdo" rewrite (v2 to v10) with the arena layout from `ascii_art_luta.txt`.
- **Nov 2013**: `absurdo_rede.py`, peer-to-peer UDP version (one player connects, the other waits).
- `experiments/` keeps the small tests used to learn non-blocking input (`msvcrt`) and threads.

## Play in the browser

- vs. the computer: **[https://fershibli.github.io/jogo-de-luta-ascii/](https://fershibli.github.io/jogo-de-luta-ascii/)**
- two players online: **[https://fershibli.github.io/jogo-de-luta-ascii/rede.html](https://fershibli.github.io/jogo-de-luta-ascii/rede.html)**

The pages run `web/game/absurdo.py` and `web/game/absurdo_rede.py` (Python 3 copies) on Pyodide inside an xterm.js terminal. The browser has no threads, so `web/green.py` rewrites each thread function into a generator before running it: `time.sleep`, `msvcrt.getch` and `recvfrom` become yields, and a small scheduler runs the seven "threads" at the pace of the original sleeps (screen redraws are held to 30 per second). The UDP sockets are replaced by `web/netsock.py`, which sends the same messages over a WebRTC data channel (PeerJS); the "IP" the game shows and asks for is a room number. Published by `.github/workflows/pages.yml`.

## Author

Fernando Luiz Neme Chibli ([@fershibli](https://github.com/fershibli))

## Releases

Builds are made by GitHub Actions (`.github/workflows/release.yml`) for Windows only. Push a tag such as `v1.0` (or run the workflow by hand) and the zipped builds are attached to a GitHub release.

The game reads the keyboard with `msvcrt`, which only exists on Windows, so there are no macOS or Linux builds.

To play from source: `python2.7 absurdo.py`.

Network mode: `python2.7 absurdo_rede.py` on both PCs (UDP port 20134).
