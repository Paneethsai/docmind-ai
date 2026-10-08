const API_URL = "http://127.0.0.1:5000";


async function getResponseData(response) {

  const contentType =
    response.headers.get("content-type");


  if (
    contentType &&
    contentType.includes("application/json")
  ) {

    return await response.json();

  }


  return {
    error: `Server returned HTTP ${response.status}`
  };

}


export async function uploadPDF(file) {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  try {

    const response = await fetch(
      `${API_URL}/upload`,
      {
        method: "POST",
        body: formData
      }
    );


    const data =
      await getResponseData(response);


    if (!response.ok) {

      throw new Error(
        data.error ||
        "PDF upload failed."
      );

    }


    return data;


  } catch (error) {

    if (
      error.name === "TypeError"
    ) {

      throw new Error(
        "Cannot connect to the DocuMind AI backend. "
        + "Make sure the Flask server is running."
      );

    }


    throw error;

  }
}


export async function askQuestion(
  question
) {

  try {

    const response = await fetch(
      `${API_URL}/chat`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          question: question.trim()
        })
      }
    );


    const data =
      await getResponseData(response);


    if (!response.ok) {

      throw new Error(
        data.error ||
        "Could not generate an answer."
      );

    }


    return data;


  } catch (error) {

    if (
      error.name === "TypeError"
    ) {

      throw new Error(
        "Cannot connect to the DocuMind AI backend. "
        + "Make sure the Flask server is running."
      );

    }


    throw error;

  }
}