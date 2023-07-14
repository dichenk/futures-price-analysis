FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py db_func.py ./
CMD ["python", "-u", "main.py"]
