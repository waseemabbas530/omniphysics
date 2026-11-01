from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(title="OmniPhysics Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "OmniPhysics Backend Engine Active"}

async def physics_tutor_stream(query: str):
    response_chunks = [
        "Analyzing physical vectors...\n\n",
        "Kinematics equation: $v^2 = u^2 + 2as$\n\n",
        "Calculating launch velocity..."
    ]
    for chunk in response_chunks:
        yield f"data: {chunk}\n\n"
        await asyncio.sleep(0.3)

@app.post("/api/chat")
async def chat_tutor(query: str):
    return StreamingResponse(physics_tutor_stream(query), media_type="text/event-stream")