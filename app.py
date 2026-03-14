import streamlit as st
import os
import yaml
from pathlib import Path
from src.ingestion.pdf_parser import extract_text_from_pdf
from src.ingestion.chunker import chunk_text
from src.ingestion.preprocessor import preprocess_pages
from src.embeddings.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import Retriever
from src.generation.prompt_builder import build_prompt, build_summary_prompt
from src.generation.llm_handler import LLMHandler
from src.utils.helpers import load_config, ensure_directories

# Load config
cfg = load_config()
ensure_directories()

VECTOR_PATH = cfg["vectorstore"]["path"]

st.set_page_config(
    page_title="Research RAG Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Research Paper RAG Assistant")
st.markdown("Upload research papers and ask questions grounded in their content.")

# Initialize models
def load_models():
    embedder = Embedder(cfg["embedding"]["model"])
    store = VectorStore()
    if Path(f"{VECTOR_PATH}.faiss").exists():
        store.load(VECTOR_PATH)
    retriever = Retriever(embedder, store)
    llm = LLMHandler(
        model=cfg["llm"]["model"],
        max_tokens=cfg["llm"]["max_tokens"],
        temperature=cfg["llm"]["temperature"]
    )
    return embedder, store, retriever, llm

embedder, store, retriever, llm = load_models()

# Sidebar
with st.sidebar:
    st.header("📁 Upload Research Papers")
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("📥 Index Papers", type="primary") and uploaded_files:
        os.makedirs("data/raw_pdfs", exist_ok=True)
        all_chunks = []
        progress = st.progress(0)
        status = st.empty()

        for i, file in enumerate(uploaded_files):
            status.text(f"Processing: {file.name}")
            path = f"data/raw_pdfs/{file.name}"
            with open(path, "wb") as f:
                f.write(file.read())

            pages = extract_text_from_pdf(path)
            pages = preprocess_pages(pages)
            chunks = chunk_text(
                pages,
                chunk_size=cfg["chunking"]["chunk_size"],
                overlap=cfg["chunking"]["chunk_overlap"]
            )
            all_chunks.extend(chunks)
            progress.progress((i + 1) / len(uploaded_files))

        status.text("Generating embeddings...")
        texts = [c["text"] for c in all_chunks]
        embeddings = embedder.embed(texts, cfg["embedding"]["batch_size"])
        store.add(embeddings, all_chunks)
        store.save(VECTOR_PATH)

        progress.progress(1.0)
        status.text("Done!")
        st.success(f"Indexed {len(all_chunks)} chunks from {len(uploaded_files)} papers!")

    st.divider()
    st.header("📊 Index Status")
    if store.is_empty():
        st.warning("No papers indexed yet.")
    else:
        st.success(f"{store.index.ntotal} chunks indexed")

# Main area
tab1, tab2 = st.tabs(["🔍 Ask a Question", "📋 Summarize Paper"])

# Tab 1: Q&A
with tab1:
    st.subheader("Ask anything about your research papers")
    query = st.text_input(
        "Your Question:",
        placeholder="What methodology does this paper use?"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        top_k = st.slider("Top-K chunks", 1, 10, cfg["retrieval"]["top_k"])
            # Around line 78-79, just before store.add(...)
        print("Embedding shape:", embeddings.shape)
        print("FAISS index dimension:", store.index.d)
    if st.button("🔍 Get Answer", type="primary") and query:
        if store.is_empty():
            st.error("Please upload and index papers first.")
        else:
            with st.spinner("Retrieving and generating answer..."):
                results = retriever.retrieve(query, top_k=top_k)
                prompt = build_prompt(query, results)
                answer = llm.generate(prompt)

            st.subheader("💡 Answer")
            st.write(answer)

            st.subheader("📚 Retrieved Sources")
            for i, chunk in enumerate(results, 1):
                with st.expander(
                    f"[{i}] {chunk['source']} | Page {chunk['page']} | Score: {chunk['score']:.3f}"
                ):
                    st.write(chunk["text"])

# Tab 2: Summarize
with tab2:
    st.subheader("Summarize a specific paper")
    if store.is_empty():
        st.warning("Please upload and index papers first.")
    else:
        papers = list(set([m["source"] for m in store.metadata]))
        selected_paper = st.selectbox("Select a paper:", papers)

        if st.button("📋 Summarize", type="primary") and selected_paper:
            with st.spinner("Summarizing..."):
                paper_chunks = [m for m in store.metadata if m["source"] == selected_paper]
                paper_chunks = paper_chunks[:10]
                prompt = build_summary_prompt(paper_chunks, selected_paper)
                summary = llm.generate(prompt)

            st.subheader(f"Summary: {selected_paper}")
            st.write(summary)
