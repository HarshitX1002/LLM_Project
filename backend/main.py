from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from typing import Any
from pymongo import MongoClient
from gridfs import GridFS
from transformers import T5ForConditionalGeneration, T5Tokenizer

# from fastapi import APIRouter
# import gridfs
# Load environment variables from .env file (if any)
load_dotenv()
connection_string = "mongodb+srv://USER_123:USER_123@cluster0.3pxvzcm.mongodb.net/LLM_chatbot"
client = MongoClient(connection_string)


# Access your database and collection
db = client['LLM_chatbot']  # Replace 'your_database' with your actual database name
collection = db['USER_FILES']


# class Response(BaseModel):
#    result: str | None
#    query: str
#    file_id: str
class FileMetadata(BaseModel):
    filename: str
    size: int
class InputData(BaseModel):
  input: str

model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

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
    content = await file.read()
    file_id = collection.insert_one({"filename": file.filename, "content": await file.read()}).inserted_id
    print("deffucntion")
    return {"file_id": str(file_id)}
   


@app.post("/predict")
async def predict(data: InputData):
        input_text = data.input
        context = ""  # Add context here
        input_ids = tokenizer.encode(context + input_text, return_tensors="pt")

    # Generate text using the T5 model
        output = model.generate(input_ids, max_length=100)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)


        print(generated_text)
        return {"result": generated_text}

    # Decode the generated text
        

        
    # Generate text based on the provided prompt
        
                

        









# @app.post("/predict")

# async def predict(file_id: str, question: str):
#      # Retrieve file content from MongoDB
#     file_data = fs.get(file_id).read()
#     # //file_content = file_data["content"].decode("utf-8")
    
#     # Use LLM to answer the question
#     prediction = llm_pipeline(question, file_data)
#     print(prediction)
    
#     return {"prediction": prediction}

  