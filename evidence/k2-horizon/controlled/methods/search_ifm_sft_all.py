import json
import os
import time

import duckdb


BASE = (
    "https://huggingface.co/datasets/IFM/SFT-Reasoning/resolve/main/"
    "3efforts-pretrain/"
    "3efforts_pretrain_16k.chunk0-a9b71abcd1-"
)
URLS = [f"{BASE}{index:05d}.parquet" for index in range(58)]
OUTPUT = (
    "/Users/evadne/Projects/k2-horizon-controlled/dataset-probes/"
    "sft-3efforts-all-strict-claude-identity.json"
)

connection = duckdb.connect()
connection.execute("SET threads = 8")
url_list = "[" + ",".join(repr(url) for url in URLS) + "]"

query = f"""
SELECT filename, text, token_count
FROM read_parquet({url_list}, filename = true, union_by_name = true)
WHERE regexp_matches(
        text,
        '(?i)(^|[^A-Za-z])(I am|I''m|I’m|my name is)[[:space:]]+Claude([^A-Za-z]|$)'
      )
   OR regexp_matches(
        text,
        '(?i)Claude[[:space:]]*,[[:space:]]+(an?[[:space:]]+)?AI[[:space:]]+(assistant|language model)'
      )
   OR regexp_matches(
        text,
        '(?i)(^|[\\n\\r\"])[[:space:]]*As Claude[[:space:]]*,[[:space:]]*I'
      )
"""

started = time.monotonic()
rows = connection.execute(query).fetchall()
elapsed = time.monotonic() - started

records = [
    {"filename": filename, "text": text, "token_count": token_count}
    for filename, text, token_count in rows
]
payload = {
    "sources": URLS,
    "query_kind": "strict first-person Claude identity phrases",
    "elapsed_seconds": elapsed,
    "matches": len(records),
    "records": records,
}

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as output_file:
    json.dump(payload, output_file, ensure_ascii=False, indent=2)

print(json.dumps({key: value for key, value in payload.items() if key not in {"records", "sources"}}, indent=2))
for index, record in enumerate(records, start=1):
    lowered = record["text"].lower()
    position = lowered.find("claude")
    start = max(0, position - 700)
    end = min(len(record["text"]), position + 1800)
    print(f"\n--- MATCH {index} {os.path.basename(record['filename'])} token_count={record['token_count']} ---")
    print(record["text"][start:end])
