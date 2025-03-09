import PyPDF2
from docx import Document
import os
from sentence_transformers import util
import streamlit as st

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ' '.join([page.extract_text() for page in reader.pages])
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ' '.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format")
    return text



def chunk_text(text, chunk_size=256, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def search(query, top_k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]


st.title("Semantic Textbook Search")
uploaded_file = st.file_uploader("Upload a textbook (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    index_document(file_path)
    st.success("File indexed successfully!")

query = st.text_input("Enter your search query:")
if query:
    results = search(query)
    st.subheader("Top Results:")
    for i, res in enumerate(results):
        st.write(f"{i+1}. {res}")