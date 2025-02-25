import React, { useState } from "react";
import { scanProject } from "../services/api";

const ScanForm = () => {
  const [projectUrl, setProjectUrl] = useState("");
  const [scanResult, setScanResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleScanSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const result = await scanProject(projectUrl);
      setScanResult(result);
    } catch (error) {
      setScanResult({ message: "Failed to scan project" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center mt-10">
      <h2 className="text-2xl font-bold mb-4">Security Scanner</h2>
      <form onSubmit={handleScanSubmit} className="flex flex-col items-center">
        <input
          type="text"
          value={projectUrl}
          onChange={(e) => setProjectUrl(e.target.value)}
          placeholder="Enter GitHub project URL"
          className="px-4 py-2 border rounded w-80 mb-2"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          {isLoading ? "Scanning..." : "Scan Project"}
        </button>
      </form>

      {scanResult && (
        <div className="mt-4 bg-gray-200 p-4 rounded w-80">
          <h3 className="font-bold">Scan Result:</h3>
          <pre className="text-sm">{JSON.stringify(scanResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ScanForm;

