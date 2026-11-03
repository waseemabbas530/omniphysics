from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

from backend.database import init_db, save_note, save_simulation_config
from backend.models import NoteRequest, SimulationConfigRequest

app = FastAPI(title="OmniPhysics Backend API", version="0.1.0")

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "OmniPhysics Backend Engine Active"}

@app.post("/api/chat")
async def chat_tutor(request: ChatRequest):
    async def event_generator():
        response_text = f"Simulating physics reasoning for: {request.prompt} [LaTeX: E=mc^2]"
        for word in response_text.split(" "):
            yield f"data: {word} \n\n"
            await asyncio.sleep(0.1)
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# New Persistence Endpoints
@app.post("/api/notes")
def create_user_note(note: NoteRequest):
    try:
        save_note(note.topic, note.content)
        return {"status": "success", "message": "User note saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/configs")
def create_simulation_config(config: SimulationConfigRequest):
    try:
        save_simulation_config(config.config_name, config.config_json)
        return {"status": "success", "message": "Simulation configuration saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))