FROM python:3.8 AS bnp_test
COPY src/requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install -r requirements.txt
COPY src src