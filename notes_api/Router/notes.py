from fastapi import APIRouter, HTTPException
from schemas.note import Note


router = APIRouter(
    prefix="/notes", #helps in url no need to chnage url everytime form every where just make chnages here.
    tags=["Notes"] # when there are lot of object just to indentify and make then seprates tags been used.
)

notes = [
     {
            "id": 1,
            "title": "Learn FastAPI",
            "content": "Study CRUD",
            "is_pinned": True
        },
        {
            "id": 2,
            "title": "Learn Python",
            "content": "Study Pydantic",
            "is_pinned": False
        }
]


# create note
@router.post("/")
def create_note(note: Note):
    note_id = len(notes) + 1

    new_note = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
        "is_pinned": note.is_pinned
    }

    notes.append(new_note)

    return {
        "massage": "note created successfull",
       "note": new_note,
    }

# Get all notes
@router.get("/")
def get_notes():
    return {
        "notes": notes
    }

# Get one note 
@router.get("/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note

    raise HTTPException(
        status_code=404,
        detail="note not found"
    )

@router.put("/{note_id}")
def updated_note(note_id: int, updated_note: Note):
    for index, note in enumerate(notes):
        if note["id"] == note_id:

            notes[index] = {
                "id": note_id,
                "title": updated_note.title,
                "content": updated_note.content,
                "is_pinned": updated_note.is_pinned
            }

            return {
                "massage": "note updated successfully",
                "note": notes[index]
            }

    raise HTTPException(
        status_code=404,
        detail="note not found"
    )


@router.delete("/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
           delete_note = notes.pop(index)

           return {
            "massage": "note successfully deleted",
            "note": delete_note
           }

    raise HTTPException(
        status_code=404,
        detail="note not found"
    )