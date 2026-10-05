import os
import json
import fitz
import numpy as np
import faiss

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

DOCUMENT_FOLDER = "documents"
INDEX_FILE = "campuslens.index"
DATA_FILE = "chunks.json"


def chunk_text(text, chunk_size=1000, overlap=150):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


all_chunks = []

print("📚 Reading college documents...")

for filename in os.listdir(DOCUMENT_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(DOCUMENT_FOLDER, filename)

    print(f"📄 Processing: {filename}")

    doc = fitz.open(pdf_path)

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text().strip()

        if not text:
            continue

        chunks = chunk_text(text)

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": filename,
                "page": page_number,
                "verified": True
            })

    doc.close()


print(f"✅ Created {len(all_chunks)} chunks")


print("🧠 Creating embeddings...")

embeddings = []

for i, item in enumerate(all_chunks):

    print(f"Embedding {i + 1}/{len(all_chunks)}")

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=item["text"]
    )

    embeddings.append(result.embeddings[0].values)


embeddings = np.array(
    embeddings,
    dtype="float32"
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(DATA_FILE, "w", encoding="utf-8") as file:
    json.dump(
        all_chunks,
        file,
        ensure_ascii=False,
        indent=2
    )

print()
print("🎉 RAG index created successfully!")
print(f"📦 Vector index: {INDEX_FILE}")
print(f"📄 Chunk data: {DATA_FILE}")