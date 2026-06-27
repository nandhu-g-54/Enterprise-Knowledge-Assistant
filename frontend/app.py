import streamlit as st
import requests

# Backend API
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    layout="wide"
)

# Title
st.title("📚 Enterprise Knowledge Assistant")
st.markdown("Ask questions from your internal company documents")

# Sidebar - Upload PDF
st.sidebar.header("📂 Document Management")

uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:

    if st.sidebar.button("Upload Document"):

        files = {"file": uploaded_file.getvalue()}

        response = requests.post(
            f"{BASE_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )

        if response.status_code == 200:
            st.sidebar.success("Uploaded successfully")
        else:
            st.sidebar.error("Upload failed")
            st.sidebar.write(response.text)

# Reindex button
if st.sidebar.button("🔄 Reindex Knowledge Base"):

    response = requests.post(f"{BASE_URL}/reindex")

    if response.status_code == 200:
        st.sidebar.success("Reindex completed")
    else:
        st.sidebar.error("Reindex failed")
        st.sidebar.write(response.text)

st.sidebar.markdown("---")

# Main input
question = st.text_input("💬 Ask a question from your documents:")

col1, col2 = st.columns([1, 4])

with col1:
    ask_btn = st.button("Ask")

if ask_btn:

    if question.strip() == "":
        st.warning("Please enter a question")

    else:
        with st.spinner("Searching documents and generating answer..."):

            try:
                response = requests.post(
                    f"{BASE_URL}/ask",
                    json={"question": question}
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Answer Generated")

                    # Answer
                    st.subheader("🧠 Answer")
                    st.write(data["answer"])

                    # Confidence
                    st.subheader("📊 Confidence Score")
                    st.progress(float(data["confidence"]))
                    st.write(data["confidence"])

                    # Sources
                    st.subheader("📄 Sources")

                    if data["sources"]:
                        for src in data["sources"]:
                            st.markdown(
                                f"📌 **{src['document']}** — Page {src['page']}"
                            )
                    else:
                        st.warning("No sources found")

                else:
                    st.error("Backend error")
                    st.write(response.text)

            except Exception as e:
                st.error("Request failed")
                st.write(str(e))

# Footer
st.markdown("---")
st.markdown("🚀 Enterprise RAG System | Built with FastAPI + ChromaDB + LangChain")