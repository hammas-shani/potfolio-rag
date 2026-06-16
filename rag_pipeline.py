import os
from pathlib import Path
from dotenv import load_dotenv

# Standard Document Object & Text Splitters (Zero dependency loaders)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Modern Standalone Vector Store & Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma  

# Native LLM Framework Components
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =========================================================================
# FIXED: v1.0+ Updates Ke Mutabiq Classic Packaging Import Patterns
# =========================================================================
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

# Project Directories Configuration
DATASET_DIR = "dataset"
CHROMA_PATH = "vector_db"
CACHE_PATH = "semantic_cache_db"

# Embeddings Core Instance
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_db():
    print("Reading data from dataset folder natively...")
    docs = []
    dataset_path = Path(DATASET_DIR)
    
    if not dataset_path.exists():
        os.makedirs(DATASET_DIR)
        print(f"⚠️ '{DATASET_DIR}' directory created. Put your text resume files here!")
        return None

    # Native Python file scanning to avoid community deprecations
    for file_path in dataset_path.rglob("*.*"):
        if file_path.is_file() and file_path.suffix in ['.txt', '.md' , '.json']:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    docs.append(Document(page_content=content, metadata={"source": str(file_path)}))
            except Exception as e:
                print(f"Error parsing file {file_path}: {e}")

    if not docs:
        print("❌ Dataset folder is empty! Please add files to parse.")
        return None

    print(f"Successfully processed {len(docs)} document(s). Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "], 
        chunk_size=2000,
        chunk_overlap=400
    )
    chunks = text_splitter.split_documents(docs)

    print("Generating Vector Embeddings and compiling ChromaDB...")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    print("✅ Vector DB Compiled Successfully!")
    return vector_db

def get_rag_chain():
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant", 
        temperature=0.3 
    )

system_prompt = (
    "You are the exclusive AI Assistant for Hammas Shahzad Shani, an AI/ML Engineer. "
    "Your objective is to provide precise information from the CONTEXT regarding Hammas's professional profile, projects, and skills. "
    "\n\n"
    "STRICT LANGUAGE MIRRORING RULES:\n"
    "- If the user asks in English, you MUST respond in professional English. DO NOT mix any Urdu words.\n"
    "- If the user asks in Roman Urdu, you MUST respond in professional Pakistani Roman Urdu. DO NOT use any English sentences.\n"
    "- Do not explain your language choice. Simply mirror the user's language.\n"
    "\n\n"
    "CRITICAL BEHAVIORAL RULES:\n"
    "1. IDENTITY LOCK: You are NOT a general-purpose AI. If a user asks questions unrelated to Hammas Shahzad Shani (e.g., math, general knowledge, coding, 'how are you'), you must immediately decline.\n"
    "   - Refusal (English): 'I can only assist with information related to Hammas Shahzad Shani and his professional work.'\n"
    "   - Refusal (Roman Urdu): 'Main sirf Hammas Shahzad Shani aur unke professional kaam ke baare mein maloomat de sakta hoon.'\n"
    "2. NO HALLUCINATION: ONLY state facts explicitly present in the provided CONTEXT. If the answer is not in the context, use the exact refusal phrases defined above.\n"
    "3. NO GENERAL KNOWLEDGE: Never define technologies (e.g., 'What is FastAPI') unless it is directly explaining Hammas's specific project implementation.\n"
    "\n\n"
    "TONE & STYLE:\n"
    "- Maintain a businesslike, concise, and professional tone.\n"
    "- Avoid filler phrases ('Welcome', 'Hope you are doing well', etc.).\n"
    "- Use Pakistani Roman Urdu (e.g., 'istemaal', 'skills') and strictly avoid Hindi vocabulary (e.g., 'upyog', 'kaushal').\n"
    "\n\n"
    "CONTACT PROTOCOL:\n"
    "- Only provide Hammas's WhatsApp (03111809562) if the user specifically asks for contact info or if you have failed to answer a question regarding his background.\n"
    "\n\n"
    "Context:\n{context}"
)
    
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)

# --- 🧠 CUSTOM SEMANTIC CACHE LOGIC (SQLite Powered) ---
def get_semantic_answer(rag_chain, user_input, threshold=0.7):
    semantic_cache = Chroma(persist_directory=CACHE_PATH, embedding_function=embeddings)
    
    # 1. Search
    results = semantic_cache.similarity_search_with_score(user_input, k=6)
    
    if results:
        best_match, distance = results[0]
        if distance < threshold:
            print(f"🟢 CACHE HIT! Score: {distance}")
            return best_match.metadata["answer"]

    # 2. Miss -> Invoke Chain
    print("🔴 CACHE MISS! Hitting Groq API...")
    response = rag_chain.invoke({"input": user_input})
    answer = response["answer"]

    # 3. Save & Persist (Important step for permanent cache)
    semantic_cache.add_texts(texts=[user_input], metadatas=[{"answer": answer}])
    # Chroma DB ko save karne ke liye persist karna zaroori hai
    # Note: Modern Chroma versions mein persist automatic hota hai, 
    # lekin verify kar lein agar aapka version purana hai.
    
    return answer

def get_specific_project_details(project_name):
    # Vector DB se specific project search karein
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    # k=1 kyunke humein exact project chahiye
    results = vector_db.similarity_search(project_name, k=1)
    
    if results:
        return results[0].page_content
    return "Project details not found."    

if __name__ == "__main__":
    db = build_vector_db()
    if db:
        print("\nVerifying operational integrity...")
        chain = get_rag_chain()
        test_response = get_semantic_answer(chain, "Hi, Who is Hammas?")
        print(f"\nPipeline Test Response: {test_response}")



