import streamlit as st
import requests
import os

# --- CONFIGURATION ---
# Default to environment variable, but allow sidebar override if needed
DEFAULT_API_URL = os.getenv("API_URL", "http://fastapi-app:8000")

st.set_page_config(
    page_title="Resume Matcher", 
    page_icon="🤖", 
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: CONFIG & UPLOAD ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", value=DEFAULT_API_URL, help="URL of the backend FastAPI service")

    st.divider()
    
    st.header("📂 Upload CV")
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=["pdf"], 
        accept_multiple_files=False
    )
    
    if uploaded_file:
        if st.button("Process Resume", type="primary"):
            with st.spinner("Uploading & Indexing..."):
                try:
                    files_payload = {
                        "file": (uploaded_file.name, uploaded_file, "application/pdf")
                    }
                    
                    response = requests.post(
                        f"{api_url}/upload-pdf", 
                        files=files_payload, 
                        timeout=360
                    )
                    
                    if response.status_code == 200:
                        st.success(f"✅ Indexed: {uploaded_file.name}")
                        # Optional: Clear the uploader after success (requires a key hack or st.form, skipping for simplicity)
                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to Backend. Check your Docker network.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 Resume Search Assistant")
st.caption("Ask questions about the uploaded candidates (e.g., 'Who has experience with Python?')")

# 1. Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle user input
if prompt := st.chat_input("Ask a question about the candidates..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Get response from API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Analyzing resumes..."):
            try:
                response = requests.post(
                    f"{api_url}/query", 
                    json={"query": prompt}, 
                    timeout=360
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "No response found.")
                    
                    # Display the answer
                    message_placeholder.markdown(answer)
                    full_response = answer
                    
                    # Optional: If your backend returns "source_documents", you can display them in an expander
                    if "source_documents" in data:
                        with st.expander("View Source Context"):
                            st.json(data["source_documents"])
                            
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    message_placeholder.error(error_msg)
                    full_response = error_msg

            except requests.exceptions.ConnectionError:
                error_msg = "❌ Connection refused. Is the backend running?"
                message_placeholder.error(error_msg)
                full_response = error_msg
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                message_placeholder.error(error_msg)
                full_response = error_msg

    # 4. Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})