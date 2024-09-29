from dataclasses import dataclass

@dataclass
class FileInfo:
    path: str
    original_code: str


@dataclass
class NodeInfo:
    file_uuid: str
    begin_offset: int
    end_offset: int
