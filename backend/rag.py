import pymupdf
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Global document state
index = None
chunks = []


def process_pdf(pdf_path):

    global index, chunks

    # Open PDF
    document = pymupdf.open(pdf_path)

    pages = []

    # Extract text page by page
    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text().strip()

        if text:

            pages.append({
                "text": text,
                "page": page_number
            })

    document.close()


    # Reject empty/scanned PDFs
    if not pages:

        raise ValueError(
            "This PDF does not contain readable text. "
            "Please upload a text-based PDF."
        )


    # Create chunks
    new_chunks = create_chunks(
        pages
    )


    if not new_chunks:

        raise ValueError(
            "No readable content was found in the PDF."
        )


    # Create embeddings
    texts = [
        chunk["text"]
        for chunk in new_chunks
    ]


    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )


    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )


    # Create FAISS index
    dimension = embeddings.shape[1]

    new_index = faiss.IndexFlatIP(
        dimension
    )


    new_index.add(
        embeddings
    )


    # Replace old document only after
    # successful processing
    chunks = new_chunks

    index = new_index


    return len(chunks)


def create_chunks(
    pages,
    chunk_size=600,
    overlap=100
):

    result = []


    for page in pages:

        words = page["text"].split()


        if not words:
            continue


        start = 0


        while start < len(words):

            end = min(
                start + chunk_size,
                len(words)
            )


            text = " ".join(
                words[start:end]
            ).strip()


            if text:

                result.append({

                    "text": text,

                    "page": page["page"]

                })


            # Move forward
            start += (
                chunk_size - overlap
            )


    return result


def search(
    query,
    top_k=5
):

    if index is None or not chunks:

        raise ValueError(
            "Please upload a PDF first."
        )


    # Create query embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )


    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )


    # Search FAISS
    number_to_search = min(
        top_k,
        len(chunks)
    )


    scores, indices = index.search(
        query_embedding,
        number_to_search
    )


    results = []


    for score, i in zip(
        scores[0],
        indices[0]
    ):

        if i < 0:
            continue


        result = {
            "text": chunks[i]["text"],
            "page": chunks[i]["page"],
            "score": float(score)
        }


        results.append(result)


    return results