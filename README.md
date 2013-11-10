# Absurdo - ASCII fighting game

A two-player fighting game drawn entirely in ASCII art in the Windows console: a court-like arena, life bars for P1 and P2, attacks and blocks read straight from the keyboard. Later it got a **networked version over UDP**, so two friends could fight from different PCs.

## History

- **Oct 2013**: `teste_luta` prototypes, then the "absurdo" rewrite (v2 to v10) with the arena layout from `ascii_art_luta.txt`.
- **Nov 2013**: `absurdo_rede.py`, peer-to-peer UDP version (one player connects, the other waits).
- `experiments/` keeps the small tests used to learn non-blocking input (`msvcrt`) and threads.

## Author

Fernando Luiz Neme Chibli ([@fershibli](https://github.com/fershibli))

## Releases

Builds are made by GitHub Actions (`.github/workflows/release.yml`) for Windows only. Push a tag such as `v1.0` (or run the workflow by hand) and the zipped builds are attached to a GitHub release.

The game reads the keyboard with `msvcrt`, which only exists on Windows, so there are no macOS or Linux builds.

To play from source: `python2.7 absurdo.py`.

Network mode: `python2.7 absurdo_rede.py` on both PCs (UDP port 20134).
