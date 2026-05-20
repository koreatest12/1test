import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
FORBIDDEN_PATTERNS = [
    "OPENAI_API_KEY",
    "from openai import",
    "import openai",
    "client.batches",
    "client.files.create",
    "api.openai.com",
]

SCAN_PATHS = [
    BASE_DIR / ".github" / "workflows",
    BASE_DIR / "scripts",
    BASE_DIR / "requirements-offline.txt",
]

ALLOWLIST_FILES = {
    "scripts/offline_safety_check.py",
}


def iter_text_files(path: Path):
    if path.is_file():
        yield path
        return

    if not path.exists():
        return

    for item in path.rglob("*"):
        if item.is_file() and item.suffix in {".py", ".yml", ".yaml", ".txt", ".md"}:
            yield item


def main():
    violations = []

    for scan_path in SCAN_PATHS:
        for file_path in iter_text_files(scan_path):
            rel = file_path.relative_to(BASE_DIR).as_posix()
            if rel in ALLOWLIST_FILES:
                continue

            text = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in text:
                    violations.append(f"{rel}: contains forbidden pattern: {pattern}")

    if violations:
        print("Offline safety check failed.")
        for item in violations:
            print(f"- {item}")
        sys.exit(1)

    print("Offline safety check passed: no API-related execution patterns found in offline workflow scope.")


if __name__ == "__main__":
    main()
