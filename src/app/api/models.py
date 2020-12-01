from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    tag: str = Field(..., min_length=3, max_length=50)
    summary: str = Field(..., min_length=3, max_length=50)
    revision: str = Field(..., min_length=3, max_length=50)
    local_time: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int
