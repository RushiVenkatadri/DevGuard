from fastapi import APIRouter, Depends
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.models import ScanResult

router = APIRouter()

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Referrer-Policy"
]

@router.get("/scan")
async def scan_website(url: str, db: AsyncSession = Depends(get_db)):
    """
    Scan website and store results in PostgreSQL.
    """
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        # Security checks
        missing_headers = [header for header in SECURITY_HEADERS if header not in headers]
        exposed_headers = {h: headers[h] for h in ["X-Powered-By", "Server"] if h in headers}
        clickjacking_vulnerable = "X-Frame-Options" not in headers

        # Store result in database
        scan_result = ScanResult(
            url=url,
            status=response.status_code,
            missing_headers=missing_headers,
            exposed_headers=exposed_headers,
            clickjacking_vulnerable=clickjacking_vulnerable
        )
        db.add(scan_result)
        await db.commit()

        return {
            "url": url,
            "status": response.status_code,
            "missing_headers": missing_headers,
            "exposed_headers": exposed_headers,
            "clickjacking_vulnerable": clickjacking_vulnerable
        }
    except requests.exceptions.RequestException:
        return {"url": url, "status": "error", "message": "Website not reachable"}
