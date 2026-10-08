# Contributing to Meta Open Sound

We want to make contributing to this project as easy and transparent as
possible.

## Our development process

The source of truth for this library is maintained internally at Meta and
mirrored to GitHub. We welcome contributions of new sounds, corrections to
metadata, and improvements to documentation via pull requests and issues.

## Contributor License Agreement (CLA)

In order to accept your contribution, we need you to submit a CLA. You only need
to do this once to work on any of Meta's open source projects.

Complete your CLA here: <https://code.facebook.com/cla>

## Pull requests

1. Fork the repo and create your branch from `main`.
2. If you're contributing audio, make sure it meets the audio standards below.
3. Update `catalog.json` and the collection `manifest.json` if you add or change
   a collection.
4. Ensure file names follow the [naming convention](docs/naming-convention.md).
5. Make sure your contribution is your own work (or properly cleared) and can be
   released under CC0.

## Issues

We use GitHub issues to track public bugs and requests. Please provide clear
descriptions and steps to reproduce when reporting a problem with a sample or
its metadata.

## Audio standards

| Attribute | Standard |
| --- | --- |
| Master format | WAV. 24-bit / 48 kHz preferred; a contribution's source format is preserved rather than converted |
| Web preview | OGG Vorbis. Channel layout follows the source — stereo and ambisonic material is not downmixed |
| Naming | UCS-aligned — see [docs/naming-convention.md](docs/naming-convention.md) |
| Metadata | Every collection includes a `README.md` design spec and a `manifest.json` sample list |
| Loudness | Consistent, un-clipped levels across a collection |

## License

By contributing to Meta Open Sound, you agree that your contributions will be
licensed under [CC0 1.0 Universal](LICENSE), dedicating them to the public
domain. You also agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
