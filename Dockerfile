# Use an official Python runtime as a parent image
FROM python:3.11.5-alpine3.18

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV NAME streamstorm

# Run your Python script when the container launches
CMD ["python", "app.py"]
