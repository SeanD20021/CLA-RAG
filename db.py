from typing import Dict, List
import chromadb
from textExtractor import text_to_text, pdf_to_text, word_to_text, excel_to_text
from pathlib import Path
import uuid
import ollama
from embeddingfunction import EmbeddingFunction
from textchunking import sentence_chunking
from textchunking import text_chunker
import os

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Splits extracted text into smaller chunks of a given size."""
    words = text.split()
    chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def format_text_for_vector_db(text: str, filename: str, sheet_name: str, chunk_size: int = 500) -> List[Dict]:
    """
    Processes extracted Excel text into chunks suitable for a vector database.
    
    Args:
        text (str): The extracted text from an Excel sheet.
        filename (str): The name of the Excel file.
        sheet_name (str): The sheet where the text came from.
        chunk_size (int): Number of words per chunk.

    Returns:
        List of dictionaries containing:
        - 'chunk_text': The chunked text data.
        - 'metadata': Dictionary with 'filename', 'sheet_name', and 'chunk_index'.
    """
    chunks = chunk_text(text, chunk_size)
    formatted_chunks = []

    for i, chunk in enumerate(chunks):
        metadata = {
            "filename": filename,
            "sheet_name": sheet_name,
            "chunk_index": i
        }
        formatted_chunks.append({"chunk_text": chunk, "metadata": metadata})

    return formatted_chunks

embedding_function = EmbeddingFunction()

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection", embedding_function=embedding_function)
path = Path("Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\Reports\\")
filename = "Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\Reports\\2023 Report - Bilsland - POL - Mendez, Catalina V.pdf"
filenameTwo = "Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\Reports\\2023 Report - Ross - HIST - Gyapong, Ignatius.pdf"
filenameThree = "Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\CLA Fellowship Reporting 2023-2024.xlsx"

#text = pdf_to_text(filename)

text = excel_to_text(filenameThree)
print(text)
if (filenameThree[-4:] == "xlsx"):
    print("success")
print(filenameThree[-4:])
#chunks = sentence_chunking(text)
# chunks = text_chunker(text, filename)
# #chunks = format_text_for_vector_db(text, filename, "test")'
# print(len(chunks))
# for chunk in chunks: 
#   print(chunk)
#   print(embedding_function(chunk))
#   print("END OF CHUNK\n\n\n\n")

'''files = path.rglob('*')
documents = []
for f in files:
    text = pdf_to_text(f.__str__())
    documents.append(text)

for i, d in enumerate(documents):
  chunks = sentence_chunking(d)
  print(len(chunks))
  for chunk in chunks:
    print(chunk)
  collection.add(
    ids=[str(i)],
    embeddings=embedding_function(d),
    documents=[d]
  )'''

# results = collection.query(
#     query_texts=["How many andrews fellowship reports are there?"],
#     n_results = 1
# )


# print(results)
# data = results['documents'][0][0]
# print(data)

# output = ollama.generate(
#     model = "llama3.2",
#     prompt = f"Using this data: {data} respond to this prompt: who are the andrews fellowship reports from?"
# )


# print(output['response'])

