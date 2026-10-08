# Naming Convention

Meta Open Sound file names follow a convention aligned with the
[Universal Category System (UCS)](https://universalcategorysystem.com/), adapted
for multi-sampled instruments and interaction sounds.

## Pattern

```
{CatID}{SubCatID}_{Descriptor}..._{Variation}.wav
```

| Field | Meaning | Example |
| --- | --- | --- |
| `CatID` | Category prefix (see table below) | `INS` |
| `SubCatID` | Subcategory in PascalCase | `Piano` |
| `Descriptor` | One or more PascalCase fields, largest-to-smallest scope | `Vel03`, `C4` |
| `Variation` | Two-digit zero-padded number (`01`–`99`) | `01` |

Example: `INSPiano_Vel03_C4_01.wav` — an Instruments / Piano sample, velocity
layer 3, note C4, variation 01.

## Category IDs
The vocabulary is the **Universal Category System v8.2.1**, vendored at
[`ucs/ucs_v8.2.1.csv`](../ucs/ucs_v8.2.1.csv) — 715 CatIDs across 82 categories and
100 CatShort codes. That file is the source of truth; `naming.py` loads it directly, so
this document does not restate all 100. Look a code up there rather than guessing.

A UCS CatID is the CatShort and SubCategory concatenated: `ANML` + `Dog` = `ANMLDog`,
`MECH` + `Clik` = `MECHClik`. That is the same shape this library already used
(`INSPiano`), so only the vocabulary changed, not the pattern.

Frequently used CatShorts:

| CatShort | Category |
| --- | --- |
| `AMB` | Ambience |
| `DSGN` | Designed |
| `FOLY` | Foley |
| `METL` | Metal |
| `MECH` | Mechanical |
| `MUSC` | Musical |
| `SWSH` | Swooshes |
| `UI` | User Interface |
| `VOX` | Voices |
| `WATR` | Water |
| `WOOD` | Wood |
| `DOOR` | Doors |
| `CREA` | Creatures |
| `MAG` | Magic |

### Local extensions

Codes we add on top of UCS. Deliberately minimal — the vocabulary is owned, and
contributors pick from it rather than extending it.

| Code | Meaning | Why it is not UCS |
| --- | --- | --- |
| `INS` | Playable virtual instrument | UCS classifies *recordings of* instruments (`MUSCKeyd` is "keyed instruments, such as pianos and harpsichord") and spends its subcategory slot on instrument kind, so it can neither say "piano" nor express "this is a playable multi-sampled instrument". |

> Codes previously listed here — `DES`, `IMP`, `WHH`, `EXP`, `FOL`, `MVT`, `MUS`, `PHY` —
> were not UCS (UCS spells them `DSGN`, `EXPL`, `FOLY`, `MUSC`, `MOVE`, and has no
> IMPACTS/WHOOSHES/PHYSICS category). They were unused by any collection and have been
> removed.

## Note names

Pitched samples encode the note in a descriptor field:

- Natural notes use the note letter and octave: `C4`, `A0`, `G7`.
- Sharps use a lowercase `s` suffix instead of `#`: `A#0` is written `As0`,
  `C#4` is written `Cs4`.
- Octave numbering is scientific pitch notation (middle C = `C4`).

## Velocity layers

Multi-sampled instruments encode velocity as a `Vel{NN}` field:

| Field | Velocity range (0–127) | Dynamic |
| --- | --- | --- |
| `Vel01` | 1–31 | pp (pianissimo) |
| `Vel02` | 32–63 | mp (mezzo-piano) |
| `Vel03` | 64–95 | mf (mezzo-forte) |
| `Vel04` | 96–127 | ff (fortissimo) |
