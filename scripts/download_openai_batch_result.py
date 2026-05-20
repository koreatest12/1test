import argparse
import os
from pathlib import Path

from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent
OUT_FILE = BASE_DIR / "generated" / "openai_batch_results.jsonl"


def write_content(response, output_path: Path):
    if hasattr(response, "write_to_file"):
        response.write_to_file(str(output_path))
        return

    if isinstance(response, bytes):
        output_path.write_bytes(response)
        return

    if hasattr(response, "read"):
        data = response.read()
        if isinstance(data, str):
            output_path.write_text(data, encoding="utf-8")
        else:
            output_path.write_bytes(data)
        return

    if hasattr(response, "content"):
        data = response.content
        if isinstance(data, str):
            output_path.write_text(data, encoding="utf-8")
        else:
            output_path.write_bytes(data)
        return

    output_path.write_text(str(response), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-id", default=os.getenv("BATCH_ID"))
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is required.")

    if not args.batch_id:
        raise ValueError("batch id is required. Use --batch-id or BATCH_ID env.")

    client = OpenAI()
    batch = client.batches.retrieve(args.batch_id)

    if batch.status != "completed":
        raise RuntimeError(f"Batch is not completed. Current status: {batch.status}")

    if not batch.output_file_id:
        raise RuntimeError("Batch completed but output_file_id is empty.")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    content_response = client.files.content(batch.output_file_id)
    write_content(content_response, OUT_FILE)

    print(f"Downloaded result: {OUT_FILE}")


if __name__ == "__main__":
    main()
