# app.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Union
from .types_ import QuestionRequest
from sql_chatbot.modulos.chatbot_sql import SQLChatbot
from sql_chatbot.modulos.router import is_api_request
from sql_chatbot.modulos.chatbot_api import api_call

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Description": "POC SQL Chatbot with router to API requests and SQL queries."}

@app.post("/ask", response_class=HTMLResponse)
async def ask(question_request: QuestionRequest):
    user_input = question_request.model_dump()
    question = question_request.question
    # Detect if it's an API request
    if is_api_request(question):
        data = api_call()
        return templates.TemplateResponse(
            "index_api.html",
            {"request": {}, "data": data},
        )

    # Generate SQL from the question
    sql_ = SQLChatbot(db_uri="sqlite:////home/dacs00/projects/sql-chatbot/db/dataset01.db", 
                         model_path="../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
                         )
    try:
        response = sql_.run(user_input, validation=False)
    except Exception as e:
        response = str(e)
    return templates.TemplateResponse(
    "index_sql.html",
    {"request": {}, "data": response},
)

#curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "dame una imagen de la nasa"}'