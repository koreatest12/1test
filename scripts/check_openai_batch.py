import argparse
import json
import os

from openai import OpenAI


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

    result = {
        "batch_id": batch.id,
        "status": batch.status,
        "endpoint": batch.endpoint,
        "input_file_id": batch.input_file_id,
        "output_file_id": batch.output_file_id,
        "error_file_id": batch.error_file_id,
        "created_at": batch.created_at,
        "completed_at": batch.completed_at,
        "failed_at": batch.failed_at,
        "expired_at": batch.expired_at,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
