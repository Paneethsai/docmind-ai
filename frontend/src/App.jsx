
import { useState } from "react";

import Upload from "./components/Upload";
import Chat from "./components/Chat";

import "./App.css";


function App() {

  const [documentUploaded, setDocumentUploaded] =
    useState(false);


  function handleUploaded() {

    setDocumentUploaded(true);

  }


  return (

    <div className="app">

      {/* Background 3D shapes */}

      <div className="background-shape shape-one"></div>
      <div className="background-shape shape-two"></div>
      <div className="background-shape shape-three"></div>


      {/* Header */}

      <header className="hero">

        <div className="logo-box">
          🧠
        </div>

        <div className="badge">
          ✨ AI-Powered Document Assistant
        </div>

        <h1>
          DocuMind <span>AI</span>
        </h1>

        <p>
          Chat with your documents using the power of
          <strong> Generative AI</strong>
        </p>

        <div className="hero-tags">

          <span>📄 PDF Analysis</span>

          <span>⚡ Instant Answers</span>

          <span>🔎 Smart Search</span>

        </div>

      </header>


      {/* Main */}

      <main>

        <section className="glass-container">

          <div className="section-number">
            01
          </div>

          <Upload
            onUploaded={handleUploaded}
          />

        </section>


        <section className="glass-container">

          <div className="section-number">
            02
          </div>

          <Chat
            documentUploaded={documentUploaded}
          />

        </section>


        {/* Feature cards */}

        <section className="features">

          <div className="feature-card">

            <div className="feature-icon purple">
              📚
            </div>

            <h3>
              Understand
            </h3>

            <p>
              Extract meaningful information
              from your documents.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon blue">
              🔍
            </div>

            <h3>
              Search
            </h3>

            <p>
              Find the most relevant information
              instantly.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon pink">
              🤖
            </div>

            <h3>
              Ask AI
            </h3>

            <p>
              Get clear answers using
              Generative AI.
            </p>

          </div>

        </section>


        <footer>

          <p>
            Built with ❤️ using React • Flask • Gemini • FAISS
          </p>

        </footer>

      </main>

    </div>

  );
}


export default App;
