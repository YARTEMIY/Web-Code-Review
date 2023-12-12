FROM joyzoursky/python-chromedriver

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]