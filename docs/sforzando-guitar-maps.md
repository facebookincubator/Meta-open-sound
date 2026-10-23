# Guitar SFZ maps in sforzando

For keyboard playing, load `meta-nylon-guitar-sforzando.sfz` or
`meta-steel-guitar-sforzando.sfz` from the corresponding collection directory.
Each file contains the reference map's first-position keyboard regions, without
the overlapping full-string channel maps. It accepts any MIDI channel.

The existing `<collection-id>.sfz` remains the reference map: channel 1 is the
keyboard layout, and channels 2–7 select Low E, A, D, G, B and High E individually
in samplers that enforce `lochan`/`hichan`. In sforzando/ARIA 1.982 on macOS
Apple Silicon, those restrictions did not isolate the guitar regions: a single
middle-C note triggered several string recordings of that same pitch. This is
an observed sampler compatibility problem; other engines have not been tested.

## Keyboard and individual strings

| Map | Nylon MIDI range | Steel MIDI range |
| --- | --- | --- |
| Keyboard (`<collection-id>-sforzando.sfz`) | 40–83 (E2–B5) | 40–84 (E2–C6) |
| `string-maps/<collection-id>-StringLowE.sfz` | 40–59 | 40–60 |
| `string-maps/<collection-id>-StringA.sfz` | 45–63 | 45–65 |
| `string-maps/<collection-id>-StringD.sfz` | 50–68 | 50–70 |
| `string-maps/<collection-id>-StringG.sfz` | 55–73 | 55–75 |
| `string-maps/<collection-id>-StringB.sfz` | 59–77 | 59–79 |
| `string-maps/<collection-id>-StringHighE.sfz` | 64–83 | 64–84 |

Load one string map on each sampler instance or track when a part chooses its
strings explicitly. Route each track's MIDI in the host. All recordings remain
available through these maps. The Steel Low E map retains the reference's B2
fallback: MIDI 47 uses the A#2 recording shifted up one semitone. The keyboard
map uses the recorded A-string B2 instead.

Nylon retains its original keyswitches: MIDI 24 Auto (default), 25 Finger, and
26 Pick. Auto and Pick retain their velocity crossfades; Finger uses one take
at all velocities. Steel retains the discrete 1–48, 49–96 and 97–127 layers.
Pitch and amplitude randomization, velocity gain, release, and per-string
`group`/`off_by` behavior are inherited unchanged from the reference map.
Separate sampler instances cannot choke each other's voices.

This change isolates physical strings. It does not change nylon's crossfade
design or claim that every velocity in a blend selects only one region.

## OGG and WAV paths

The maps in the repository use OGG previews. Keep the collection layout:

```text
meta-steel-guitar/
  meta-steel-guitar.sfz
  meta-steel-guitar-sforzando.sfz
  ogg/
    INSGuitarSteel_StringB_Vel02_C4_01.ogg
    ...
  string-maps/
    meta-steel-guitar-StringLowE.sfz
    ...
```

For a WAV release, extract that collection's official WAV archive and run this
command from the repository root, using the directory that contains the WAVs:

```sh
python3 tools/prepare_guitar_wav_maps.py meta-steel-guitar /path/to/meta-steel-guitar
python3 tools/prepare_guitar_wav_maps.py meta-nylon-guitar /path/to/meta-nylon-guitar
```

The helper creates the keyboard map and `string-maps/` next to the existing
samples. It changes sample extensions to `.wav`, removes the keyboard map's
`default_path=ogg/`, and changes the string maps' path to `default_path=../`.
It checks sample existence and refuses to replace a different existing map.
It reads no audio content and leaves the extracted reference SFZ and samples
untouched. No extra sample downloads or format conversion are required.

The v1.0.0 release ZIPs predate these alternate maps. Maintainers can include
the new maps in a subsequent OGG/WAV release using the same path conversion
and generate that archive's `SHA256SUMS` after packaging.

## Reproduce the channel stacking

1. Load the original `meta-nylon-guitar.sfz` or `meta-steel-guitar.sfz` from
   its v1.0.0 WAV release in sforzando 1.982 on macOS Apple Silicon. Bypass
   Ambience and use one sampler instance with MIDI channel 1.
2. For nylon, select the default Auto keyswitch (MIDI 24). Send one Note On
   for MIDI 60 at velocity 64, then Note Off. Use MIDI numbers because host
   octave labels differ.
3. Compare against the B-string Vel02 C4 sample played alone. The original
   maps sound like several recordings of the same note together.
4. Load the prepared `<collection-id>-sforzando.sfz` and repeat. At this
   velocity, the keyboard map plays the B-string Vel02 C4 recording alone.

In deterministic native VST3 comparisons at 48 kHz/512-frame buffers, the
original nylon output matched A, D, G and B recordings summed at unity gain;
the original steel output matched Low E, A, D, G and B. Channel 8 also sounded,
although the reference file maps only channels 1–7. Moving channel opcodes to
groups or regions did not resolve the observed nylon stacking.

The comparisons disable `pitch_random` and `amp_random` only in diagnostic
copies, so waveforms can be compared. The distributed alternate maps retain
both settings. Single-region comparisons and preserved region/group opcodes
support the compatibility fix; this does not establish support in untested
samplers.

## Validate the maps

Run from the repository root with Python 3.11 or later:

```sh
python3 tools/verify_guitar_sfz_maps.py
```

This reads the SFZs, manifests, catalog and collection checksums. It verifies
that each alternate map retains its corresponding reference channel's region
opcodes, covers its full key/velocity/keyswitch range, selects only one physical
string for each note, resolves all sample paths, and keeps every original
recording accessible. Nylon's intended velocity overlaps are allowed. Native
sampler playback remains a separate manual check using the steps above.
