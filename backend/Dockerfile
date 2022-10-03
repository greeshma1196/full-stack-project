FROM python:3.9.14-alpine3.16

WORKDIR /backend

COPY /backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /backend .

EXPOSE 5000

ENTRYPOINT ["python3", "-u", "main.py"]