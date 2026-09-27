from datetime import datetime

from pydantic import BaseModel


class CodeFile(BaseModel):
    file_id: str
    path: str
    filename: str
    language: str
    file_type: str
    content: str
    size_bytes: int
    modified_at: datetime
    content_hash: str