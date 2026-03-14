def build_prompt(query: str, chunks: list) -> str:
    """
    Build a prompt for the LLM using retrieved chunks as context.
    """
    context = ""
    for i, chunk in enumerate(chunks, 1):
        context += (
            f"\n[{i}] Source: {chunk['source']} | Page: {chunk['page']}\n"
            f"{chunk['text']}\n"
            f"{'-' * 60}\n"
        )

    prompt = f"""You are an expert research assistant. Your job is to answer questions 
based strictly on the provided research paper excerpts below.

RULES:
- Answer ONLY using the context provided below.
- Always cite sources using [1], [2], etc. matching the chunk numbers.
- If the answer is not found in the context, say: 
  "I could not find relevant information in the provided papers."
- Be precise, academic, and concise.
- For comparison queries, structure your answer clearly with headings.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""

    return prompt


def build_summary_prompt(chunks: list, paper_name: str) -> str:
    """
    Build a prompt specifically for summarizing a paper.
    """
    context = ""
    for i, chunk in enumerate(chunks, 1):
        context += f"\n[{i}] Page {chunk['page']}:\n{chunk['text']}\n"

    prompt = f"""You are an expert research assistant. Summarize the research paper 
"{paper_name}" based on the excerpts below.

Include:
- Main objective
- Methodology used
- Key findings
- Contributions
- Limitations (if mentioned)

CONTEXT:
{context}

SUMMARY:"""

    return prompt