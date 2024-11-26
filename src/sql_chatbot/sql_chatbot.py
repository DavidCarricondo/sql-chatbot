from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from sql_chatbot.model import LlmModel
from langchain_core.prompts import PromptTemplate
from typing import Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

db = SQLDatabase.from_uri("sqlite:////home/dacs00/projects/sql-chatbot/db/dataset01.db")

def load_sql_template(template: Optional[str] = None) -> PromptTemplate:
    if template is None:
        template = '''Given a question, create a syntactically correct {dialect} query to run. With {top_k} results per select statement.
        Use the following format:

        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"

        Only use the following tables:

        {table_info}.

        Question: {input}'''
    return PromptTemplate.from_template(template)

def load_llm_model(model_path: str) -> LlmModel:
    llm_model = LlmModel(model_path=model_path)
    llm_model.load_llm()
    return llm_model.llm

def load_sql_chain() -> create_sql_query_chain:
    llm = load_llm_model("../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    prompt = load_sql_template()
    return create_sql_query_chain(llm, db, prompt, k=1)

def invoke_sql_chain(question: dict) -> str:
    chain = load_sql_chain()
    return chain.invoke(question)

def invoke_sql_chain_with_validation(question: dict) -> str:

    chain = load_sql_chain()
    llm = load_llm_model("../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf")


    system = """Double check the user's {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins

    If there are any of the above mistakes, rewrite the query.
    If there are no mistakes, just reproduce the original query with no further commentary.

    Output the final SQL query only."""

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{query}")]
    ).partial(dialect=db.dialect)

    validation_chain = prompt | llm | StrOutputParser()

    full_chain = {"query": chain} | validation_chain    
    return full_chain.invoke_with_validation(question)

if __name__ == "__main__":
    question = {"question": "Cuantos clientes hay?"}
    response = invoke_sql_chain_with_validation(question)
    print(response)
