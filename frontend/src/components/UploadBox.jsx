import { useRef } from "react";

function UploadBox({
  file,
  setFile,
}) {
  const inputRef = useRef(null);

  const handleFileChange = (event) => {
    const selected = event.target.files[0];

    if (!selected) return;

    if (selected.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    setFile(selected);
  };

  return (
    <div className="bg-slate-800 rounded-2xl border-2 border-dashed border-slate-600 p-10 text-center">

      <h2 className="text-2xl font-semibold mb-4">
        Upload EPC Document
      </h2>

      <p className="text-slate-400 mb-8">
        Drag & Drop your PDF here
      </p>

      <button
        onClick={() => inputRef.current.click()}
        className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl"
      >
        Choose PDF
      </button>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleFileChange}
      />

      {file && (

        <div className="mt-8 bg-slate-900 rounded-xl p-4">

          <p className="text-green-400 font-medium">
            Selected File
          </p>

          <p className="mt-2">
            {file.name}
          </p>

          <p className="text-sm text-slate-400 mt-2">
            {(file.size / 1024 / 1024).toFixed(2)} MB
          </p>

        </div>

      )}

    </div>
  );
}

export default UploadBox;