install: 
	poetry install 
lint: 
	pylint --disable=R,C src/sql_chatbot/
test: 
	poetry run pytest -vv tests
run:
	fastapi dev src/sql_chatbot/app.py