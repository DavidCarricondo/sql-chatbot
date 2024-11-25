import pytest
from sql_chatbot.model import LlmModel
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


@pytest.fixture
def model():
    return LlmModel(model_path="../../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def test_load_llm(model):
    model.load_llm()
    assert model.llm is not None
    assert isinstance(model.llm.callback_manager, CallbackManager)

def test_set_prompt_template_default(model):
    template = model.set_prompt_template(None)
    assert isinstance(template, PromptTemplate)
    assert "Question: {question}" in template.template

def test_set_prompt_template_custom(model):
    custom_template = "Custom question: {question}"
    template = model.set_prompt_template(custom_template)
    assert isinstance(template, PromptTemplate)
    assert "Custom question: {question}" in template.template

def test_invoke_llm(model, mocker):
    model.load_llm()
    mock_response = "Mock response"
    mocker.patch.object(model.llm, 'invoke', return_value=mock_response)
    response = model.invoke_llm(prompt="What is AI?")
    assert response == mock_response

def test_invoke_llm_exception(model, mocker):
    model.load_llm()
    mocker.patch.object(model.llm, 'invoke', side_effect=Exception("Mock exception"))
    response = model.invoke_llm(prompt="What is AI?")
    assert "Mock exception" in response
