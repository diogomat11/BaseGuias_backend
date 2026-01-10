```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import engine, Base
from .routes import auth, carteirinhas, jobs, guias, logs

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Base Guias Unimed API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Base Guias Unimed API is running"}

from .routes import carteirinhas, jobs, guias, logs, auth

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(carteirinhas.router)
app.include_router(jobs.router)
app.include_router(guias.router)
app.include_router(logs.router, prefix="/api/logs")

