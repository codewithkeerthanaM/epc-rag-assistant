import { useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import UploadBox from "../components/UploadBox";
import UploadProgress from "../components/UploadProgress";

function Upload() {

  const [file, setFile] = useState(null);

  const [status] = useState(
    "Ready to upload."
  );

  return (

    <DashboardLayout>

      <div className="max-w-4xl mx-auto p-10">

        <UploadBox
          file={file}
          setFile={setFile}
        />

        <UploadProgress
          status={status}
        />

      </div>

    </DashboardLayout>

  );
}

export default Upload;