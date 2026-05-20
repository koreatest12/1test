import json
import os
from pathlib import Path

from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "generated" / "batch_input.jsonl"
OUT_FILE = BASE_DIR / "generated" / "batch_submit_result.json"


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is required for real_submit mode.")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. Run scripts/build_batch_input.py first."
        )

    client = OpenAI()

    uploaded_file = client.files.create(
        file=INPUT_FILE.open("rb"),
        purpose="batch",
    )

    batch = client.batches.create(
        input_file_id=uploaded_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "project": "github-batch-eval-test",
            "mode": "real_submit",
        },
    )

    result = {
        "input_file_id": uploaded_file.id,
        "batch_id": batch.id,
        "status": batch.status,
        "endpoint": batch.endpoint,
        "completion_window": batch.completion_window,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
