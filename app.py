import chainlit as cl
from rag_pipeline import get_rag_chain, get_semantic_answer

@cl.on_chat_start
async def start_chat():
    # RAG chain ko load kar ke session mein store kar rahe hain
    chain = get_rag_chain()
    cl.user_session.set("rag_chain", chain)

    # Apka Professional Welcome Message
    await cl.Message(
        content="Hi, my name is Hammas Shahzad Shani. I am an AI Engineer. How can I help you?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("rag_chain")
    
    msg = cl.Message(content="Thinking... 🤔")
    await msg.send()
    
    try:
        # Semantic Cache aur LLM se answer lana
        answer = get_semantic_answer(chain, message.content)
        
        msg.content = answer
        await msg.update()
        
    except Exception as e:
        msg.content = f"⚠️ Maaf kijiyega, ek error aagaya: {str(e)}"
        await msg.update()