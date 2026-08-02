"""
Shared entrypoint — both members' routers mounted here.
Run: uvicorn main:app --reload --port 8000
Docs auto-generated at /docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import sales, inventory, ai_insights

app = FastAPI(
    title="Enterprise BI Platform API",
    description="Sales & Inventory analytics API — built by a 2-person team.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(ai_insights.router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
