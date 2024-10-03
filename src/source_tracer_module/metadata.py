from pathlib import Path


def load_metadata_files(root_path: Path):
    metadata_files = root_path.rglob("*.tracer-metadata.json")
    return [metadata_file_path.read_text() for metadata_file_path in metadata_files]
