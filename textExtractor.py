#This file contains text extraction functions for different file types
import fitz
from docx import Document
import pandas



#PDF
def pdf_to_text(filename):
    doc = fitz.open(filename)
    #text = filename + "\n"
    text = ''
    for num in range(len(doc)):
        page = doc[num]
        text += page.get_text()
    return text


#Word doc
def word_to_text(filename):
    doc = Document(filename)
    text = filename + "\n".join([para.text for para in doc.paragraphs])
    
    return text

#Excel doc
def excel_to_text(filename):
    text = filename + "\n"
    sheets = pandas.read_excel(filename, sheet_name=None, engine="openpyxl")

    for sheet_name, df in sheets.items():
        text += f"\nSheet: {sheet_name}\n"
        text += df.to_string(index=False) + "\n"
    return text

#text file

def text_to_text(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return filename + "\n" + file.read()