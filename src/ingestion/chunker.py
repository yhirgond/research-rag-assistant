from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(pages: list, chunk_size: int = 600, overlap: int = 100) -> list:
    """
    Split pages into overlapping chunks using LangChain's
    RecursiveCharacterTextSplitter (sliding window approach).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for page in pages:
        splits = splitter.split_text(page["text"])

        for chunk_id, split in enumerate(splits):
            chunks.append({
                "chunk_id": f"{page['source']}_p{page['page']}_c{chunk_id}",
                "text": split,
                "source": page["source"],
                "page": page["page"],
                "file_path": page["file_path"]
            })

    return chunks