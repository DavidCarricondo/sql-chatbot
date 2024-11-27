
template_sql = '''Given a question, create a syntactically correct {dialect} query to run. With {top_k} results per select statement.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"

    Only use the following tables:

    {table_info}.

    Question: {input}'''

template_sql_validation = """Double check the user's {dialect} query for common mistakes, including:
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