FROM python:3.8

WORKDIR /usr/src/backend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py", "0.0.0.0"]