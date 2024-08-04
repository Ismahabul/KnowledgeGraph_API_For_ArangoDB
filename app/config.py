import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ARANGO_HOSTS = os.getenv("ARANGO_HOSTS")
    ARANGO_DB_NAME = os.getenv("ARANGO_DB_NAME")
    ARANGO_USERNAME = os.getenv("ARANGO_USERNAME")
    ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD")
