"""Prepare the alternate guitar SFZs beside an extracted WAV library.

Copies map text only. Existing samples and reference maps are never modified.
"""
import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ("meta-nylon-guitar", "meta-steel-guitar")


def prepare(collection_id, wav_dir):
    collection = ROOT / "systems/instruments" / collection_id
    manifest = json.loads((collection / "manifest.json").read_text())
    maps = manifest["sfz_maps"]
    paths = [maps["keyboard"], *maps["strings"].values()]
    pending = []
    for relative in paths:
        text = (collection / relative).read_text()
        if relative == maps["keyboard"]:
            old, new = "<control>\ndefault_path=ogg/\n", ""
        else:
            old, new = "default_path=../ogg/\n", "default_path=../\n"
        if text.count(old) != 1:
            raise ValueError(f"Unexpected sample-path layout: {relative}")
        text = text.replace(old, new)
        text = re.sub(r"(sample=[^\s]+)\.ogg\b", r"\1.wav", text)
        for sample in re.findall(r"\bsample=([^\s]+)", text):
            if not (wav_dir / sample).is_file():
                raise ValueError(f"Missing WAV sample: {wav_dir / sample}")
        target = wav_dir / relative
        data = text.encode()
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f"Refusing to overwrite a different map: {target}")
        pending.append((target, data))
    # Preflight every path before creating any map.
    for target, data in pending:
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
    return [str(target) for target, _ in pending]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", choices=COLLECTIONS)
    parser.add_argument("wav_dir", type=Path,
                        help="Directory containing that collection's extracted WAV samples")
    args = parser.parse_args()
    try:
        paths = prepare(args.collection, args.wav_dir.resolve())
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print("\n".join(paths))


if __name__ == "__main__":
    main()
