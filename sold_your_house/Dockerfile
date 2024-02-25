# Image: python:latest
FROM python:latest

# Set the working directory in the container to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
