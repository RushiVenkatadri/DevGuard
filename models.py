from sqlalchemy import Column, Integer, String, Boolean, JSON
from pydantic import BaseModel, EmailStr

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    status = Column(Integer)
    missing_headers = Column(JSON)
    exposed_headers = Column(JSON)
    clickjacking_vulnerable = Column(Boolean)


class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # Hashed password will be stored
