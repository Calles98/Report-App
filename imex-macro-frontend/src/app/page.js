"use client";

import { redirect, useRouter } from "next/navigation";
import { useState, useRef } from "react";

const types = ["Standard", "Duplicates", "Blanks"];

export default function Home() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [analysisType, setAnalysisType] = useState("Standard");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("analysisType", analysisType);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload file");
      }

      // Create a Blob URL for the downloaded file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);

      // Clear the file input after report is processed
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = ""; // Reset the input field
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="flex flex-col gap-y-10 min-h-screen justify-center items-center mx-auto">
      <div>
        <h1>Select the type of analysis:</h1>
        <ul className="flex gap-2">
          {types.map((type, index) => (
            <li
              key={index}
              className={`hover:cursor-pointer hover:underline hover:text-blue-800 ${
                analysisType === type && "underline text-blue-800"
              }`}
              onClick={() => setAnalysisType(type)}
            >
              {type}
            </li>
          ))}
        </ul>
      </div>
      <h1 className="m-4 text-xl font-bold">Upload File for Analysis</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} ref={fileInputRef} />
        <button
          type="submit"
          className="bg-slate-500 text-white p-5 rounded-md"
        >
          Upload and Process
        </button>
      </form>
      {downloadUrl && (
        <div className="text-xl font-thin">
          <h2>Download your processed report:</h2>
          <a
            className="hover:underline hover:text-blue-500"
            href={downloadUrl}
            download="report.html"
            onClick={() => setDownloadUrl("")}
          >
            Download Report
          </a>
        </div>
      )}
    </div>
  );
}
