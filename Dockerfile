FROM python:3.10

WORKDIR /.
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

