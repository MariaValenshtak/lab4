FROM python:3.12

WORKDIR /Valenshtak

COPY . /Valenshtak

RUN pip install googletrans==3.1.0a0

CMD ["python", "gtrans3.py"]