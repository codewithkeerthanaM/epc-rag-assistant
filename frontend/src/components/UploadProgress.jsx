function UploadProgress({
  status,
}) {
  return (
    <div className="bg-slate-800 rounded-xl p-5 mt-6">

      <h3 className="font-semibold mb-3">
        Upload Status
      </h3>

      <div className="bg-slate-900 rounded-lg p-4">

        <p className="text-green-400">
          {status}
        </p>

      </div>

    </div>
  );
}

export default UploadProgress;