FROM python:3.8

WORKDIR /usr/src/parser

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./parsing.py"]