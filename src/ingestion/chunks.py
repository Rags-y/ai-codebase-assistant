from pydantic import BaseModel


class CodeChunk(BaseModel):
    chunk_id: str
    file_id: str
    path: str
    language: str

    chunk_type: str
    name: str

    start_line: int
    end_line: int

    content: str

    parent_file: str | None = None