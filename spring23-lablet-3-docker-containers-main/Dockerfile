FROM python:3.8-alpine

RUN pip install flask redis emoji

WORKDIR /app

COPY view_count.py .

ENTRYPOINT ["python", "view_count.py"]
