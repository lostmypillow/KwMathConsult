FROM python:3.12

RUN apt-get update -y

RUN apt-get install -y python3-tk


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "main"]