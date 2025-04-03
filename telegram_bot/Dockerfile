FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip3 -r requirements.txt

COPY run.py .

CMD ["python3", "run.py"]

