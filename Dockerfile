FROM python:3.12-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "waitress-serve", "--port", "5000", "app:app" ]
