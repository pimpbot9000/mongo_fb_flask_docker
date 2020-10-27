FROM python:3.8.5-alpine3.12
WORKDIR /usr/app
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev linux-headers 
RUN pip install -r requirements.txt
ENV FLASK_ENV=development
COPY app.py .
COPY database database
EXPOSE 5000
CMD flask run --host=0.0.0.0
