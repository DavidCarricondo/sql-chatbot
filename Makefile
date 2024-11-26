install: 
	poetry install 
lint: 
	pylint --disable=R,C app.py
test: 
	poetry run pytest -vv tests