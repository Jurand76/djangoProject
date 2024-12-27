# Use official image of Python
FROM python:3.10-slim

# Working directory in container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from project
COPY . .

# Set environment Django_settings_module
ENV DJANGO_SETTINGS_MODULE=djangoProject.settings

# Expose port 8000
EXPOSE 8000

# Run Django server
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:$PORT"]