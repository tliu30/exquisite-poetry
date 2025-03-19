install:
	pip install -r requirements.txt

upgrade-db:
	flask db upgrade

deploy-dev:
	flask --debug run --port 5000

deploy-prod:
	flask run --host 0.0.0.0 --port 5000

