FROM python:3.9-slim

# Install dependencies required for psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code to the container
COPY . /app/

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0", "-p", "8000", "SaaS_Boilerplate.wsgi:application"]

