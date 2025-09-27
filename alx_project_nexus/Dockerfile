# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (for Gunicorn)
EXPOSE 8000

# Run Gunicorn (production server)
CMD ["gunicorn", "alx_project_nexus.wsgi:application", "--bind", "0.0.0.0:8000"]
