# database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://arorigavincode_db_user:aNl2mDqmRwPb5ZBX@cluster0.vehurzz.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL, tlsAllowInvalidCertificates=True)
db = client["fastapi_auth_db"]
users_collection = db["users"]
