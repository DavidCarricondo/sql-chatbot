# app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from sql_chatbot.modulos.chatbot_sql import SQLChatbot
import requests
from pathlib import Path
from .types_ import QuestionRequest
from sql_chatbot.modulos.router import is_api_request

# Define paths
BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "db/dataset01.db"

app = FastAPI()
#templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

#llama = LlamaCPP(model_path=str(BASE_DIR / "llama/ggml-model.bin"))

"""
# Fetch weather data
def fetch_weather(city: str) -> str:
    # Replace with your OpenWeatherMap API key
    api_key = "TU_CLAVE_API_AQUI"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"El clima en {city} es {description} con una temperatura de {temp}°C."
        else:
            return "No pude obtener el clima. ¿Escribiste correctamente la ciudad?"
    except Exception as e:
        return f"Error al conectar con el API: {e}"

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
"""

@app.post("/ask", response_class=JSONResponse)
async def ask(question_request: QuestionRequest):
    user_input = question_request.model_dump()
    question = question_request.question
    # Detect if it's an API request
    if is_api_request(question):
        # Generate city from user input using Llama
        #city = llama.generate_api_request(user_input)  # Example: "Dame el clima en Madrid" → "Madrid"
        #return {"result": fetch_weather(city)}
        return {"result": "API request"}

    # Generate SQL from the question
    sql_ = SQLChatbot(db_uri="sqlite:////home/dacs00/projects/sql-chatbot/db/dataset01.db", 
                         model_path="../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
                         )
    try:
        response = sql_.run(user_input)
    except Exception as e:
        response = str(e)

    return JSONResponse(content={"result": response})
