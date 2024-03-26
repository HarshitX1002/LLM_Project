import React from "react";
import { useState, useEffect } from "react";
import Navbar from "./components/nav";
import axios from "axios";
// import "./App.css";

export default function App() {
  const [result, setResult] = useState();
  const [question, setQuestion] = useState();
  const [file, setFile] = useState(null);
  const [answer, setAnswer] = useState("");

  const handleQuestionChange = (event: any) => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: any) => {
    setFile(event.target.files[0]);
  };

  const handleFormSubmit1 = async (event: any) => {
    event.preventDefault();

    if (!file) {
      console.error("No file selected");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    axios.post("http://127.0.0.1:8000/upload", formData).then((response) => {
      console.log(response);
    });
  };

  const handleFormSubmit = async (event: any) => {
    event.preventDefault();

    if (!file) {
      console.error("No file selected");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    if (question) {
      formData.append("question", question);
    }

    // fetch("http://127.0.0.1:8000/predict", {
    //   method: "POST",
    //   body: formData,
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     setResult(data.result);
    //   })
    //   .catch((error) => {
    //     console.error("Error", error);
    //   });
  };
  const fetchAnswer = async () => {
    try {
      const response = await axios.post("http://localhost:8000/predict", {
        // Include any necessary data for generating the answer
      });
      setAnswer(response.data.answer); // Assuming the response contains the generated answer
    } catch (error) {
      console.error("Error fetching answer:", error);
    }
  };

  return (
    <>
      <Navbar />
      <div className="container-fluid">
        <div
          className="container-fluid text-center bg-dark rounded-3"
          data-bs-spy="scroll"
          data-bs-root-margin="0px 0px -40%"
          data-bs-smooth-scroll="true"
        >
          <form className="form">
            <div className="my-2">
              <label
                className="p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3 my-3"
                htmlFor="question"
              >
                Question :
              </label>
              <input
                className="p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3 mx-2 questionInput"
                id="question"
                type="text"
                value={question}
                onChange={handleQuestionChange}
                placeholder="Ask your question here"
              />
              <button
                className="btn btn-primary submitBtn rounded-3 btn-lg "
                style={{ padding: "14px" }}
                id="submit"
                type="submit"
                onClick={handleFormSubmit}
                disabled={!file || !question}
              >
                Submit
              </button>
            </div>
          </form>
          <div>
            <label
              className="p-3 text-dark bg-dark-subtle border border-dark-subtle rounded-3 fileLabel"
              htmlFor="file"
            >
              Upload CSV, TXT, PDF or DOCX file:
            </label>
            <input
              type="file"
              id="file"
              name="file"
              accept=".csv,.docx,.pdf,.txt"
              onChange={handleFileChange}
              className="p-3 text-dark bg-dark-subtle border border-dark-subtle rounded-3 fileInput my-4"
            />
            <button
              className="btn btn-secondary submitBtn rounded-3 btn-lg rounded-3 mx-2 submitBtn my-3  fileLabel"
              type="submit"
              id="upload"
              onClick={handleFormSubmit1}
              style={{ padding: "15px" }}
              //alert={("File uploaded successfully!")}
            >
              Upload
            </button>
          </div>
          <div>
            <label className="m- p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3 my-3">
              <h4>Result</h4>
            </label>
            <br />
            <textarea
               className="resultOutput bg-secondary"
               id="textArea"
              value={result}
              cols={150}
              rows={100}
            >
              Result:
            </textarea>
          </div>
        </div>
      </div>
    </>
  );
}
function then(arg0: any) {
  throw new Error("Function not implemented.");
}
