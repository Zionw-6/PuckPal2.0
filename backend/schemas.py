from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Attempt(BaseModel):
    drill_id: str
    drill_title: str
    reps: int
    seconds: float
    rate: float
    date: str

class ProgramEntry(BaseModel):
    day_number: int
    drill_id: str
    reps: int
    minutes: int
