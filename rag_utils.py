import os
import ssl
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

# Bypass SSL for college/lab network security
ssl._create_default_https_context = ssl._create_unverified_context

def process_pdf_to_db(uploaded_files, api_key):
    os.environ["GOOGLE_API_KEY"] = api_key
    all_chunks = []

    # 1. Extract Text
    for file in uploaded_files:
        reader = PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # 2. Chunking (Task 3)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        all_chunks.extend(splitter.create_documents([text]))

    # 3. Task 7: Persistence (Save to local folder)
    # Using the stable gemini-embedding-001 model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"  # This creates the folder on your desktop
    )
    return vector_db

def get_answer(vector_db, question, api_key):
    os.environ["GOOGLE_API_KEY"] = api_key
    # Task 4 & 5: Similarity Search
    docs = vector_db.similarity_search(question, k=3)
    
    if docs:
        context = "\n".join([d.page_content for d in docs])
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        response = llm.invoke(f"Context: {context}\n\nQuestion: {question}")
        return response.content
    return "I could not find relevant information in the documents."