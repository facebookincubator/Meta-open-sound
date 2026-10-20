# Meta Open Sound — Free Instrument Samples and Sound Effects

Free, royalty-free instrument samples and sound effects from Meta's Creative
Audio team. Download multi-sampled piano, nylon guitar, and steel guitar, plus
289 game and VR sound effects, as WAV or OGG. Use them in games, apps, web
audio, films, DAW instruments, prototypes, or machine learning.

The instruments are public domain under [CC0 1.0 Universal](LICENSE): use them
commercially, change them, and redistribute them, and you don't need to credit
anyone. The Oculus Audio Pack is [CC BY 4.0](corpora/oculus-audio-pack/LICENSE):
just as free to use, but you must credit it. See [License](#license).

Each instrument comes with a design specification covering note mapping,
velocity layers, and playback guidance. The spec doesn't assume an engine, so
you can build a working sampler in any engine or framework. Each instrument
also ships an SFZ map that loads directly in SFZ samplers such as sfizz and
Sforzando.

> **AI agents:** start with [AGENTS.md](AGENTS.md). It covers how to find a sample,
> read its design spec, and download the audio.

## Collections

| Collection | Samples | License | Description |
| --- | --- | --- | --- |
| [Meta Piano](systems/instruments/meta-piano/README.md) | 352 | CC0 | Full 88-key upright piano (A0–C8), 4 velocity layers. Warm, full character with medium sustain. |
| [Meta Nylon Guitar](systems/instruments/meta-nylon-guitar/README.md) | 348 | CC0 | Nylon-string classical guitar (E2–B5), six string zones, 3 dynamic layers (two picked, one fingerstyle). |
| [Meta Steel Guitar](systems/instruments/meta-steel-guitar/README.md) | 375 | CC0 | Steel-string acoustic guitar (E2–C6), six strings chromatic, 3 velocity layers. |
| [Oculus Audio Pack 1](corpora/oculus-audio-pack/README.md) | 508 | CC BY 4.0 | 289 game and VR sound effects: footsteps on six surfaces, themed UI sets, character vocals, doors, ambience loops, musical stings, horror and interaction foley. Searchable by description. |

## Common uses

- **Piano sounds for a web game or app.** Use the OGG previews from Meta Piano
  and load them with the Web Audio API. [AGENTS.md](AGENTS.md#playing-a-sample-on-the-web)
  has a working snippet.
- **A free piano or guitar sample library for a DAW or plugin.** Download the
  24-bit / 48 kHz WAV ZIP from [Releases](../../releases) and map it with the
  collection's design spec.
- **Sound effects for a game or VR app.** Search the Oculus Audio Pack's
  `index/` by description, copy the OGGs you need, and add its credit line to
  your credits.
- **Training data or audio research.** The CC0 collections' samples and
  metadata carry no license restrictions.

## File formats

| Format | Where | Details |
| --- | --- | --- |
| OGG Vorbis | In this repository, and as a ZIP on each [Release](../../releases) | Web-optimized previews — great for auditioning and lightweight playback. |
| WAV | Attached to each [Release](../../releases) | Source quality (24-bit / 48 kHz for the instruments), for production use. |
| SFZ | In each instrument directory and in both Release ZIPs | Sampler map: which sample plays for each note and velocity. |

## Quick start

### Download a single preview

```bash
curl -sLO "https://github.com/facebookincubator/Meta-open-sound/raw/main/systems/instruments/meta-piano/ogg/INSPiano_Vel03_C4_01.ogg"
```

### Clone just the collection you want (sparse checkout)

```bash
git clone --filter=blob:none --sparse https://github.com/facebookincubator/Meta-open-sound.git
cd Meta-open-sound
git sparse-checkout set systems/instruments/meta-piano
```

### Get the full-quality WAV bundle

Download the WAV ZIP from the [Releases](../../releases) page, or with the
GitHub CLI. It includes the SFZ map, so you can load it in a sampler as-is:

```bash
gh release download meta-piano-v1.0.0 \
  --repo facebookincubator/Meta-open-sound \
  --pattern "*.zip"
```

## Programmatic access

- [`catalog.json`](catalog.json) — an index of every collection (id, name,
  category, path, tags, license).
- Each collection's `manifest.json` lists its samples and specs. The `ogg_dir`
  field points at the in-repo OGG previews; full-quality WAVs are in the
  matching Release.
- Each instrument's `<id>.sfz` maps every sample to its keys and velocities.
- Each collection's `SHA256SUMS` lets you check a download with
  `sha256sum -c SHA256SUMS`.
- Each collection's `LICENSE` holds its license text, and its `manifest.json`
  carries the same `license` id.

## Naming convention

File names follow a UCS-aligned convention, e.g. `INSPiano_Vel03_C4_01.wav`
(Instruments / Piano, velocity layer 3, note C4, variation 01). See
[`docs/naming-convention.md`](docs/naming-convention.md) for the full reference.

## FAQ

**Can I use these sounds commercially?** Yes. Every collection allows
commercial use, modification, and redistribution. CC0 collections are in the
public domain.

**Do I have to credit Meta?** Not for a CC0 collection; credit is appreciated
but not required. A collection under a license that requires credit (such as
CC BY 4.0) has an `ATTRIBUTION.md` with the exact line to use.

**Are more collections coming?** Yes. Watch the repository or see
[CHANGELOG.md](CHANGELOG.md).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). By
contributing you agree that your submissions are released under CC0. Please also
review our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Each collection is licensed separately. Its directory has a `LICENSE` with the
full terms, its `catalog.json` entry and `manifest.json` carry the `license`
id, and a collection that requires credit also has an `ATTRIBUTION.md`. The instruments
are CC0; the Oculus Audio Pack is CC BY 4.0.

Everything else in this repository is released under
[CC0 1.0 Universal](LICENSE). To the extent possible under law, Meta Platforms,
Inc. has waived all copyright and related or neighboring rights to it, and to
every collection marked CC0.
