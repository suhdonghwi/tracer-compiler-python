from pathlib import Path
from dataclasses import dataclass


@dataclass
class SourceFile:
    path: str
    content: str

    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content

    @classmethod
    def from_file(cls, path: str):
        return cls(path=path, content=Path(path).read_text())
