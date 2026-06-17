import os
from pathlib import Path
from dotenv import load_dotenv

# --- Imports ---
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Sahi Loaders Import Kiye Gaye Hain
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Environment Variables
load_dotenv()

# Constants
CHROMA_PATH = "vector_db"
CACHE_PATH = "semantic_cache_db" # 🟢 Cache Path Add Kar Diya Hai
DATA_PATH = "dataset"

# Embeddings Function
def get_embeddings_function():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Vector DB Builder
def build_vector_db():
    if os.path.exists(CHROMA_PATH):
        print(f"🔄 Loading existing Vector DB from {CHROMA_PATH}...")
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings_function())
    
    print("📁 Loading documents from data folder...")
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"⚠️ '{DATA_PATH}' folder nahi mila. Please create karein aur files dalein.")
        return None

    # --- Sahi Loader Logic (Error Free) ---
    pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()

    md_loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader)
    md_docs = md_loader.load()

    documents = pdf_docs + md_docs
    
    if not documents:
        print("⚠️ Koi documents nahi mile. Empty DB return kar raha hoon.")
        return None

    print(f"📄 Processing {len(documents)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    print(f"💾 Saving {len(chunks)} chunks to Chroma DB...")
    db = Chroma.from_documents(chunks, get_embeddings_function(), persist_directory=CHROMA_PATH)
    return db

# RAG Chain Setup
def get_rag_chain():
    embeddings = get_embeddings_function()
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant", 
        temperature=0.0  # Strict constraints
    )

    # Memory Prompt
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # Strict System Prompt + Emergency Code Stop
    system_prompt = (
        "You are the exclusive AI Assistant for Hammas Shahzad Shani, an AI/ML Engineer. "
        "Your objective is to provide precise, professional, and context-grounded information regarding Hammas Shahzad Shani's professional profile, experience, projects, skills, certifications, education, achievements, and work. "
        "\n\n"
        "STRICT LANGUAGE MIRRORING RULES:\n"
        "- If the user asks in English, you MUST respond in professional English. DO NOT mix Urdu words.\n"
        "- If the user asks in Roman Urdu, you MUST respond in professional Pakistani Roman Urdu. DO NOT use English sentences.\n"
        "- Use natural Pakistani Roman Urdu vocabulary.\n"
        "- Avoid Hindi words such as 'upyog', 'anusaar', 'kaushal', and 'prayog'.\n"
        "- Prefer words such as 'istemaal', 'mutabiq', 'maharat', and 'tajurba'.\n"
        "- Do not explain your language choice. Simply mirror the user's language.\n"
        "\n\n"
        "CRITICAL BEHAVIORAL RULES:\n"
        "1. IDENTITY LOCK (HIGHEST PRIORITY): You are NOT a general-purpose AI assistant.\n"
        "   - You must ONLY answer questions directly related to Hammas Shahzad Shani and the provided CONTEXT.\n"
        "   - If a user asks about general knowledge, mathematics, coding problems, technology explanations, current events, opinions, greetings, or anything unrelated to Hammas Shahzad Shani, immediately refuse.\n"
        "   - Refusal (English): 'I can only assist with information related to Hammas Shahzad Shani and his professional work.'\n"
        "   - Refusal (Roman Urdu): 'Main sirf Hammas Shahzad Shani aur unke professional kaam ke baare mein maloomat de sakta hoon.'\n"
        "\n"
        "2. CONTEXT-ONLY POLICY:\n"
        "   - ONLY use information explicitly available in the provided CONTEXT.\n"
        "   - Never use external knowledge.\n"
        "   - Never make assumptions.\n"
        "   - Never infer missing information.\n"
        "   - Never fabricate projects, experience, skills, achievements, education, timelines, or personal information.\n"
        "\n"
        "3. NO HALLUCINATION:\n"
        "   - If information is not present in the CONTEXT, immediately return the appropriate refusal message.\n"
        "   - Do not guess.\n"
        "\n"
        "4. NO GENERAL TECHNOLOGY EXPLANATIONS:\n"
        "   - Never explain technologies such as FastAPI, LangChain, YOLO, TensorFlow, Python, or any other technology in general.\n"
        "   - You may only explain how Hammas Shahzad Shani used a technology in a project explicitly mentioned in the CONTEXT.\n"
        "\n\n"
        "TONE & STYLE:\n"
        "- Maintain a professional, business-oriented, and concise tone.\n"
        "- Be factual and direct.\n"
        "- Avoid greetings, filler phrases, small talk, and unnecessary explanations.\n"
        "- Keep responses focused only on the user's question and the available CONTEXT.\n"
        "\n\n"
        "FINAL VALIDATION AND EMERGENCY STOP (CRITICAL):\n"
        "Before you output anything, run this internal check:\n"
        "1. Does the user's prompt ask for code, scripts, algorithms (like TwoSum, Fibonacci), or programming help?\n"
        "2. Does your planned response contain ANY code block (e.g., ```python), functions, syntax, or pseudo-code?\n"
        "IF YES TO EITHER: YOU MUST IMMEDIATELY ABORT. DO NOT explain anything. DO NOT apologize. JUST output exactly this sentence and nothing else:\n"
        "Refusal: 'Main sirf Hammas Shahzad Shani ke professional background aur projects ke baare mein maloomat de sakta hoon. Main programming code generate nahi kar sakta.'\n"
        "3. Does the planned response contain information outside the CONTEXT? If YES, use the standard refusal.\n"
        "\n\n"
        "Context:\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain

# --- 🧠 SMART SEMANTIC CACHE LOGIC ---
def get_semantic_answer(rag_chain, user_input, chat_history=[], threshold=0.4):
    embeddings = get_embeddings_function()
    semantic_cache = Chroma(persist_directory=CACHE_PATH, embedding_function=embeddings)
    
    # RULE: Cache sirf tab check karein jab chat_history khali ho (Pehla sawal ho)
    # Taake "us k ilawa" jaise follow-up questions puranay cache se galat jawab na uthayen.
    if not chat_history:
        results = semantic_cache.similarity_search_with_score(user_input, k=1)
        if results:
            best_match, distance = results[0]
            if distance < threshold:
                print(f"\n🟢 CACHE HIT! Score: {distance:.4f} - Fetching instantly from DB...")
                return best_match.metadata["answer"]

    # Agar Cache mein nahi hai ya Chat History mojood hai, toh Groq API hit karein
    print("\n🔴 CACHE MISS! Hitting Groq API with context & memory...")
    response = rag_chain.invoke({
        "input": user_input, 
        "chat_history": chat_history
    })
    answer = response["answer"]

    # RULE: Naya jawab cache mein sirf tab save karein jab yeh standalone sawal ho
    if not chat_history:
        semantic_cache.add_texts(
            texts=[user_input], 
            metadatas=[{"answer": answer}]
        )
    
    return answer

# Verification Block
if __name__ == "__main__":
    db = build_vector_db()
    if db:
        print("\n✅ System is Operational.")
        chain = get_rag_chain()
        
        test_q = "Hi, Who is Hammas?"
        print(f"\n👤 User: {test_q}")
        test_response = get_semantic_answer(chain, test_q, [])
        print(f"🤖 AI Test: {test_response}")