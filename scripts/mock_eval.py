import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "generated" / "batch_input.jsonl"
CASE_FILE = BASE_DIR / "eval_data" / "test_cases.jsonl"
OUT_FILE = BASE_DIR / "generated" / "mock_results.jsonl"


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. Run scripts/build_batch_input.py first."
        )

    cases = {item["id"]: item for item in load_jsonl(CASE_FILE)}
    batch_inputs = load_jsonl(INPUT_FILE)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUT_FILE.open("w", encoding="utf-8") as f:
        for req in batch_inputs:
            custom_id = req["custom_id"]
            item = cases[custom_id]
            keywords = item["expected_keywords"]

            mock_answer = (
                f"[MOCK ANSWER] 질문: {item['question']} / "
                f"핵심 포함: {', '.join(keywords)}"
            )

            result = {
                "id": f"mock-result-{custom_id}",
                "custom_id": custom_id,
                "response": {
                    "status_code": 200,
                    "request_id": f"mock-request-{custom_id}",
                    "body": {
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": mock_answer,
                                }
                            }
                        ]
                    },
                },
                "error": None,
            }

            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"Mock results created: {OUT_FILE}")
    print(f"Mock count: {len(batch_inputs)}")


if __name__ == "__main__":
    main()
