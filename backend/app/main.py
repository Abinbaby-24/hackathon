from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    products,
    inspections,
    scan,
    violations,
    reports
)

app = FastAPI(
    title="Hackathon API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(products.router)
app.include_router(inspections.router)
app.include_router(scan.router)
app.include_router(violations.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Hackathon backend is running"
    }