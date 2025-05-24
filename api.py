from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, request, jsonify
from clinicaltrialsdatabasehandler_trial_shortlisting import DataBaseHandler
from pymongo import MongoClient
from pydantic import BaseModel,EmailStr
from typing import Dict,Any
from patient_card_frontend_validation_app import PatientCard
import shortlisted_nctids
import time,threading
import json 
import requests
import os

#--------------------------------------------------------------------------------------------------------------
cache_lock = threading.Lock()
processed_col = "Processed_Clinical_Trials",
uri = 'mongodb://usamahs226:CureMDUsamahpa55phras3@172.16.101.226:27017/?authMechanism=DEFAULT',
client = MongoClient(uri) 
inference_stats_db = client['oncology_trials']  
inference_stats_collection = inference_stats_db['50_patients_updated']
#--------------------------------------------------------------------------------------------------------------
dbh = DataBaseHandler()
app = FastAPI()
PatientDetails = "PatientDetails"
LogicBuilder = "LogicBuilder"
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
                    "http://localhost:5173","http://172.16.19.80:5173",
                    "http://localhost:5174","http://172.16.19.80:5174",
                    "http://localhost:5175","http://172.16.19.80:5175",
                    "http://localhost:5176","http://172.16.19.80:5176",
                    "http://localhost:5178","http://172.16.19.80:5178",
                    "http://localhost:5179","http://172.16.19.80:5179",


                    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
#--------------------------------------------------------------------------------------------------------------
user_login_collection = dbh.db["User_login_data"]


# Pydantic models
class User(BaseModel):
    UserName: str
    password: str


# /check-user endpoint
@app.post("/check-user")
async def check_user(user: User):
    existing_user = user_login_collection.find_one({
        "UserName": user.UserName,
        "password": user.password  # In production, use hashed passwords
    })
    UserName = user.UserName
    # Create a user-specific collection
    user_collection_name = f"user_data_{UserName.strip()}"

    if existing_user:
        return {"exists": True,
                "user_collection": user_collection_name}
    else:
        return {"exists": False}

# Pydantic models
class signupUser(BaseModel):
    UserName: str
    email: EmailStr
    password: str

@app.post("/sign-up")
async def sign_up(user: signupUser):
    existing_user = user_login_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert user in users-login-data
    user_login_collection.insert_one(user.dict())
    UserName = user.UserName
    # Create a user-specific collection
    user_collection_name = f"user_data_{UserName.strip()}"


    dbh.db.create_collection(user_collection_name)  # Optional: safe to skip if it will auto-create on first insert

    return {
        "message": "User created successfully",
        "user_collection": user_collection_name
    }
