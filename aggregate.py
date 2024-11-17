from pathlib import Path
import json

# Define the base directory and output file
base_directory = Path("./dist")
output_file = base_directory / "metadata_files.json"

# List to store the aggregated JSON data
aggregated_data = []

try:
    # Check if the base directory exists
    if not base_directory.exists():
        print(f"Directory {base_directory} does not exist.")
    else:
        # Recursively find all files ending with ".tracer_metadata.json"
        tracer_files = base_directory.rglob("*.tracer_metadata.json")

        for file_path in tracer_files:
            try:
                # Read and parse the JSON file
                with file_path.open("r") as file:
                    data = json.load(file)
                    aggregated_data.append(data)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

        # Write the aggregated data to the output file
        with output_file.open("w") as outfile:
            json.dump(aggregated_data, outfile, indent=4)
        print(f"Aggregated metadata has been written to {output_file}.")
except Exception as e:
    print(f"An error occurred: {e}")
