from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from sql_chatbot.modulos.model import LlmModel
from langchain_core.prompts import PromptTemplate
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from sql_chatbot.types_ import OutputSqlJson
import re
import pandas as pd
import sqlite3

class SQLChatbot:
    def __init__(self, db_uri: str, model_path: str):
        """
        A chatbot that generates and validates SQL queries based on user questions.
        Attributes:
            db (SQLDatabase): The SQL database connection.
            model_path (str): The path to the language model.
        """
        self.db = SQLDatabase.from_uri(db_uri)
        self.model_path = model_path

    @staticmethod
    def parse_result(text: str) -> str:
        """
        Parses the result text to extract JSON-like content.
        Args:
            text (str): The text to parse.
        Returns:
            str: The parsed text.
        """
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            parsed = match.group(0)
            parsed = re.sub(r'\{[^"]*"', '{"', parsed)
            return re.sub(r'"[^"]*\}', '"}', parsed) 
        else:
            return text


    def load_sql_template(self, template: Optional[str] = None) -> PromptTemplate:
        """
        Loads the SQL template for generating queries.
        Args:
            template (Optional[str]): The template string. Defaults to None.
        Returns:
            PromptTemplate: The loaded prompt template.
        """
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

    def load_llm_model(self) -> LlmModel:
        """
        Loads the language model.
        Returns:
            LlmModel: The loaded language model.
        """
        llm_model = LlmModel(model_path=self.model_path)
        llm_model.load_llm()
        return llm_model.llm

    def load_sql_chain(self) -> create_sql_query_chain:
        """
        Loads the SQL query chain.
        Returns:
            create_sql_query_chain: The created SQL query chain.
        """
        llm = self.load_llm_model()
        prompt = self.load_sql_template()
        return create_sql_query_chain(llm, self.db, prompt, k=1)

    def invoke_sql_chain(self, question: dict) -> str:
        """
        Invokes the SQL query chain with a given question.
        Args:
            question (dict): The question to process.
        Returns:
            str: The generated SQL query.
        """
        chain = self.load_sql_chain()
        return chain.invoke(question)

    def invoke_sql_chain_with_validation(self, question: dict) -> str:
        """
        Invokes the SQL query chain with validation for common SQL mistakes.
        Args:
            question (dict): The question to process.
        Returns:
            str: The validated SQL query.
        """
        chain = self.load_sql_chain()
        llm = self.load_llm_model()

        system = """Double check the user's {dialect} query for common mistakes, including:
        - Using NOT IN with NULL values
        - Using UNION when UNION ALL should have been used
        - Using BETWEEN for exclusive ranges
        - Data type mismatch in predicates
        - Properly quoting identifiers
        - Using the correct number of arguments for functions
        - Casting to the correct data type
        - Using the proper columns for joins

        If there are any mistakes, rewrite the query.
        If there are no mistakes, just reproduce the original query with no further commentary.

        Respond exclusively in a JSON object with the following format:

        {{
            "SQLQuery": "corrected query",
        }}
        
        Never include explanations or additional text, only the JSON.
        query: {query}
        """

#        prompt = ChatPromptTemplate.from_messages(
#            [("system", system), ("human", "{query}")]
#        ).partial(dialect=self.db.dialect)
        prompt = PromptTemplate.from_template(system).partial(dialect=self.db.dialect)


        parser = JsonOutputParser(pydantic_object=OutputSqlJson)

        validation_chain = prompt | llm | self.parse_result | parser

        full_chain = {"query": chain} | validation_chain    
        
        result = full_chain.invoke(question)
        print(result)
        return result

    def run_query(self, query: str) -> str:
        """
        Runs the SQL query on the database and returns the result.
        Args:
            query (str): The SQL query to run.
        Returns:
            str: The result of the SQL query.
        """
        con = sqlite3.connect('/home/dacs00/projects/sql-chatbot/db/dataset01.db')
        df = pd.read_sql_query(query["SQLQuery"], con)
        con.close()
        return {"SQLQuery": query["SQLQuery"],
                "ANSWER": df.to_string(index=False)
                }
    
    def run(self, question:dict, validation: bool = True):
        """
        Runs the chatbot with a given question and optional validation.
        Args:
            question (dict): The question to process.
            validation (bool): Whether to validate the SQL query. Defaults to True.
        Returns:
            str: The result of the SQL query.
            """
        if validation:
            response = self.invoke_sql_chain_with_validation(question)
        else:
            response = self.invoke_sql_chain(question)
            response = {"SQLQuery": response}
        return self.run_query(response)


if __name__ == "__main__":
    chatbot = SQLChatbot(db_uri="sqlite:////home/dacs00/projects/sql-chatbot/db/dataset01.db", 
                         model_path="../models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
                         )
    question = {"question": "Cuanto es la suma de todos los importes?"} # #"Cuantos clientes hay?"
    response = chatbot.run(
        question, 
        validation=False
        )
    print("*** Response ***")
    print(response)



