FROM python:3.7-alpine AS base_alpine

RUN apk add --update alpine-sdk
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base_alpine AS base
COPY dopamine dopamine
ENTRYPOINT ["python", "-m", "dopamine"]
