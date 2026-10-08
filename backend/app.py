import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from rag import process_pdf, search
from llm import generate_answer


app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = "../uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok"
    })


@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No PDF selected."
            }), 400


        file = request.files["file"]


        if file.filename == "":

            return jsonify({
                "error": "No PDF selected."
            }), 400


        if not file.filename.lower().endswith(".pdf"):

            return jsonify({
                "error": "Only PDF files are allowed."
            }), 400


        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        file.save(filepath)


        chunk_count = process_pdf(
            filepath
        )


        return jsonify({

            "message":
                "Document processed successfully",

            "chunks":
                chunk_count

        })


    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    except Exception as e:

        print(
            "UPLOAD ERROR:",
            repr(e)
        )

        return jsonify({

            "error":
                "PDF processing failed."

        }), 500


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "error": "Invalid request."
            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({
                "error":
                    "Please enter a question."
            }), 400


        print(
            "Question:",
            question
        )


        retrieved_chunks = search(
            question,
            top_k=5
        )


        print(
            "Retrieved chunks:",
            len(retrieved_chunks)
        )


        result = generate_answer(
            question,
            retrieved_chunks
        )

        answer = result["answer"]

        web_sources = result.get(
            "web_sources",
            []
        )


        sources = sorted(
            set(
                int(chunk["page"])
                for chunk in retrieved_chunks
            )
        )


        return jsonify({

            "answer":
                answer,

            "sources":
                sources,

            "web_sources":
                web_sources

        })

    except ValueError as e:

        print(
            "CHAT ERROR:",
            repr(e)
        )

        return jsonify({

            "error":
                str(e)

        }), 400


    except RuntimeError as e:

        print(
            "CHAT ERROR:",
            repr(e)
        )

        return jsonify({

            "error":
                str(e)

        }), 500


    except Exception as e:

        print(
            "CHAT ERROR:",
            repr(e)
        )

        return jsonify({

            "error":
                "Something went wrong while processing "
                "your question."

        }), 500


if __name__ == "__main__":

    print(
        "Starting DocuMind AI backend..."
    )


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False

    )