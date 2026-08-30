import json
from pathlib import Path

import ollama


KNOWLEDGE_BASE = Path("knowledge_base")
OUTPUT_FILE = Path("rag/knowledge_index.json")
EMBEDDING_MODEL = "embeddinggemma"


def load_documents():
    documents = []

    for filepath in KNOWLEDGE_BASE.glob("*.md"):
        content = filepath.read_text(encoding="utf-8")

        documents.append({
            "source": filepath.name,
            "content": content
        })

    return documents


def chunk_text(text, chunk_size=1000):
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        candidate = (
            f"{current_chunk}\n\n{paragraph}"
            if current_chunk
            else paragraph
        )

        if len(candidate) <= chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def build_index():
    documents = load_documents()

    records = []

    for document in documents:
        chunks = chunk_text(document["content"])

        for chunk_number, chunk in enumerate(chunks):
            response = ollama.embed(
                model=EMBEDDING_MODEL,
                input=chunk
            )

            embedding = response["embeddings"][0]

            records.append({
                "source": document["source"],
                "chunk": chunk_number,
                "text": chunk,
                "embedding": embedding
            })

            print(
                f"Indexed {document['source']} "
                f"chunk {chunk_number}"
            )

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(records),
        encoding="utf-8"
    )

    print(f"\nIndexed {len(records)} chunks.")


if __name__ == "__main__":
    build_index()