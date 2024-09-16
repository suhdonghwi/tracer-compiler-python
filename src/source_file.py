from pathlib import Path
from dataclasses import dataclass

@dataclass
class SourceFile:
    path: str
    content: str

    @classmethod
    def from_file(cls, path: str):
        return cls(path=path, content=Path(path).read_text())
