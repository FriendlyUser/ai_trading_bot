FROM python:3.8.3-slim

WORKDIR /service/app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN apt-get update && apt-get install gcc npm -y && apt-get clean
RUN pip install --upgrade pip
# install dependencies
RUN pip install -r requirements.txt

COPY ai_trading_bot .

EXPOSE 8081

ENV PYTHONUNBUFFERED 1

HEALTHCHECK --timeout=30s --interval=1m30s --retries=5 \
  CMD curl -s --fail http://localhost:8081/_health || exit 1

CMD ["python3", "-u", "main.py"]
