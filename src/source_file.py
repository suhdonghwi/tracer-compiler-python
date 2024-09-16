from dataclasses import dataclass

@dataclass
class SourceFile:
    path: str
    content: str

    def __init__(self, path: str):
        self.path = path

        with open(path, "r") as f:
            self.content = f.read()

    def __repr__(self):
        return f"SourceFile(path='{self.path}', content=...)"
