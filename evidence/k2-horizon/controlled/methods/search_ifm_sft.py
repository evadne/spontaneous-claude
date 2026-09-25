import json
import re
import time

import duckdb


URL = (
    "https://huggingface.co/datasets/IFM/SFT-Reasoning/resolve/main/"
    "3efforts-pretrain/"
    "3efforts_pretrain_16k.chunk0-a9b71abcd1-00000.parquet"
)
OUTPUT = (
    "/Users/evadne/Projects/k2-horizon-controlled/dataset-probes/"
    "sft-3efforts-shard0-assistant-claude-identity.json"
)

connection = duckdb.connect()
connection.execute("SET threads = 8")

query = f"""
SELECT text, token_count
FROM read_parquet('{URL}')
WHERE text ILIKE '%Claude%'
"""

started = time.monotonic()
rows = connection.execute(query).fetchall()
elapsed = time.monotonic() - started

identity_pattern = re.compile(
    r"(?i)(?:\b(?:I am|I'm|I’m|my name is)\s+Claude\b|"
    r"\bClaude\s*,\s+(?:an?\s+)?AI\s+(?:assistant|language model)\b|"
    r"\bAs Claude\s*,\s*I\b)"
)

records = []
for text, token_count in rows:
    assistant_segments = re.findall(
        r"(?is)(?:^|\n)ASSISTANT:\s*(.*?)(?=\n(?:USER|ASSISTANT):|\Z)",
        text,
    )
    matching_segments = [segment for segment in assistant_segments if identity_pattern.search(segment)]
    if matching_segments:
        records.append(
            {
                "text": text,
                "token_count": token_count,
                "matching_assistant_segments": matching_segments,
            }
        )

payload = {
    "source": URL,
    "query_kind": "Claude identity phrases restricted to ASSISTANT segments",
    "elapsed_seconds": elapsed,
    "claude_bearing_records": len(rows),
    "matches": len(records),
    "records": records,
}

import os

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as output_file:
    json.dump(payload, output_file, ensure_ascii=False, indent=2)

print(json.dumps({key: value for key, value in payload.items() if key != "records"}, indent=2))
for index, record in enumerate(records[:10], start=1):
    lowered = record["text"].lower()
    position = lowered.find("claude")
    start = max(0, position - 500)
    end = min(len(record["text"]), position + 1500)
    print(f"\n--- MATCH {index} token_count={record['token_count']} ---")
    print(record["text"][start:end])
