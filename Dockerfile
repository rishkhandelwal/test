# syntax=docker/dockerfile:1

# Use the recommended Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /chatbot-seema

COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]