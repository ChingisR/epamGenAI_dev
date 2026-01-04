import streamlit as st
import requests
import os

# 1. Configuration
# We get the API URL from Docker environment variables, or default to localhost for testing
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG Resume Assistant", layout="centered")
st.title("🤖 Resume Search Assistant")

# 2. Sidebar - Upload Section
with st.sidebar:
    st.header("Upload New CVs")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Upload & Process"):
            with st.spinner("Reading PDF..."):
                # Prepare the file to send to the Backend API
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload-pdf", files=files)
                    
                    # --- IMPROVED ERROR HANDLING ---
                    if response.status_code == 200:
                        # Parse the JSON to check if it's a real success or a handled error
                        data = response.json()
                        if data.get("status") == "success":
                            st.success("Success! File added to knowledge base.")
                        else:
                            # Display the specific error message from the backend
                            error_msg = data.get("message", "Unknown error occurred.")
                            st.error(f"Backend Error: {error_msg}")
                    else:
                        st.error(f"HTTP Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

# 3. Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about candidates (e.g., 'Who knows Python?')..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get answer from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Send question to FastAPI backend
                response = requests.post(f"{API_URL}/query", json={"query": prompt})
                
                if response.status_code == 200:
                    answer = response.json().get("response", "No response found.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Server Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error. Is the backend running? {e}")