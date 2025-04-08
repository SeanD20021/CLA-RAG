import os
import chromadb
from textExtractor import text_to_text, pdf_to_text, word_to_text, excel_to_text
from pathlib import Path
import uuid
import ollama
from embeddingfunction import EmbeddingFunction
from textchunking import sentence_chunking
from textchunking import text_chunker
from docx import Document
import json

path = Path("Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\Reports\\")
filename = "Z:\\Associate Dean Matei\\Fellowship Progress Reporting\\Modified Reports\\final.docx"
doc = Document(filename)

chunks = []
data = []
tempChunk = ""
tempData = ""
for para in doc.paragraphs:
    line = para.text.strip()
    #print(line[1:15])
    if (line == "}"):
        tempData += "}"
        data.append(tempData)
        #print("happens 2")
        #print(tempChunk)
        #print(tempData)
        tempData = ""
        tempChunk = ""
    elif(line[1:15] == "questionNumber"):
        #print("happens")
        tempChunk = tempChunk + line + "\n}"
        tempData = tempData + line + "\n"
        chunks.append(tempChunk)
        #print(tempChunk)
        #print(tempData)
        tempChunk = ""
    else:
        tempChunk = tempChunk + line + "\n"
        tempData = tempData + line + "\n"


client = chromadb.Client()
embedding_function = EmbeddingFunction()

collection = client.create_collection(name="my_collection", embedding_function=embedding_function)

for i, chunk in enumerate(chunks):
    #print(chunk + "\n\n\n")
    result = embedding_function(chunk)
    collection.add(
      ids = [str(uuid.uuid4())],
      embeddings = result,
      documents = data[i],
    )

context = '''
You will recieve a list of document chunks with metadata and the answer to a question. 
It contains in order: the author's name, the year written, the award recieved, the school they are in, question number, and question.
You will recieve questions that require you to summarize or find a pattern between multiple reports for the same question.
'''
queryOne = "who wrote an andrews fellowship report in 2023?"
queryTwo = "can you summarize the answer to question 6 for Adam Taylor, Noah McKay, Savannah Meier, and Quyn-Anh Nguyen"
queryThree = "can you summarize question 6 for the 2023 dean's graduate fellowship winners"
queryFour = "can you summarize James Day's Report"
queryFive = "can you summarize question 6 for Ross Fellowship reports"
querySix = "question: 6, year: 2023, award: dean's graduate fellowship"
querySeven = "how many publications do the ross fellows have?"
results = collection.query(
    include=["documents", "metadatas", "distances"],
    query_texts=["question:2, award: Ross Fellowship"],
    n_results = 31
)
final = []

for doc in results['documents'][0]:
    index = doc.find("questionNumber")
    #print(doc)
    if (doc[index + 17] == "2" or doc[index + 16] == "2"):
        final.append(doc)
    #print(doc[index + 17])
print(results["distances"])
print(len(final))
for doc in final:
    print(doc)
#data = [json.loads(entry) for entry in results['documents'][0]]
#print(data)

output = ollama.generate(
    model = "llama3.1:8b",
    prompt = f"""
    {context}
    Here is the user's question: {querySeven}
    Here are the relevant documents pulled from the database: {final}
    """
 )

print(output['response'])



