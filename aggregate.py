from pathlib import Path
from typing import Dict, Any, cast
import json


def collect_metadata_files(directory: Path) -> Dict[str, Path]:
    """Collects metadata files from the directory and maps file_ids to their corresponding paths."""
    metadata_files: Dict[str, Any] = {}

    # Find all files ending with .tracer-metadata.json
    for metadata_file in directory.rglob("*.tracer_metadata.json"):
        # Load the content of each file and extract the file_id
        with metadata_file.open("r", encoding="utf-8") as f:
            content: Dict[str, Any] = json.load(f)
            file_id: str = cast(str, content.get("file_id"))
            if file_id:
                metadata_files[file_id] = content

    return metadata_files


def main() -> None:
    dist_dir: Path = Path("./dist")
    tracer_file: Path = dist_dir / "__tracer__" / "trace.json"
    output_file: Path = dist_dir / "test-output.json"

    # Collect metadata files
    metadata_files: Dict[str, Path] = collect_metadata_files(dist_dir)

    # Read trace.json content as a string
    with tracer_file.open("r", encoding="utf-8") as trace_f:
        trace_content = trace_f.read()

    # Prepare the final output structure using string concatenation
    metadata_files_json = json.dumps(
        {
            "metadata_files": {
                file_id: content for file_id, content in metadata_files.items()
            }
        },
        indent=2,
    )

    final_output = f'{metadata_files_json[:-2]},\n  "trace": {trace_content}\n}}'

    # Write the final output to test-output.json
    with output_file.open("w", encoding="utf-8") as f:
        f.write(final_output)


if __name__ == "__main__":
    main()
