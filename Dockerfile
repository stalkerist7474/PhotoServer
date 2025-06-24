FROM python:3.13.3-slim


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .


CMD ["gunicorn", "-k", "eventlet","-w 4", "-b 0.0.0.0:8000", "app:app"]