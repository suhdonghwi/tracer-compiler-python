compile input:
  uv run python src/main.py {{input}} dist

run input:
  -(cd dist && python {{input}})
  python aggregate.py
