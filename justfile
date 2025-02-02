compile input:
  uv run python src/main.py {{input}} dist

run input:
  -(cd dist && python {{input}})
  python aggregate.py
  cp dist/eval_event_log.json ../tracer-web/public/eval_event_log.json
  cp dist/source_file_metadata_list.json ../tracer-web/public/source_file_metadata_list.json
