import chainlit as cl
from rag_pipeline import get_rag_chain, get_semantic_answer, get_specific_project_details

# GLOBAL CHAIN LOAD KAR LEIN (Is se session error khatam ho jayega)
rag_chain = get_rag_chain()

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="👋 Welcome! I am Hammas's AI Assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Ab session.get() ki zaroorat nahi, direct global variable use karein
    msg = cl.Message(content="Thinking... 🔄")
    await msg.send()
    
    try:
        # Pass the global rag_chain here
        answer = get_semantic_answer(rag_chain, message.content)
        msg.content = answer
        await msg.update()
    except Exception as e:
        msg.content = f"⚠️ Error: {str(e)}"
        await msg.update()