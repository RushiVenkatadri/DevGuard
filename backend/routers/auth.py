from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import jwt
import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Secret keys (Change these in production)
SECRET_KEY = "kira"
ALGORITHM = "HS256"

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")  # Adjust if necessary
db = client.devguard  # Database name
users_collection = db.users  # Collection name

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# FastAPI router
router = APIRouter()

# User Models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Password hashing functions
def hash_password(password: str) -> str:
    """Hash the password securely."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if password is correct."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# JWT Token Generation
def create_access_token(username: str):
    """Generate JWT access token."""
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# User Registration
@router.post("/register")
async def register_user(user: UserRegister):
    """Register a new user."""
    existing_user = await users_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "email": user.email, "password": hashed_password}

    await users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

# User Login
@router.post("/login")
async def login_user(user: UserLogin):
    """Login user and return JWT token."""
    stored_user = await users_collection.find_one({"username": user.username})

    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

# Get Current User (Protected Route Dependency)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protected Route Example
@router.get("/protected-route")
async def protected_route(user: dict = Depends(get_current_user)):
    """Example of a protected route."""
    return {"message": f"Hello, {user['username']}! You accessed a protected route."}

# Logout (Placeholder)
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme)):
    """Logout user (Currently just a placeholder)."""
    return {"message": "Logout successful"}
