# Use the official Python 3.11 image as the base image
FROM python:3.11.5

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requiremnts.txt requiremnts.txt

# Install the project dependencies
RUN pip install -r requiremnts.txt

# Copy the Django project files into the container
COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN  python manage.py crontab add


