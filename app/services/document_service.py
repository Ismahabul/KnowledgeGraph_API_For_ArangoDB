from langchain_community.document_loaders import TextLoader, WikipediaLoader, WebBaseLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

def load_documents(source_type: str, source: str):
    if source_type == "wikipedia":
        return WikipediaLoader(query=source).load()
    elif source_type == "pdf":
        return PyPDFLoader(source).load_and_split()
    elif source_type == "web":
        return WebBaseLoader(source).load()
    elif source_type == "text":
        return TextLoader(source).load()
    else:
        raise ValueError(f"Invalid source type: {source_type}")

def split_documents(documents):
    text_splitter = TokenTextSplitter(chunk_size=2024, chunk_overlap=24)
    return text_splitter.split_documents(documents)
