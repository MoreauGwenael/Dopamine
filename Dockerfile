FROM python:3.10-buster AS base_buster

RUN apk add --update alpine-sdk
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base_buster AS base
COPY dopamine dopamine
ENTRYPOINT ["python", "-m", "dopamine"]
