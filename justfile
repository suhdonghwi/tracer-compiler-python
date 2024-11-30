compile input:
  uv run python src/main.py {{input}} dist

run input:
  -(cd dist && python {{input}})
  python aggregate.py
  cp dist/execution_log.json ../tracer/public/execution_log.json
  cp dist/metadata_files.json ../tracer/public/metadata_files.json
