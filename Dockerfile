#
FROM python:3.11.6


WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]

