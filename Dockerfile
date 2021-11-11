# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install .

CMD [ "python3", "-m", "scripts/run.py"]