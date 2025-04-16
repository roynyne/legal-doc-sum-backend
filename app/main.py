# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import preprocess, summarize

app = FastAPI(title="Legal Document Summarizer")

# CORS (for later with frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(preprocess.router, prefix="/preprocess")
app.include_router(summarize.router, prefix="/summarize")
