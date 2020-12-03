from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    tag: str = Field(..., min_length=1, max_length=50)
    topic: str = Field(..., min_length=2, max_length=50)
    summary: str = Field(..., min_length=0, max_length=150)
    digest: str = Field(..., min_length=32, max_length=150)
    source_url: str = Field(..., min_length=0, max_length=150)
    target_url: str = Field(..., min_length=0, max_length=150)
    time_ref: str = Field(..., min_length=0, max_length=50)

class NoteDB(NoteSchema):
    id: int
