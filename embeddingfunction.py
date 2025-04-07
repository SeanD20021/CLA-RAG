import ollama
import numpy as np

class EmbeddingFunction:
    def __call__(self, input):
        # Ensure input is a list (can be a list of strings)
        if isinstance(input, str):
            #print("happens")
            input = [input]  # Make it a list if it's a single string
        embeddings = []
        for text in input:
            response = ollama.embed(model="nomic-embed-text", input=text)
            embeddings.append(response["embeddings"][0])
        return np.array(embeddings)
    
    #mxbai-embed-large