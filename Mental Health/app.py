import streamlit as st
import requests

# Set the URL of your running FastAPI server
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("AI-Powered Mental Health Chatbot")

# Create a text input for the user's query
user_query = st.text_input("Enter your message:")

# Create a button to send the request
if st.button("Send"):
    if user_query:
        # Send a POST request to the /chat endpoint
        response = requests.post(
            f"{FASTAPI_URL}/chat", 
            json={"session_id": "user_session", "query": user_query}
        )
        
        # Display the response from the FastAPI backend
        if response.status_code == 200:
            st.write(f"Chatbot: {response.json()['response']}")
        else:
            st.error("Error communicating with the chatbot.")