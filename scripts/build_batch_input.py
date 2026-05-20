import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "eval_data" / "test_cases.jsonl"
OUT_DIR = BASE_DIR / "generated"
OUT_FILE = OUT_DIR / "batch_input.jsonl"

MODEL = os.getenv("EVAL_MODEL", "gpt-4o-mini")


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path}:{line_no}: {exc}") from exc
    return rows


def validate_case(item: dict):
    required = ["id", "question", "expected_keywords"]
    for key in required:
        if key not in item:
            raise ValueError(f"Missing required key: {key}")

    if not isinstance(item["expected_keywords"], list) or not item["expected_keywords"]:
        raise ValueError(f"expected_keywords must be a non-empty list: {item.get('id')}")


def build_request(item: dict):
    validate_case(item)

    return {
        "custom_id": item["id"],
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "당신은 IT/보안/배치운영 평가용 AI입니다. "
                        "질문에 대해 정확하고 간결하게 한국어로 답변하세요."
                    ),
                },
                {
                    "role": "user",
                    "content": item["question"],
                },
            ],
            "temperature": 0,
        },
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    cases = load_jsonl(DATA_FILE)
    if not cases:
        raise ValueError("No test cases found.")

    with OUT_FILE.open("w", encoding="utf-8") as f:
        for item in cases:
            request = build_request(item)
            f.write(json.dumps(request, ensure_ascii=False) + "\n")

    print(f"Batch input created: {OUT_FILE}")
    print(f"Case count: {len(cases)}")
    print(f"Model: {MODEL}")


if __name__ == "__main__":
    main()
