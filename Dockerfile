# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install kaggle pandas tqdm

COPY upload_kaggle.py upload_kaggle.py

COPY word_order.py word_order.py

COPY tokenized.p tokenized.p

COPY patterns/dataset-metadata.json patterns/dataset-metadata.json

CMD [ "python3", "-m" , "upload_kaggle"]