import pytest
from sql_chatbot.modulos.chatbot_sql import SQLChatbot
from sql_chatbot.types_ import OutputSqlJson

@pytest.fixture
def sql_chatbot_instance():
    return SQLChatbot(
        db_uri="sqlite:////home/dacs00/projects/sql-chatbot/db/dataset01.db", 
        model_path="../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
                         )

def test_load_sql_template_default(sql_chatbot_instance):
    prompt = sql_chatbot_instance.load_sql_template()
    assert prompt is not None
    assert "{input}" in prompt.template

def test_load_sql_template_custom(sql_chatbot_instance):
    custom_template = "SELECT * FROM users WHERE id = {input}"
    prompt = sql_chatbot_instance.load_sql_template(custom_template)
    assert prompt is not None
    assert prompt.template == custom_template

def test_load_llm_model(sql_chatbot_instance):
    llm = sql_chatbot_instance.load_llm_model()
    assert llm is not None

def test_load_sql_chain(sql_chatbot_instance):
    chain = sql_chatbot_instance.load_sql_chain()
    assert chain is not None

def test_invoke_sql_chain(sql_chatbot_instance):
    question = {"question": "Cuantos clientes hay?"}
    response = sql_chatbot_instance.invoke_sql_chain(question)
    assert response is not None
    assert isinstance(response, str)

def test_invoke_sql_chain_with_validation(sql_chatbot_instance):
    question = {"question": "Cuantos clientes hay?"}
    response = sql_chatbot_instance.invoke_sql_chain_with_validation(question)
    assert isinstance(response, str)

def test_run(sql_chatbot_instance):
    query = {"question":"Cuanto es la suma de todos los importes?"}
    response = sql_chatbot_instance.run(query)
    assert response is not None
    assert "SQLQuery" in response
    assert "ANSWER" in response