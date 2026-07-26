from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def read(relative_path: str) -> str:
    """Read a file relative to the project root, regardless of the process's cwd."""
    with open(BASE_DIR / relative_path, "r") as f:
        return f.read()
