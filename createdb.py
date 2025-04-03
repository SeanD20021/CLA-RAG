import chromadb
import ollama
from embeddingfunction import EmbeddingFunction


embedding_function = EmbeddingFunction()

chroma_client = chromadb.HttpClient(host='localhost', port=8000)

collection = chroma_client.create_collection(name="my_collection", embedding_function=embedding_function)