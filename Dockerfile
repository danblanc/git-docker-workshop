FROM python:3.9

RUN apt-get update && \
    apt-get install -y --no-install-recommends 

WORKDIR /app

COPY requirements.txt *.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "my-script.py"]