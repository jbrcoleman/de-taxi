FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2 sqlalchemy pyarrow

WORKDIR /app
COPY upload-data.py upload-data.py

ENTRYPOINT [ "python", "upload-data.py" ]