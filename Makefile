install: 
	poetry install 
lint: 
	pylint --disable=R,C app.py
test: 
	python -m pytest -vv --cov=app test_app.py