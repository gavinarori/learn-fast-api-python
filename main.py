
from fastapi import FastAPI, HTTPException, status
import database
import schemas
import auth

from bson import ObjectId

app = FastAPI()

@app.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate):
    existing_user = await database.users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.hash_password(user.password)
    new_user = {"username": user.username, "email": user.email, "password": hashed_pw}
    result = await database.users_collection.insert_one(new_user)
    created_user = await database.users_collection.find_one({"_id": result.inserted_id})

    return {
        "id": str(created_user["_id"]),
        "username": created_user["username"],
        "email": created_user["email"],
    }

@app.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserCreate):
    db_user = await database.users_collection.find_one({"email": user.email})
    if not db_user or not auth.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth.create_access_token({"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
