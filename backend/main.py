from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")  

app = FastAPI()

class Question(BaseModel):
    query: str
    history: List[str] = Field(default_factory=list)
@app.get("/")
def home():
    return {"message": "Welcome to Python Tutor API. Use POST /ask to chat."}

@app.post("/ask")
def ask_tutor(question: Question):
    # System prompt ensures tutor-like behavior
    system_prompt = """You are a friendly and patient Python tutor.
- Always explain concepts step by step.
- Use simple examples that beginners can understand.
- Encourage and motivate the learner.
- If code is shared, explain what it does and help debug with clear reasoning.
- Avoid overly complex jargon unless necessary.
"""

    # Build conversation
    conversation = system_prompt + "\n"
    for turn in question.history:
        conversation += turn + "\n"
    conversation += f"User: {question.query}\nTutor:"

    try:
        response = model.generate_content(conversation)
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
