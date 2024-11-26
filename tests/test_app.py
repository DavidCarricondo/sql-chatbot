import pytest
from fastapi.testclient import TestClient
from sql_chatbot.app import app
from sql_chatbot.types_ import QuestionRequest

client = TestClient(app)

def test_ask_sql_query():
    question_request = QuestionRequest(question="Cual es la suma total de todos los importes?")
    response = client.post("/ask", json=question_request.model_dump())
    assert response.status_code == 200
    assert "result" in response.json()

@pytest.mark.skip(reason="This test requires implementing the api call")
def test_ask_api_request():
    question_request = QuestionRequest(question="Dame el clima en Madrid")
    response = client.post("/ask", json=question_request.model_dump())
    assert response.status_code == 200
    assert response.json()["result"] == "API request"

def test_ask_invalid_sql():
    question_request = QuestionRequest(question="INVALID SQL QUERY")
    response = client.post("/ask", json=question_request.model_dump())
    assert response.status_code == 200
    assert "result" in response.json()
    #assert "error" in response.json()["result"].lower()