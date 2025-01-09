from pydantic import BaseModel
from typing import List, Literal
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship



class Conviction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

class Distortion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    situation: str = Field(index=True)
    thoughts: str = Field(index=True)
    support: str = Field(index=True)


class EmotionType(str, Enum):
    POSITIVE = 'Положительная'
    NEGATIVE = 'Отрицательная'

class Emotion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: EmotionType

class NotePublic(Note):
    id: int

class EmotionPublic(Emotion):
    id: int

class ConvictionPublic(Conviction):
    id: int

class DistortionPublic(Distortion):
    id: int

class Note_emotion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    note_id: int | None = Field(default=None, foreign_key="note.id")
    emotion_id:  int | None = Field(default=None, foreign_key="emotion.id")

class Note_conviction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    note_id: int | None = Field(default=None, foreign_key="note.id")
    conviction_id:  int | None = Field(default=None, foreign_key="conviction.id")

class Note_distortion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    note_id: int | None = Field(default=None, foreign_key="note.id")
    distortion_id:  int | None = Field(default=None, foreign_key="distortion.id")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
   
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/notes/")
def create_note(note: Note, session: SessionDep) -> Note:
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.get("/notes/")
def read_notes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Note]:
    notes = session.exec(select(Note).offset(offset).limit(limit)).all()
    return notes



@app.get("/emotions/", response_model=list[Emotion])
def read_emotions(
    session: SessionDep
    ) -> list[Emotion]:
    return session.exec(select(Emotion)).all()

@app.get("/convictions/", response_model=list[Conviction])
def read_convictions(
    session: SessionDep
    ) -> list[Conviction]:
    return session.exec(select(Conviction)).all()

@app.get("/distortions/", response_model=list[Distortion])
def read_distortions(
    session: SessionDep
    ) -> list[Distortion]:
    return session.exec(select(Distortion)).all()

@app.get("/note_emotions/", response_model=list[Note_emotion])
def read_note_emotions(
    session: SessionDep
    ) -> list[Note_emotion]:
    return session.exec(select(Note_emotion)).all()

@app.post("/note_emotions/")
def create_note_emotions(note_emotion: Note_emotion, session: SessionDep) -> Note_emotion:
    session.add(note_emotion)
    session.commit()
    session.refresh(note_emotion)
    return note_emotion

@app.post("/note_convictions/")
def create_note_convictions(note_conviction: Note_conviction, session: SessionDep) -> Note_conviction:
    
    session.add(note_conviction)
    session.commit()
    session.refresh(note_conviction)
    return note_conviction

@app.post("/note_distortions/")
def create_note_distortions(note_distortion: Note_distortion, session: SessionDep) -> Note_distortion:
    session.add(note_distortion)
    session.commit()
    session.refresh(note_distortion)
    return note_distortion

@app.get("/note_convictions/", response_model=list[Note_conviction])
def read_note_convictions(
    session: SessionDep
    ) -> list[Note_conviction]:
    return session.exec(select(Note_conviction)).all()

@app.get("/note_distortions/", response_model=list[Note_distortion])
def read_note_distortions(
    session: SessionDep
    ) -> list[Note_distortion]:
    return session.exec(select(Note_distortion)).all()

