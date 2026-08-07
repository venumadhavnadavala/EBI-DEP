from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.sales import router as sales_router
from routers.inventory import router as inventory_router
from routers.ai_insights import router as ai_router

app = FastAPI(
    title="Enterprise BI Platform",
    version="1.0.0"
)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------

app.include_router(sales_router)
app.include_router(inventory_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {"message": "Enterprise BI Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}