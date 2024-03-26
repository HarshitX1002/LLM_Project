from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from typing import Any
from pymongo import MongoClient
from gridfs import GridFS
from transformers import pipeline
# from fastapi import APIRouter
# import gridfs
# Load environment variables from .env file (if any)
load_dotenv()
connection_string = "mongodb+srv://USER_123:USER_123@cluster0.3pxvzcm.mongodb.net/LLM_chatbot"
client = MongoClient(connection_string)


# Access your database and collection
db = client['LLM_chatbot']  # Replace 'your_database' with your actual database name
collection = db['USER_FILES']
fs = GridFS(db)

class Response(BaseModel):
   result: str | None
   query: str
   file_id: str
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
llm = pipeline("text-generation", model="gpt2")  # Initialize GPT-2 language model



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
    content = await file.read()
    file_id = collection.insert_one({"filename": file.filename, "content": await file.read()}).inserted_id
    return {"file_id": str(file_id)}
   


@app.post("/predict")
async def predict(query: str, file_id: list[str]):
    # Fetch file content from MongoDB based on file_id
    file_contents = [collection.find_one({"_id": file_id})["file_content"] for file_id in file_id]

    # Generate response using the language model
    response = llm(query + file_contents)

    return {"answer": "Generated answer based on the user query and file content"}
# @app.post("/predict")
# async def predict(file_id: str, question: str):
#      # Retrieve file content from MongoDB
#     file_data = fs.get(file_id).read()
#     # //file_content = file_data["content"].decode("utf-8")
    
#     # Use LLM to answer the question
#     prediction = llm_pipeline(question, file_data)
#     print(prediction)
    
#     return {"prediction": prediction}

  