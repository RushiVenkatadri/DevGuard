import React, { useEffect, useState } from "react";
import { fetchScans } from "../services/api";

const Dashboard = () => {
  const [scans, setScans] = useState([]);

  useEffect(() => {
    const getScans = async () => {
      try {
        const data = await fetchScans();
        setScans(data);
      } catch (error) {
        console.error("Failed to fetch scan history", error);
      }
    };

    getScans();
  }, []);

  return (
    <div className="container mx-auto mt-8">
      <h1 className="text-3xl font-bold mb-4">Scan History</h1>
      <div className="bg-white shadow-md rounded p-4">
        {scans.length === 0 ? (
          <p>No scan history available</p>
        ) : (
          <ul>
            {scans.map((scan, index) => (
              <li key={index} className="border-b p-2">
                <strong>Project:</strong> {scan.project_url}  
                <br />
                <strong>Status:</strong> {scan.status}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Dashboard;