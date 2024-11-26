import pytest
from sql_chatbot.model import LlmModel
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


@pytest.fixture
def model():
    return LlmModel(model_path="../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def test_load_llm(model):
    model.load_llm()
    assert model.llm is not None
    
def test_set_prompt_template_default(model):
    template = model.set_prompt_template(None)
    assert isinstance(template, PromptTemplate)
    assert "Question: {question}" in template.template

def test_set_prompt_template_custom(model):
    custom_template = "Custom question: {question}"
    template = model.set_prompt_template(template = custom_template)
    assert isinstance(template, PromptTemplate)
    assert "Custom question: {question}" in template.template

def test_invoke(model):
    model.load_llm()
    response = model.invoke(prompt="What is AI?")
    assert isinstance(response, str)

def test_invoke_exception(model):
    model.load_llm()
    response = model.invoke(prompt="What is AI?")
    assert isinstance(response, str)
