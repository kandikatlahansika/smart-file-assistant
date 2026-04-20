import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

# --- Configuration ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAAr5BtIRegqDBOUtJ8H1lK7mnbNCw-J9s"

st.set_page_config(page_title="Smart-File AI")
st.title("📂 Smart-File AI Assistant")

# --- Task 1: UI Setup ---
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], accept_multiple_files=True)
    process_btn = st.button("Process Files")

# --- Task 2 & 3: Processing & Storage ---
if process_btn and uploaded_files:
    all_chunks = []
    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        
        loader = PyPDFLoader(file.name) if file.name.endswith(".pdf") else TextLoader(file.name)
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        all_chunks.extend(text_splitter.split_documents(data))
        os.remove(file.name)

    # Store in ChromaDB (Task 7: Persistence)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    st.session_state.vector_db = Chroma.from_documents(
        documents=all_chunks, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    st.success("Files processed and saved!")

# --- Task 4, 5 & 6: Query, Citations & Fallback ---
if prompt := st.chat_input("Ask a question:"):
    st.chat_message("user").markdown(prompt)
    
    # Task 4: Retrieve relevant chunks
    if "vector_db" in st.session_state:
        docs = st.session_state.vector_db.similarity_search_with_relevance_scores(prompt, k=2)
        
        # Task 5 & 6 logic
        if docs: # If information is found
            context = "\n".join([d[0].page_content for d in docs])
            source = docs[0][0].metadata.get("source", "Unknown file")
            
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            response = llm.invoke(f"Context: {context}\n\nQuestion: {prompt}")
            st.chat_message("assistant").markdown(f"{response.content}\n\n*(Source: {source})*")
        else:
            # Fallback for document-specific questions (Rule 5)
            st.chat_message("assistant").markdown("I could not find this information in the uploaded files.")
    else:
        # Task 4: General AI Response if no files are uploaded
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        response = llm.invoke(prompt)
        st.chat_message("assistant").markdown(response.content)