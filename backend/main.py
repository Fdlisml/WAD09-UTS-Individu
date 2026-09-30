from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.session_controller import router as session_router

app = FastAPI(title="Campus Shuttle API (MVC)")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Controller (Router)
app.include_router(session_router)
