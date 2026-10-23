"""Check alternate guitar maps against the reference SFZ and sample inventory.

Uses the standard library, reads files only, and does not invoke a sampler.
"""
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STRINGS = ("LowE", "A", "D", "G", "B", "HighE")


def parse(path):
    text = re.sub(r"//[^\n]*", "", path.read_text())
    controls, global_ops, master, group, regions = {}, {}, {}, {}, []
    for tag, body in re.findall(r"<(\w+)>([^<]*)", text):
        ops = dict(re.findall(r"(\w+)=([^\s]+)", body))
        if tag == "control":
            controls.update(ops)
        elif tag == "global":
            global_ops, master, group = ops, {}, {}
        elif tag == "master":
            master, group = ops, {}
        elif tag == "group":
            group = ops
        elif tag == "region":
            regions.append({**global_ops, **master, **group, **ops})
        else:
            raise ValueError(f"Unexpected SFZ header in {path}: {tag}")
    return controls, regions


def strip_channel(region):
    return {k: v for k, v in region.items() if k not in ("lochan", "hichan")}


def note_number(sample):
    match = re.search(r"_([A-G])(s?)(-?\d+)_01\.(?:ogg|wav)$", sample)
    assert match, sample
    note, sharp, octave = match.groups()
    return 12 * (int(octave) + 1) + dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)[note] + bool(sharp)


def verify_collection(collection_id, catalog_entry):
    collection = ROOT / "systems/instruments" / collection_id
    manifest = json.loads((collection / "manifest.json").read_text())
    maps = manifest["sfz_maps"]
    assert catalog_entry["sfz_maps"] == maps
    assert list(maps["strings"]) == list(STRINGS)
    controls, original = parse(collection / maps["reference"])
    inventory = {Path(s["file"]).with_suffix(".ogg").name for s in manifest["samples"]}
    all_samples, summaries = set(), []
    for channel, relative in enumerate([maps["keyboard"], *maps["strings"].values()], 1):
        path = collection / relative
        controls, regions = parse(path)
        expected = [strip_channel(r) for r in original
                    if int(r.get("lochan", 1)) <= channel <= int(r.get("hichan", 16))]
        assert regions == expected, f"Reference mapping differs: {relative}"
        assert not any("lochan" in r or "hichan" in r for r in regions)
        assert "<master>" not in path.read_text()
        by_key = {key: [] for key in range(128)}
        for region in regions:
            low = int(region.get("lokey", region.get("key", 0)))
            high = int(region.get("hikey", region.get("key", 127)))
            center = int(region.get("pitch_keycenter", region.get("key", 60)))
            assert low == high and center == note_number(region["sample"])
            sample = region["sample"]
            assert sample in inventory
            assert (path.parent / controls.get("default_path", "") / sample).is_file()
            assert region["group"] == region["off_by"]
            by_key[low].append(region)
            all_samples.add(sample)
        played_keys = [key for key, candidates in by_key.items() if candidates]
        low, high = min(played_keys), max(played_keys)
        assert played_keys == list(range(low, high + 1))
        styles = [24, 25, 26] if collection_id == "meta-nylon-guitar" else [None]
        for style in styles:
            for key, candidates in by_key.items():
                for velocity in range(1, 128):
                    selected = [r for r in candidates
                                if (style is None or int(r["sw_last"]) == style)
                                and int(r.get("lovel", 1)) <= velocity <= int(r.get("hivel", 127))]
                    assert bool(selected) == (low <= key <= high), (relative, style, key, velocity)
                    # Nylon intentionally blends velocity layers. They must belong
                    # to the same physical string, unlike the reported channel stacking.
                    strings = {re.search(r"_String([^_]+)_", r["sample"]).group(1) for r in selected}
                    assert len(strings) <= 1, (relative, style, key, velocity, strings)
                    if selected and channel > 1:
                        assert strings == {STRINGS[channel - 2]}
                    if selected and collection_id == "meta-steel-guitar":
                        assert len(selected) == 1
        summaries.append(dict(path=relative, regions=len(regions), midi_range=[low, high],
                              channel_filtering="none; identical routing on all 16 channels",
                              velocity_and_style_coverage="passed"))
    assert all_samples == inventory
    checked = set()
    for line in (collection / "SHA256SUMS").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        path = collection / relative
        with path.open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == digest, relative
        checked.add(relative)
    files = {p.relative_to(collection).as_posix() for p in collection.rglob("*")
             if p.is_file() and p.name not in ("SHA256SUMS", ".DS_Store")}
    assert checked == files, "Collection checksum coverage differs"
    return dict(collection=collection_id, samples=len(inventory), maps=summaries,
                reference_opcodes_preserved=True, all_sample_paths_resolve=True,
                checksum_files_verified=len(checked))


def main():
    catalog = json.loads((ROOT / "catalog.json").read_text())
    results = []
    for collection_id in ("meta-nylon-guitar", "meta-steel-guitar"):
        entry = next(e for e in catalog["collections"] if e["id"] == collection_id)
        results.append(verify_collection(collection_id, entry))
    print(json.dumps(dict(all_passed=True, collections=results), indent=2))


if __name__ == "__main__":
    main()
