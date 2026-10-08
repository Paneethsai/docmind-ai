import os

from dotenv import load_dotenv
from google import genai
from ddgs import DDGS


# =====================================================
# LOAD ENVIRONMENT
# =====================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it to backend/.env"
    )


# =====================================================
# GEMINI CLIENT
# =====================================================

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-3.6-flash"


# =====================================================
# WEB SEARCH
# =====================================================

def web_search(query, max_results=5):

    try:

        print("Searching web for:", query)

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })

        print(
            "Web results found:",
            len(results)
        )

        return results

    except Exception as e:

        print(
            "WEB SEARCH ERROR:",
            repr(e)
        )

        return []


# =====================================================
# BUILD PDF CONTEXT
# =====================================================

def build_pdf_context(retrieved_chunks):

    if not retrieved_chunks:
        return "No relevant information was found in the uploaded PDF."

    context_parts = []

    for number, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
PDF SOURCE {number}
PAGE: {chunk["page"]}

{chunk["text"]}
"""
        )

    return "\n".join(context_parts)


# =====================================================
# BUILD WEB CONTEXT
# =====================================================

def build_web_context(web_results):

    if not web_results:

        return (
            "No external web information was available."
        )

    context_parts = []

    for number, result in enumerate(
        web_results,
        start=1
    ):

        context_parts.append(
            f"""
WEB SOURCE {number}
TITLE: {result["title"]}
URL: {result["url"]}

{result["snippet"]}
"""
        )

    return "\n".join(context_parts)


# =====================================================
# GENERATE ANSWER
# =====================================================

def generate_answer(
    question,
    retrieved_chunks
):

    print(
        "Generating answer for:",
        question
    )


    # -------------------------------------------------
    # PDF INFORMATION
    # -------------------------------------------------

    pdf_context = build_pdf_context(
        retrieved_chunks
    )


    # -------------------------------------------------
    # WEB INFORMATION
    # -------------------------------------------------

    web_results = web_search(
        question,
        max_results=5
    )

    web_context = build_web_context(
        web_results
    )


    # -------------------------------------------------
    # PROMPT
    # -------------------------------------------------

    prompt = f"""
You are DocuMind AI, an intelligent document and
web research assistant.

You have two information sources:

1. UPLOADED PDF
2. EXTERNAL WEB INFORMATION


IMPORTANT:

The uploaded PDF is the primary source when the
user asks specifically about the uploaded document.

External web information can be used to:

- explain concepts more clearly
- provide missing background information
- answer general questions
- provide current information
- compare the document with outside information
- improve the usefulness of the answer


====================================================
UPLOADED PDF
====================================================

{pdf_context}


====================================================
EXTERNAL WEB INFORMATION
====================================================

{web_context}


====================================================
ANSWER RULES
====================================================

1. Understand the user's exact question.

2. If the question is specifically about the PDF,
   prioritize information from the PDF.

3. If the PDF does not contain enough information,
   use reliable external information when appropriate.

4. Never present external information as if it came
   from the uploaded PDF.

5. Clearly distinguish PDF information from external
   information when both are used.

6. Do not invent facts.

7. Do not guess.

8. If reliable information cannot be found,
   clearly say so.

9. Use simple language.

10. Make answers easy for students to understand.

11. For steps, use numbered lists.

12. For comparisons, use clear bullet points or tables.

13. For definitions, give the definition first.

14. For explanations, provide a short example when
    reliable information supports it.

15. Do not mention FAISS, embeddings, chunks, or
    internal retrieval.

16. Do not claim that a web result came from the PDF.

17. If information from the web is used, mention that
    external sources were also considered.

18. For current or changing information, prefer the
    web information over old general knowledge.

19. Do not blindly trust a single web result.

20. If PDF information conflicts with external
    information, explain the difference instead of
    silently choosing one.


====================================================
USER QUESTION
====================================================

{question}


Now provide the most useful, accurate and
easy-to-understand answer.
"""


    # -------------------------------------------------
    # GEMINI
    # -------------------------------------------------

    try:

        print(
            "Sending question to Gemini..."
        )


        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt

        )


        if not response:

            raise RuntimeError(
                "Gemini returned no response."
            )


        answer = response.text


        if not answer:

            raise RuntimeError(
                "Gemini returned an empty answer."
            )


        answer = answer.strip()


        print(
            "Gemini answer generated successfully."
        )


        return {
            "answer": answer,
            "web_sources": web_results
        }


    except Exception as e:

        print(
            "GEMINI ERROR:",
            repr(e)
        )


        raise RuntimeError(
            f"Gemini API error: {str(e)}"
        )