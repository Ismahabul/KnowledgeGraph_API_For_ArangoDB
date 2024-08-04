from fastapi import FastAPI
from app.routers import upload_router, query_router

app = FastAPI()

app.include_router(upload_router.router, prefix="/upload", tags=["Upload API"])
app.include_router(query_router.router, prefix="/query", tags=["Query API"])

@app.get("/")
def home():
    return {"message": "Welcome to the Knowledge Graph API"}