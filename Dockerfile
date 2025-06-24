FROM python:3.10-alpine

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY book_reader.py /app/book_reader.py

CMD ["python3", "book_reader.py"]