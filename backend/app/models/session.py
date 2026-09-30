from pydantic import BaseModel

class SessionBase(BaseModel):
    passenger_name: str
    route: str
    date: str
    time: str

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
