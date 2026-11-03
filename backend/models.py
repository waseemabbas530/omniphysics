from pydantic import BaseModel

class NoteRequest(BaseModel):
    topic: str
    content: str

class SimulationConfigRequest(BaseModel):
    config_name: str
    config_json: str