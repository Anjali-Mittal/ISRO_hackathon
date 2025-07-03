import gradio as gr
from backend import ask_kg

# Memory to store chat history
chat_history = []

def chat_interface(user_message, history):
    cypher, answer = ask_kg(user_message)

    # Add user's question and bot's answer to chat history
    history = history or []
    history.append((user_message, answer))
    return history, history  # (chatbot display, updated state)

with gr.Blocks() as demo:
    gr.Markdown("ISRO Knowledge Assistant")

    chatbot = gr.Chatbot(label="Chat with ISRO Bot")
    msg = gr.Textbox(label="Enter your question...", placeholder="e.g. When was Mangalyaan launched?")
    state = gr.State([])

    msg.submit(chat_interface, [msg, state], [chatbot, state])
    msg.submit(lambda: "", None, msg)  # Clear input after submission

demo.launch(share=True)