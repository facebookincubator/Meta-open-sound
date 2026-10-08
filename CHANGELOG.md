# Changelog

All notable changes to Meta Open Sound are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

### Added

- **Meta Nylon Guitar** — nylon-string classical guitar (E2–B5), six string
  zones, 3 dynamic layers (two picked, one fingerstyle), 348 samples.
- **Meta Steel Guitar** — steel-string acoustic guitar (E2–C6), six strings
  chromatic, 3 velocity layers, 375 samples.
- An SFZ map for each instrument (`<id>.sfz`), ready to load in any SFZ sampler
  and readable as a reference for custom implementations.
- A `SHA256SUMS` file in each instrument directory.
- Each release now has an OGG ZIP alongside the WAV ZIP, both with the SFZ map
  and checksums.

### Changed

- OGG files are stored as regular Git files instead of Git LFS, so raw file
  URLs and "Download ZIP" return audio.

- Collections are now grouped by kind at the top level. `instruments/meta-piano/`
  becomes `systems/instruments/meta-piano/`, and published paths — including raw
  file URLs and sparse-checkout paths — move with it.
- The UCS v8.2.1 vocabulary referenced by the naming guide is now included in
  the repository.

### Fixed

- **Meta Piano** — three masters with audible defects, found by the new sample
  audit:
  - `INSPiano_Vel03_Gs5_01` and `INSPiano_Vel04_B4_01` started 67 ms and 33 ms
    late, so chords containing those notes sounded rolled. Both are trimmed to
    start with the other velocity layers of their key.
  - `INSPiano_Vel02_Gs7_01` was quieter than the softer `Vel01` layer. It is
    raised 8 dB.
- **Late attacks trimmed** in all three instruments: samples whose attack
  landed more than 20 ms after the instrument's typical attack time, from
  silence or pick/finger/damper noise before the note, so they sounded late
  or rolled in chords. Each is trimmed so its attack lands on that typical
  time (about 8 ms for the piano and nylon guitar, 25 ms for the steel
  guitar), with a 2 ms fade-in. Meta Piano: 5 samples. Meta Nylon Guitar: 22.
  Meta Steel Guitar: 52.

## meta-piano-v1.0.0

Initial public release.

### Added

- **Meta Piano** — full 88-key upright piano (A0–C8), 4 velocity layers, 352
  samples. Warm, full character with medium sustain.
  - OGG Vorbis previews included in-repo via Git LFS.
  - 24-bit / 48 kHz WAV bundle attached to the `meta-piano-v1.0.0` release.
- Repository scaffolding: `README`, `LICENSE` (CC0 1.0 Universal),
  `CONTRIBUTING`, `CODE_OF_CONDUCT`, and the `docs/naming-convention.md`
  reference.
