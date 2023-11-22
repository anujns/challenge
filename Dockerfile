# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Run app.py when the container launches
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
