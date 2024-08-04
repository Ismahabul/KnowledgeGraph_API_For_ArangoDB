from fastapi import APIRouter, UploadFile, File, Form
from app.services.document_service import load_documents, split_documents
from app.services.arango_service import create_graph_collection
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.chat_models import ChatOpenAI
from app.config import Config

router = APIRouter()

@router.post("/upload")
async def upload_source(
    source_type: str = Form(...),
    source: UploadFile = File(...),
):
    source_path = f"uploaded_files/{source.filename}"
    with open(source_path, "wb") as f:
        f.write(await source.read())

    raw_documents = load_documents(source_type, source_path)
    documents = split_documents(raw_documents)

    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY)
    llm_transformer = LLMGraphTransformer(llm=llm)
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    create_graph_collection(graph_documents)

    return {"status": "Graph collection has been created in ArangoDB"}

