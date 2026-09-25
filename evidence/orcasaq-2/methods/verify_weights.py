"""Compare pinned LFS digests with the local checkpoint."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = Path.home() / "Projects/models/orcasaq-2-27b"

for item in json.loads((HERE / "tree.json").read_text()):
    if not (item["path"].endswith(".safetensors") or item["path"] == "tokenizer.json"):
        continue
    path = MODEL / item["path"]
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            digest.update(block)
    expected = item["lfs"]["oid"].split(":")[-1]
    assert digest.hexdigest() == expected, path
    print(path.name, path.stat().st_size, digest.hexdigest(), "PASS")
