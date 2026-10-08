import { useState } from "react";
import { uploadPDF } from "../api";


function Upload({ onUploaded }) {

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");


  async function handleUpload(event) {

    const file = event.target.files[0];

    if (!file) return;


    if (!file.name.toLowerCase().endsWith(".pdf")) {

      setMessage("Please select a PDF file.");

      return;
    }


    try {

      setLoading(true);

      setMessage("");


      const result = await uploadPDF(file);


      setMessage(
        `${result.message} (${result.chunks} chunks)`
      );


      // Tell App.jsx that the PDF is ready
      onUploaded();


    } catch (error) {

      console.error("Upload error:", error);

      setMessage(error.message);


    } finally {

      setLoading(false);

    }
  }


  return (

    <div className="upload-card">

      <div className="upload-icon">
        📄
      </div>


      <h2>
        Upload your PDF
      </h2>


      <p>
        Upload a document and ask questions about it.
      </p>


      <label className="upload-button">

        {loading
          ? "Processing..."
          : "Choose PDF"
        }


        <input
          type="file"
          accept=".pdf"
          onChange={handleUpload}
          hidden
        />

      </label>


      {message && (

        <p className="upload-message">
          {message}
        </p>

      )}

    </div>
  );
}


export default Upload;