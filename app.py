import streamlit as st
from inference import ask_model

# Page title
st.set_page_config(page_title="E-Commerce AI Assistant")

st.title("🛒 E-Commerce AI Assistant")

st.write("Ask questions about orders, returns, delivery, and policies.")

# User input
question = st.text_input("Enter your question")

# Button to ask the model
if st.button("Ask AI"):
    
    if question.strip() != "":
        
        with st.spinner("Generating answer..."):
            answer = ask_model(question)

        st.subheader("AI Answer")
        st.write(answer)

    else:
        st.warning("Please enter a question.")