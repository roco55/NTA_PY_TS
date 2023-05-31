FROM python:3.10-buster

COPY . .

RUN pip install numpy

ENTRYPOINT ["python", "src/main.py"]