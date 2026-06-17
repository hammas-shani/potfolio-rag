import chainlit as cl
from rag_pipeline import get_rag_chain, get_semantic_answer, get_specific_project_details
from langchain_core.messages import HumanMessage, AIMessage

@cl.on_chat_start
async def start_chat():
    # Chat History Array initialize karein
    cl.user_session.set("chat_history", [])
    
    # Chain setup aur session me save (Ab har user ka apna session hoga)
    rag_chain = get_rag_chain()
    cl.user_session.set("rag_chain", rag_chain)
    
    await cl.Message(content="👋 Welcome! I am Hammas's AI Assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    
    # Session se chain nikalain, agar None ho to naya load karein
    chain = cl.user_session.get("rag_chain")
    if not chain:
        chain = get_rag_chain()
        cl.user_session.set("rag_chain", chain)
        
    chat_history = cl.user_session.get("chat_history", []) # Default empty list agar session clear ho
    
    msg = cl.Message(content="Thinking... 🔄")
    await msg.send()
    
    try:
        # History ke sath answer fetch karein
        answer = get_semantic_answer(chain, user_input, chat_history)
        msg.content = answer
        await msg.update()
        
        # Naya sawal aur jawab history mein save karein
        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=answer)
        ])
        cl.user_session.set("chat_history", chat_history)
        
    except Exception as e:
        msg.content = f"⚠️ Error: {str(e)}"
        await msg.update()
