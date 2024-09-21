from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceFile:
    path: Path
    content: str

    def __init__(self, path: Path, content: str):
        self.path = path
        self.content = content

    @classmethod
    def from_path(cls, path: Path):
        return cls(path=path, content=Path(path).read_text())
