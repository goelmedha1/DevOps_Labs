FROM python:3.8-alpine

RUN pip install flask

WORKDIR /app

COPY randomapp.py .

ENTRYPOINT ["python", "randomapp.py"]