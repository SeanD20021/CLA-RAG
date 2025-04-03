import nltk
from nltk.tokenize import sent_tokenize

def sentence_chunking(text, maxTokens=256, overlap_percent=10):
  sentences = sent_tokenize(text)
    
  chunks = []
  current_chunk = []
  current_length = 0
  overlap_size = int((overlap_percent / 100) * maxTokens)
    
  for sentence in sentences:
      sentence_length = len(sentence.split())  # Estimate token count using words
        
      if current_length + sentence_length > maxTokens:
          if current_chunk:
                chunks.append(" ".join(current_chunk))
            
          # Start new chunk with overlap
          overlap = current_chunk[-overlap_size:] if overlap_size > 0 else []
          current_chunk = overlap + [sentence]
          current_length = sum(len(s.split()) for s in current_chunk)
      else:
          current_chunk.append(sentence)
          current_length += sentence_length
  # Add the last chunk
  if current_chunk:
      chunks.append(" ".join(current_chunk))
  return chunks

def text_chunker(text, path):
    sentences = text.split('.')
    chunks = []
    #chunks will be ~1000
    current_chunk = ''
    prev_sentences = []

    for s in sentences:
        #print(s)
        #print("END\n\n\n\n")
        #print(current_chunk)
        if len(current_chunk) == 0:
            current_chunk = s + '.'
        elif len(current_chunk) + len(s) > 1000:
            final_chunk = path + '\n' + current_chunk
            #final_chunk =  current_chunk
            chunks.append(final_chunk)
            current_chunk = ''
            for p in prev_sentences[::-1]:
                #print(p)
                if len(current_chunk) == 0:
                    if len(p) > 200:
                        current_chunk = s + '.'
                        break
                    else:
                        current_chunk = p
                else:
                    if len(current_chunk) + len(p) <= 200:
                        current_chunk = p + '.' + current_chunk
                    else:
                        current_chunk = current_chunk + s + '.'
                        #print("happens\n\n")
                        #print(current_chunk)
                        break
        else:
            current_chunk = current_chunk + s + '.'

        if len(prev_sentences) < 5:
            prev_sentences.append(s)
        else:
            prev_sentences.pop(0)
            prev_sentences.append(s)
    current_chunk = path + "\n" + current_chunk
    #current_chunk = current_chunk
    chunks.append(current_chunk)
    return chunks


