import argparse
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CASE_FILE = BASE_DIR / "eval_data" / "test_cases.jsonl"
DEFAULT_RESULT_FILE = BASE_DIR / "generated" / "mock_results.jsonl"
SUMMARY_FILE = BASE_DIR / "generated" / "score_summary.json"


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


def extract_answer(result: dict) -> str:
    if result.get("error"):
        return ""

    body = result.get("response", {}).get("body", {})
    choices = body.get("choices", [])

    if not choices:
        return ""

    message = choices[0].get("message", {})
    return message.get("content", "") or ""


def judge_case(expected_keywords, answer: str):
    answer_lower = answer.lower()
    missing = []

    for keyword in expected_keywords:
        if keyword.lower() not in answer_lower:
            missing.append(keyword)

    passed = len(missing) == 0
    return passed, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result-file",
        default=str(DEFAULT_RESULT_FILE),
        help="Path to OpenAI Batch result JSONL or mock result JSONL.",
    )
    args = parser.parse_args()

    result_file = Path(args.result_file)

    if not result_file.exists():
        raise FileNotFoundError(f"Result file not found: {result_file}")

    cases = {item["id"]: item for item in load_jsonl(CASE_FILE)}
    results = load_jsonl(result_file)

    details = []
    passed_count = 0

    for result in results:
        custom_id = result.get("custom_id")
        if custom_id not in cases:
            details.append(
                {
                    "id": custom_id,
                    "passed": False,
                    "error": "custom_id not found in test cases",
                }
            )
            continue

        case = cases[custom_id]
        answer = extract_answer(result)
        passed, missing = judge_case(case["expected_keywords"], answer)

        if passed:
            passed_count += 1

        details.append(
            {
                "id": custom_id,
                "category": case.get("category", ""),
                "passed": passed,
                "missing_keywords": missing,
                "answer_preview": answer[:200],
            }
        )

    total = len(results)
    pass_rate = passed_count / total if total else 0.0

    summary = {
        "total": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "pass_rate": pass_rate,
        "result_file": str(result_file),
        "details": details,
    }

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if passed_count != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
