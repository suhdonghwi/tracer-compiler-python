from pathlib import Path

cwd = Path(__file__).parent
metadata_files = cwd.rglob("*.tracer-metadata.json")

print("Found metadata files: ", list(metadata_files))
