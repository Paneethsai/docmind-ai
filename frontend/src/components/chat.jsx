import { useState } from "react";

import { askQuestion } from "../api";

import Message from "./Message";


function Chat({ documentUploaded }) {

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

    const [webSources, setWebSources] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleAsk() {

    setError("");


    if (!documentUploaded) {

      setError(
        "Please upload a PDF first."
      );

      return;
    }


    if (!question.trim()) {

      setError(
        "Please enter a question."
      );

      return;
    }


    try {

      setLoading(true);


      const result =
        await askQuestion(question);


      setAnswer(
        result.answer || ""
      );


      setSources(
        Array.isArray(result.sources)
          ? result.sources
          : []
      );
      setWebSources(
        Array.isArray(result.web_sources)
          ? result.web_sources
          : []
      );

    } catch (error) {

      console.error(
        "Chat error:",
        error
      );


      setError(
        error.message ||
        "Something went wrong."
      );


    } finally {

      setLoading(false);

    }

  }


  return (

    <div className="chat-card">

      <h2>
        Ask anything about your document
      </h2>


      <div className="question-area">

        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask a question about your PDF..."
          disabled={loading}
          onKeyDown={(e) => {

            if (
              e.key === "Enter" &&
              !loading
            ) {

              handleAsk();

            }

          }}
        />


        <button
          onClick={handleAsk}
          disabled={
            loading ||
            !documentUploaded
          }
        >

          {loading
            ? "Thinking..."
            : "Ask AI"
          }

        </button>

      </div>


      {error && (

        <p className="error">
          {error}
        </p>

      )}


      {answer && (

        <Message
        answer={answer}
        sources={sources}
        webSources={webSources}
        />

      )}

    </div>

  );
}


export default Chat;