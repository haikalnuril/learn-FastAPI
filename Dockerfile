FROM python:3.10
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "fastapi", "run", "main.py", "--port", "8000" ]