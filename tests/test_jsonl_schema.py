import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CASE_FILE = BASE_DIR / "eval_data" / "test_cases.jsonl"
BATCH_FILE = BASE_DIR / "generated" / "batch_input.jsonl"


def read_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def test_eval_data_schema():
    rows = read_jsonl(CASE_FILE)
    assert len(rows) >= 1

    ids = set()

    for row in rows:
        assert "id" in row
        assert "question" in row
        assert "expected_keywords" in row
        assert isinstance(row["expected_keywords"], list)
        assert len(row["expected_keywords"]) >= 1
        assert row["id"] not in ids
        ids.add(row["id"])


def test_build_batch_input_format():
    subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "build_batch_input.py")],
        check=True,
        cwd=str(BASE_DIR),
    )

    rows = read_jsonl(BATCH_FILE)
    assert len(rows) >= 1

    for row in rows:
        assert "custom_id" in row
        assert row["method"] == "POST"
        assert row["url"] == "/v1/chat/completions"
        assert "body" in row
        assert "model" in row["body"]
        assert "messages" in row["body"]
        assert isinstance(row["body"]["messages"], list)
        assert row["body"]["temperature"] == 0
