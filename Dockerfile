FROM python:3.8.9-slim

WORKDIR app

COPY . .

RUN pip install -r requirements.txt

CMD ["run.py"]
ENTRYPOINT ["python"]