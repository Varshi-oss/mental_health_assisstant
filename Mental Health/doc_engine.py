import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
llm = GoogleGenAI(model="gemini-1.5-flash", api_key=api_key)

# Set your data directory
data_dir = "data"

# Create folder if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Directory '{data_dir}' created. Please add documents to it.")

# Load documents
documents = SimpleDirectoryReader(data_dir).load_data()

# Initialize a local embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Build the index using the specified LLM and embedding model
index = VectorStoreIndex.from_documents(
    documents,
    llm=llm,
    embed_model=embed_model
)

# Expose the retriever globally
retriever = index.as_retriever()

# Set up the query engine, explicitly passing your LLM
query_engine = index.as_query_engine(llm=llm)

def query_documents(user_query: str) -> str:
    """
    Query your indexed documents using Google Gemini LLM.
    """
    return str(query_engine.query(user_query))
