compile input:
  uv run python src/main.py {{input}} dist

run input:
  -(cd dist && python {{input}})
  python aggregate.py

move:
  mv dist/execution_log.json ../tracer/public/execution_log.json
  mv dist/metadata_files.json ../tracer/public/metadata_files.json
