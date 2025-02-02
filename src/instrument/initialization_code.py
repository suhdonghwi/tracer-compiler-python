def make_initialization_code():
    import_code = "\n".join(
        ["import tracer_runtime_python", "tracer_runtime_python.initialize()"]
    )

    return import_code
