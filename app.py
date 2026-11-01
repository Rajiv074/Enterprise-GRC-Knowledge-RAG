import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/chat/invoke"

# Streamlit page configuration
st.set_page_config(
    page_title="LLM Chat App",
    page_icon="😈"
)

# App title
st.title("😈 LLM Chat App")
st.write("Ask anything to your FastAPI-powered LLM")

# User input
question = st.text_input("Enter your question:")

# Ask button
if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Request payload
                payload = {
                    "input": {
                        "question": question
                    }
                }

                # Call FastAPI endpoint
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()

                # Parse response
                result = response.json()

                # Extract LLM response
                output = result.get("output", {})
                answer = output.get("content", "No response received.")

                # Display response
                st.success("Response:")
                st.write(answer)

            except Exception as e:
                st.error(f"Error: {e}")