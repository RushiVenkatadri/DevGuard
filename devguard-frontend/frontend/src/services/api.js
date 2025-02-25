import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // ✅ Backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export const scanProject = async (projectUrl) => {
  try {
    const response = await api.post("/scan", { url: projectUrl }); // ✅ Ensure key is "url"
    return response.data;
  } catch (error) {
    console.error("Error scanning project:", error);
    throw error;
  }
};


// ✅ New function to fetch scan results
export const fetchScans = async () => {
  try {
    const response = await api.get("/scans"); // Ensure your FastAPI backend has this route
    return response.data;
  } catch (error) {
    console.error("Error fetching scans:", error);
    throw error;
  }
};

