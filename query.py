import chromadb
import ollama
from embeddingfunction import EmbeddingFunction

#print(ollama.show("llama3.2"))
embedding_function = EmbeddingFunction()

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_collection(name="my_collection", embedding_function=embedding_function)

queryOne = "what fellowship is Noah Mckay apart of?"
queryTwo = "who wrote a report for the bisland fellowship in 2024"
queryThree = "\ngive me the names of the people who wrote an deans graduate fellowship report (dgf) in 2023"
queryFour = "\nplease list the total amount of publications submitted from the reports and the names of the people who published them"
queryFive = "please summarize the 2023 - dgf - Meier, Savannah report in two paragraphs"
context = """
I have created a vector database containing chunks of reports from various University faculty about the fellowship they're in and what they've accomplished with the support it has provided them.
The report includes 6 parts:
1.A brief description of the main learning or research projects you worked on
2.A list of any papers in preparation, submitted for review, or published
3.A list of any professional development activities attended
4.A candid evaluation of any mentoring and advising you have received so far
5.If warranted, a list of grant proposals in preparation, submitted for review, or awarded specifying the sponsoring organization, your role (PI, Co-PI, etc.), funds requested, and performance period.
6.Any other comments or suggestions for the program
If an answer can't be found in the documents provided, say so.
Also there may be other names mentioned in the report but the author of the report is listed in the filename in the first line.
The first line of the report chunks and the file name meta data provide important information. seperated by "-" they provide the year of the report, the award/fellowship, the school the faculty belongs to, and the faculty's name in that order.
The embeddings provided were created using the llama3.1 model so you should be able to interpret their meaning
"""


results = collection.query(
    include=["documents", "metadatas", "distances"],
    query_texts=[queryThree],
    n_results = 1
)

#print(results)
#print(results)
#print(results)
#print(results['metadatas'][0][0])
data = ""
for i, doc in enumerate(results['metadatas'][0]):
    data = data + f"""
filename: {doc["filename"]}
chunk number: {doc["chunkNumber"]}
data: {results['documents'][0][i]}
"""
    #embeddings: {results['embeddings'][0][i]}
#data = "\n\n\ndoc excerpt:\n".join(results['documents'][0])

print(data)
#print(results["documents"])
#print(data)
#for doc in results['documents'][0]:
#    print(doc[:50])
print(results["distances"])
#print(data)
#print(results['documents'][0])+
#print(results['documents'])



output = ollama.generate(
    model = "llama3.1:8b",
    prompt = f"""
    {context}
    Here is the user's question: {queryThree}
    Here are the data chunks from the database and their associated meta data: {data}
    """
)

print(output['response'])

#Using this list of data pulled from a vector database : {data} respond to this prompt: {queryThree}