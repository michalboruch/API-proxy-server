FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV API_URL=https://login.eagleeyenetworks.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./run.sh"]
