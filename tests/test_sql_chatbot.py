import pytest
from sql_chatbot.sql_chatbot import load_sql_template, load_llm_model, load_sql_chain, invoke_sql_chain

def test_load_sql_template_default():
    prompt = load_sql_template()
    assert prompt is not None
    assert "{input}" in prompt.template

def test_load_sql_template_custom():
    custom_template = "SELECT * FROM users WHERE id = {input}"
    prompt = load_sql_template(custom_template)
    assert prompt is not None
    assert prompt.template == custom_template

def test_load_llm_model():
    model_path = "../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
    llm = load_llm_model(model_path)
    assert llm is not None

def test_load_sql_chain():
    chain = load_sql_chain()
    assert chain is not None

def test_invoke_sql_chain():
    question = {"question": "Cuantos clientes hay?"}
    response = invoke_sql_chain(question)
    assert response is not None
    assert "SQLResult" in response