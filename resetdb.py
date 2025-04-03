import chromadb

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
#collection = chroma_client.get_collection(name="my_collection")
chroma_client.delete_collection(name="my_collection")