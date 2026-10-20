# Oculus Audio Pack 1

289 sounds / 508 files from Oculus Audio Pack 01 (v1.0,
December 2015), the general-purpose game and VR sound effects pack the
Oculus sound design team released for developers. Footsteps on six
surfaces, UI sets in seven themes, character vocals, doors, ambiences,
musical stings, horror and interaction foley.

**License: CC BY 4.0.** Unlike the CC0 collections in this repository,
these sounds require credit. See [License](#license) below.

## Finding a sound

This collection is a set of unrelated sounds, so you find one by
describing it rather than by parameters. `index/` holds one file per
UCS category (`index/FEET.json`, `index/UI.json`, ...). Each sound has a
one-line `summary` and a list of `keywords`; search those.

```bash
# every footstep sound with its summary
jq -r '.sounds[] | "\(.id)\t\(.summary)"' index/FEET.json
```

A sound's playable files are its `takes[]`. Each take's preview is
`ogg/<take file stem>.ogg`: `FEETHmn_ShoeSnowWalk_OS_03.wav` →
`ogg/FEETHmn_ShoeSnowWalk_OS_03.ogg`. The full-quality WAVs are
attached to the `oculus-audio-pack-v<version>` GitHub Release.

## What is here

- **44 UCS categories.** Largest: UI (43), VOX (27), MUSC (20), DOOR (19), FEET (18), CREA (17)
- **46.8 minutes** of audio; 34 sounds are seamless loops
- Sample rate: 48000 Hz (508)
- Bit depth: 16-bit (508)
- Channels: 1 (456) · 2 (52)
- Source folders: `01_creepy_horror` (39), `02_floors_footsteps_body_mvmt_impacts_actions_etc` (149), `03_weather_ambience_etc` (44), `04_indoors_hums_machines_actions_etc` (33), `05_user_interface` (54), `06_vocal` (97), `07_doors` (23), `08_stings` (25), `09_car` (10), `10_interaction` (34)

## Reading a sound record

- `summary`: a one-line 'use for …'. Search this first.
- `takes[]`: interchangeable variations (`asset_format: Shuffle`).
  Rotate through them; footsteps have five takes per gait.
- `ucs`: the Universal Category System placement, assigned from the
  folder and filename without a listening pass, so `confidence` is
  `machine`. Trust `summary` over the category when they disagree.
- `provenance`: the pack's original filename stem and folder,
  including the speaker subfolder for character vocals
  (`06_vocal/Troll`). The manifest's `samples[].original_name` is each
  file's exact original path.
- Sets are named consistently across sounds: the UI themes share
  Back/Close/Confirm/Error/Open, and each character voice shares
  Death/DeathScream/Effort/Hurt/Laugh.

The WAVs are byte-identical copies of the originals, renamed only.

## License

Licensed under Creative Commons Attribution 4.0 International
([CC BY 4.0](LICENSE)), © 2015 Oculus VR, LLC. You can use these sounds
for any purpose, including commercially, but when you redistribute them,
or anything you make with them, credit them like this:

> "Oculus Audio Pack 01" by Oculus VR, LLC (https://developers.meta.com/vr/downloads/package/oculus-audio-pack-1/), licensed under CC BY 4.0. Files renamed to the UCS naming convention; OGG previews transcoded from the original WAVs.

The same line is in [ATTRIBUTION.md](ATTRIBUTION.md), and in the
`attribution` field of `manifest.json` and every index file.
