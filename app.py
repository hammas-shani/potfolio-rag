import chainlit as cl
from rag_pipeline import get_rag_chain, get_semantic_answer
from langchain_core.messages import HumanMessage, AIMessage

# Constant: Kitni history yaad rakhni hai? (10 means last 5 questions and 5 answers)
MAX_HISTORY_LENGTH = 10 

@cl.on_chat_start
async def start_chat():
    # Chat History Array initialize karein
    cl.user_session.set("chat_history", [])
    
    # Chain setup aur session me save
    rag_chain = get_rag_chain()
    cl.user_session.set("rag_chain", rag_chain)
    
    await cl.Message(content="👋 Welcome! I am Hammas Shahzad Shani's Official AI Assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    
    # Session se chain nikalain, fallback logic ke sath
    chain = cl.user_session.get("rag_chain")
    if not chain:
        chain = get_rag_chain()
        cl.user_session.set("rag_chain", chain)
        
    chat_history = cl.user_session.get("chat_history", [])
    
    msg = cl.Message(content="Thinking... 🔄")
    await msg.send()
    
    try:
        # History ke sath answer fetch karein
        # Note: Agar get_semantic_answer synchronous hai, toh run_in_executor use karna behtar hota hai for async speed
        answer = get_semantic_answer(chain, user_input, chat_history)
        msg.content = answer
        await msg.update()
        
        # Naya sawal aur jawab history mein save karein
        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=answer)
        ])
        
        # --- NEW OPTIMIZATION: Keep only the most recent messages ---
        if len(chat_history) > MAX_HISTORY_LENGTH:
            chat_history = chat_history[-MAX_HISTORY_LENGTH:]
            
        cl.user_session.set("chat_history", chat_history)
        
    except Exception as e:
        msg.content = f"⚠️ Error: {str(e)}"
        await msg.update()