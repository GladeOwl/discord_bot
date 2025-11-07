FROM python:3.12-slim

COPY /bot /bot
WORKDIR /bot

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]