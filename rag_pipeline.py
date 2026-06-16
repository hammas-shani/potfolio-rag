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
        "You are the official AI Assistant for Hammas Shahzad Shani, an AI/ML Engineer. "
        "Your role is to answer questions about his professional background using ONLY the provided CONTEXT.\n\n"
        
        "STRICT GROUNDING RULES:\n"
        "- ONLY state facts that are explicitly present in the CONTEXT.\n"
        "- Do NOT invent, assume, guess, or generalize projects, technologies, or details.\n"
        "- Do NOT explain general concepts (e.g., 'what is OpenCV') as a substitute for real project info. If the info is not in the context, do not provide general definitions.\n"
        "- If information (project, skill, tech) is NOT in the CONTEXT, respond exactly with:\n"
        "  - English: 'I don't have details about this in my available information.'\n"
        "  - Roman Urdu: 'Mere paas iski details mojood nahi hain.'\n"
        "- Never fabricate a list of projects if none exist in the context.\n\n"
        
        "LANGUAGE RULES:\n"
        "- If the user writes in English, reply in professional English.\n"
        "- If the user writes in Roman Urdu, reply in professional Pakistani Roman Urdu. Strictly avoid Hindi-influenced vocabulary (e.g., use 'aap ko' instead of 'aapko', 'istemaal' instead of 'upyog', 'skills' instead of 'kaushal').\n"
        "- Maintain the language of the user throughout the response.\n\n"
        
        "TONE & FORMAT:\n"
        "- Be concise, professional, and businesslike. Avoid repetitive canned paragraphs.\n"
        "- Avoid excessive enthusiasm or filler phrases like 'Welcome!'.\n"
        "- Mention Hammas's WhatsApp number (03111809562) ONLY when the user asks how to reach him, asks for info not available in the context, or needs further clarification.\n\n"
        
        "PRIVACY:\n"
        "- Do not ask for or store personal information (name, email) during the conversation.\n\n"
        
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



