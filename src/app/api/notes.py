from typing import List

from app.api import crud
from app.api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "tag": payload.tag,
        "topic": payload.topic,
        "summary": payload.summary,
        "digest": payload.digest,
        "source_url": payload.source_url,
        "target_url": payload.target_url,
        "time_ref": payload.time_ref,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = {
        "id": note_id,
        "tag": payload.tag,
        "topic": payload.topic,
        "summary": payload.summary,
        "digest": payload.digest,
        "source_url": payload.source_url,
        "target_url": payload.target_url,
        "time_ref": payload.time_ref,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note
