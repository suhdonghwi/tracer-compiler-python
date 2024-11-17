compile input:
  uv run python src/main.py {{input}} dist

run input:
  -(cd dist && python {{input}})
  python aggregate.py

move:
  mv dist/event_log.json ../tracer/public/event_log.json
  mv dist/metadata_files.json ../tracer/public/metadata_files.json
