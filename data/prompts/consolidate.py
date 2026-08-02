"""Consolidate all prompts into 1 file."""
import json
from pathlib import Path


def main():
    src_dir = Path(__file__).parent
    all_prompts = []
    for json_file in sorted(src_dir.glob("*.json")):
        if json_file.name == "all_prompts.json":
            continue
        with open(json_file, encoding="utf-8") as f:
            prompts = json.load(f)
        all_prompts.extend(prompts)
    out_file = src_dir / "all_prompts.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_prompts, f, ensure_ascii=False, indent=2)
    print(f"Consolidated {len(all_prompts)} prompts → {out_file}")


if __name__ == "__main__":
    main()
