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
        if file_path.is_file() and file_path.suffix in ['.txt', '.md']:
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
        chunk_size=400, 
        chunk_overlap=50 
    )
    chunks = text_splitter.split_documents(docs)

    print("Generating Vector Embeddings and compiling ChromaDB...")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    print("✅ Vector DB Compiled Successfully!")
    return vector_db

def get_rag_chain():
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant", 
        temperature=0.3 
    )

    system_prompt = (
       "You are an AI Assistant for Hammas Shahzad Shani, an expert AI/ML Engineer.\n"
        "Use the following retrieved context to answer the user's questions about Hammas.\n"
        "CRITICAL LANGUAGE RULE:\n"
        "- If the user asks a question in English, you MUST reply entirely in professional English.\n"
        "- If the user asks a question in Roman Urdu, you MUST reply entirely in Roman Urdu.\n"
        "- Do NOT mix English and Roman Urdu in the same response.\n"
        "If the answer is not in the context, simply say you don't have that information. Do not invent facts.\n"
        "\nContext: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)

def get_semantic_answer(rag_chain, user_input, threshold=0.3):
    semantic_cache = Chroma(persist_directory=CACHE_PATH, embedding_function=embeddings)
    results = semantic_cache.similarity_search_with_score(user_input, k=1)
    
    if results and results[0][1] < threshold:
        print(f"🟢 CACHE HIT! Distance factor: {results[0][1]}")
        return results[0][0].metadata["answer"]

    print("🔴 CACHE MISS! Fetching live stream from Groq API...")
    response = rag_chain.invoke({"input": user_input})
    answer = response["answer"]

    semantic_cache.add_texts(texts=[user_input], metadatas=[{"answer": answer}])
    return answer

if __name__ == "__main__":
    db = build_vector_db()
    if db:
        print("\nVerifying operational integrity...")
        chain = get_rag_chain()
        test_response = get_semantic_answer(chain, "Hi, Who is Hammas?")
        print(f"\nPipeline Test Response: {test_response}")
