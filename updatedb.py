import chromadb
from textExtractor import text_to_text, pdf_to_text, word_to_text, excel_to_text
from pathlib import Path
import uuid
import ollama
from embeddingfunction import EmbeddingFunction
import nltk
from nltk.tokenize import sent_tokenize
from textchunking import sentence_chunking
from textchunking import text_chunker

nltk.download('punkt_tab')


embedding_function = EmbeddingFunction()

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_collection(name="my_collection", embedding_function=embedding_function)
path = Path("Z:\\Associate Dean Matei\\Fellowship Progress Reporting")

files = path.rglob('*')
documents = []

#will need to change this for loop to check for different file extensions
for f in files:
    print(f.name)
    if (f.name[-3:] == "pdf"):
      text = pdf_to_text(f.__str__())
      chunks = text_chunker(text, f.name)
      
      print(len(chunks))
      for i, chunk in enumerate(chunks):
        #print(chunk)
        result = embedding_function(chunk)
        collection.add(
          ids = [str(uuid.uuid4())],
          embeddings = result[0],
          documents = chunk,
          metadatas={"filename": f.name, "chunkNumber": i}
        )
        #print(result)
        #print(result[0])
    elif (f.name[-4:] == "docx"):
      text = word_to_text(f.__str__())
      chunks = text_chunker(text, f.name)
      print(len(chunks))
      for i, chunk in enumerate(chunks):
        collection.add(
          ids = [str(uuid.uuid4())],
          embeddings = embedding_function(chunk),
          documents = chunk,
          metadatas={"filename": f.name, "chunkNumber": i}
        )
    elif (f.name[-4:] == "xlsx"):
      print("happens")
      text = excel_to_text(f.__str__())
      print(f.__str__())
      print(text)
      #chunks = sentence_chunking(text)
      #print(len(chunks))
      #for chunk in chunks:
      collection.add(
        ids = [str(uuid.uuid4())],
        embeddings = embedding_function(text),
        documents = text,
        metadatas={"filename": f.name, "chunkNumber": 0}

      )
    elif (f.name[-3:] =="txt"):
       text = text_to_text(f.__str__())
       chunks = sentence_chunking(text)
       print(len(chunks))
       for chunk in chunks:
        collection.add(
          ids = [str(uuid.uuid4())],
          embeddings = embedding_function(chunk),
          documents = chunk
        )

#     if len(text) != 0:
#       documents.append(text)
# chunks = []
# for d in enumerate(documents):
#   collection.add(
#     ids=[str(uuid.uuid4())],
#     embeddings=embedding_function(d),
#     documents=[d]
#   )




