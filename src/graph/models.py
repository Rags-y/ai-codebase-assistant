from pydantic import BaseModel


class CodeRelationship(BaseModel):

    source_id: str

    target_id: str

    relationship: str