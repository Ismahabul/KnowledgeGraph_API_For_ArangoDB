from langchain.graphs import ArangoGraph
from langchain.chains import ArangoGraphQAChain
from langchain.chat_models import ChatOpenAI
from app.config import Config
from app.services.arango_service import db

def query_graph(query: str):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY)
    graph = ArangoGraph(db)
    chain = ArangoGraphQAChain.from_llm(llm, graph=graph, verbose=True)
    return chain.invoke(query)
