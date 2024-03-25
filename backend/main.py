from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from pymongo import MongoClient
from pathlib import Path
# from fastapi import APIRouter
# import gridfs
# Load environment variables from .env file (if any)
load_dotenv()
connection_string = "mongodb+srv://USER_123:USER_123@cluster0.3pxvzcm.mongodb.net/LLM_chatbot"
client = MongoClient(connection_string)


# Access your database and collection
db = client['LLM_chatbot']  # Replace 'your_database' with your actual database name
collection = db['USER_FILES']

class Response(BaseModel):
   result: str | None
class FileMetadata(BaseModel):
    filename: str
    size: int
    

    

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



conn = MongoClient("mongodb+srv://USER_123:USER_123@cluster0.3pxvzcm.mongodb.net/LLM_chatbot")
     
@app.get("/")
def read_item():
    return {"Server"}

# @app.post("/",)
# async def post_todo(file: UploadFile = File(...)):
#     content_assignment = await file.read()
#     print(content_assignment)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
   file_size = file.file.__sizeof__()
 
   metadata = FileMetadata(filename=file.filename, size = file_size)
   collection.insert_one(metadata.dict())
   return {"filename": file.filename, "size": file_size}

    # Save metadata to MongoDB

   


@app.post("/predict", response_model = Response)
def predict() -> Any:

  #implement this code block
  
  return {"result": "hello world!"}