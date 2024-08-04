from fastapi import APIRouter, Form
from app.services.query_service import query_graph

router = APIRouter()

@router.post("/query")
async def query_graph_endpoint(query: str = Form(...)):
    answer = query_graph(query)
    return {"answer": answer}
