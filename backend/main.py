from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Ensure POST is allowed
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str  # Input validation for the request body

# ✅ Define the route correctly
@app.post("/scan")
async def scan_for_vulnerabilities(request: ScanRequest):
    return {"status": "scanned", "url": request.url, "vulnerabilities": []}
