FROM python:3.8-slim

WORKDIR /app

# Copy only requirements file first, to use Docker cache effectively
COPY app/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY app/ /app

# Run the application
CMD ["python", "app.py"]
