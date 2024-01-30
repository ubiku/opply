install:
	pip install -r .\requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate