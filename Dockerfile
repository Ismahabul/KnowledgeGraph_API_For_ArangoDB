FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
