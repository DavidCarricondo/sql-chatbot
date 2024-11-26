# app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from .model import LlamaCPP
import requests
from pathlib import Path
from .custom_types import QuestionRequest

# Define paths
BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "db/dataset01.db"

# Initialize FastAPI and Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Load Llama model
llama = LlamaCPP(model_path=str(BASE_DIR / "llama/ggml-model.bin"))

# Execute SQL query
def execute_query(query: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        conn.close()
        return str(e)

# Identify API or SQL request
def is_api_request(question: str) -> bool:
    keywords = ["clima", "tiempo", "temperatura", "weather"]
    return any(keyword in question.lower() for keyword in keywords)

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

@app.post("/ask", response_class=JSONResponse)
async def ask(question_request: QuestionRequest):
    user_input = question_request.question

    # Detect if it's an API request
    if is_api_request(user_input):
        # Generate city from user input using Llama
        city = llama.generate_api_request(user_input)  # Example: "Dame el clima en Madrid" → "Madrid"
        return {"result": fetch_weather(city)}

    # Generate SQL from the question
    sql_query = llama.generate_sql(user_input)
    if not sql_query:
        raise HTTPException(status_code=400, detail="No se pudo generar una consulta SQL.")

    # Execute SQL query
    result = execute_query(sql_query)
    return {"query": sql_query, "result": result}
