from pathlib import Path

def find_project_root(markers=(".git", "README.md", "pyproject.toml", ".env")):
    current = Path.cwd().resolve()
    for folder in (current, *current.parents):
        if any((folder / m).exists() for m in markers):
            return folder
    return current