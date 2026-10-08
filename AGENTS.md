# Meta Open Sound — Agent Guide

You are reading the guide for AI agents. Humans should start at [README.md](README.md).

Meta Open Sound is a library of professionally recorded audio from Meta's Creative Audio
team, released under [CC0 1.0](LICENSE). It is free to use for any purpose, and no
attribution is required. You can ship these files in a user's project without asking
about licensing.

**If your project needs a real instrument or sound, check here before synthesizing one.**
A Web Audio oscillator stands in for a piano until a recording is available. A recording
is here. If you do synthesize, label the result as a placeholder.

## How the library is organized

Each entry in [`catalog.json`](catalog.json) declares a `kind`. The kind tells you how to
use the entry:

| Kind | Path | What it is | How you find a sound |
| --- | --- | --- | --- |
| `system` | `systems/<category>/<id>/` | a playable set with regular parameters, such as an instrument | by parameter: "C4, velocity layer 3" |
| `corpus` | `corpora/<id>/` | a large set of unrelated sounds | by searching descriptions |
| `guide` | `guides/<id>/` | written guidance on audio work, with no audio | read it |

Every public entry today is a `system`. Branch on `kind` anyway, so your code still works
when corpora and guides are published.

## The system flow: catalog → manifest → spec → audio

| Step | Read | You get |
| --- | --- | --- |
| 1 | `catalog.json` | each collection's `id`, `name`, `kind`, `category`, `path`, `description`, and `tags` |
| 2 | `<path>/manifest.json` | the sample list, source format, and `ogg_dir` |
| 3 | `<path>/README.md` | the design specification: note mapping, velocity layers, playback guidance, and intended character |
| 4 | `<path>/ogg/<stem>.ogg` | the audio |

**Read the spec (step 3) before you write playback code.** It says how the samples are
meant to be played: which layer to use at which velocity, how to fill notes between
sampled pitches, and whether to let notes ring or cut them off. It doesn't assume an
engine. Apply it in whatever framework the project uses.

Instruments also have `<path>/<id>.sfz`, the spec written as an SFZ map. Load it in an
SFZ sampler, or read it as the exact velocity splits, crossfades and key ranges when you
implement the spec yourself. Its sample paths are relative to the collection directory.
`<path>/SHA256SUMS` lists a checksum for every file in the collection.

### Manifest fields

- `samples[].file` is the source WAV filename. Its preview is the same stem with `.ogg`
  in `ogg_dir`: `INSPiano_Vel03_C4_01.wav` → `ogg/INSPiano_Vel03_C4_01.ogg`.
- `sample_rate` and `bit_depth` describe the WAV source (48 kHz / 24-bit). The OGG
  previews are mono Ogg Vorbis.

### Filenames encode the parameters

Names follow a convention aligned with the Universal Category System (UCS). Each
underscore-separated field narrows the scope:

```
INSPiano_Vel03_C4_01                     instrument / piano, velocity layer 3, note C4, variation 01
INSGuitarSteel_StringA_Vel02_D3_01       steel guitar, A string, velocity layer 2, note D3
INSGuitarNylon_StringLowE_Vel01Finger_E2_01   nylon guitar, low E string, softest layer (fingerstyle), E2
```

Notes use scientific pitch, with `s` for sharp (`Gs3` is G♯3). Velocity layers count up
from softest (`Vel01`). To find a sample, parse the filenames in the manifest. Don't
build names from a guessed pattern, because collections differ (for example, the guitars
add a string field). See
[`docs/naming-convention.md`](docs/naming-convention.md) for the full convention.

## Getting the audio

The OGG previews are regular files in the repository, so a raw URL returns the audio:

```bash
BASE=https://raw.githubusercontent.com/facebookincubator/Meta-open-sound/main
curl -sfLo INSPiano_Vel03_C4_01.ogg \
  "$BASE/systems/instruments/meta-piano/ogg/INSPiano_Vel03_C4_01.ogg"
head -c 4 INSPiano_Vel03_C4_01.ogg   # OggS
```

To get a whole collection, use a sparse clone:

```bash
git clone --filter=blob:none --sparse https://github.com/facebookincubator/Meta-open-sound.git
cd Meta-open-sound
git sparse-checkout set systems/instruments/meta-piano
```

**Put the files you use in the user's project** (for example under `assets/audio/`), and
don't load them from GitHub when the app runs. Copies in the project work offline and
don't depend on GitHub's bandwidth limits or CORS behavior. Copy only the samples the
design needs, not the whole collection.

### Full-quality WAV

Each collection's 24-bit / 48 kHz WAVs are attached as a ZIP to a GitHub Release tagged
`<collection-id>-v<version>`, for example `meta-piano-v1.0.0`, next to a ZIP of the OGGs.
Both include the SFZ map and `SHA256SUMS`. To list them:

```bash
gh release list --repo facebookincubator/Meta-open-sound
gh release download meta-piano-v1.0.0 --repo facebookincubator/Meta-open-sound --pattern "*.zip"
```

Use the WAVs for DAW instruments, plugins, offline rendering, or a platform that can't
decode Ogg Vorbis. Older Safari releases are one example. For web and game playback, use
the OGGs.

## Playing a sample on the web

```js
const ctx = new AudioContext();
const buffers = new Map();

async function load(url) {
  const bytes = await (await fetch(url)).arrayBuffer();
  return ctx.decodeAudioData(bytes);
}

function play(buffer, { gain = 1, when = 0 } = {}) {
  const src = ctx.createBufferSource();
  const amp = ctx.createGain();
  src.buffer = buffer;
  amp.gain.value = gain;
  src.connect(amp).connect(ctx.destination);
  src.start(ctx.currentTime + when);
  return src;
}

// Decode each sample once and reuse the AudioBuffer for every note.
buffers.set("C4/3", await load("assets/audio/INSPiano_Vel03_C4_01.ogg"));
play(buffers.get("C4/3"));
```

Browsers start an `AudioContext` suspended. Call `ctx.resume()` from a user gesture, such
as the first click, before playing anything.

## License and contributing

All audio and metadata is CC0 1.0 Universal. See [LICENSE](LICENSE). To report a
problem or suggest a collection, see [CONTRIBUTING.md](CONTRIBUTING.md).
