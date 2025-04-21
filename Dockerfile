FROM python:3.9-alpine

WORKDIR /app

# Install bash (because Alpine uses sh by default)
RUN apk update && apk add bash

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure wait-for-it.sh is copied and executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Use python3 explicitly instead of python
CMD ["python3", "main.py"]
