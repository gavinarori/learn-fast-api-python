
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get MongoDB URL from environment variables
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("❌ MONGO_URL is not set in .env file")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL, tlsAllowInvalidCertificates=True)
db = client["fastapi_auth_db"]
users_collection = db["users"]
