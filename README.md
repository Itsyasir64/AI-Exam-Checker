# AI Exam Checker

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# also install system deps: tesseract-ocr, poppler-utils
# edit .env (OPENAI_API_KEY, SECRET_KEY, DB_URL)
python manage.py makemigrations users exams grading
python manage.py migrate
python manage.py createsuperuser
redis-server &                                   # broker
celery -A config worker -l info &                # background grading
python manage.py runserver
```
