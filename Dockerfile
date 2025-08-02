# Dockerfile for Smart Stock Trend Predictor
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port and run the app
EXPOSE 8050
CMD ["python", "app.py"]
