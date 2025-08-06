# Use a newer and more secure version of the Python image (based on Debian Bookworm)
FROM python:3.11-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Update the package lists and apply any security upgrades to the base image
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of your application code into the container
COPY ./app /app/app

# Command to run your application when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
