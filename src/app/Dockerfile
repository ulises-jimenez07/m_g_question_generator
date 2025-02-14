FROM python:3.12-slim

RUN apt-get update

WORKDIR /app
COPY src/app /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python",  "main.py"]
