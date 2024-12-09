FROM python:3.12.8-slim
LABEL maintainer="London App Developer LTD"

# Set environment variable to ensure output is flushed immediately
ENV PYTHONUNBUFFERED=1

# Copy the requirements file into the container
COPY ./requirements.txt /requirements.txt

# Install dependencies using apt-get (Debian-based)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    linux-libc-dev \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Create and set permissions for the /app directory
RUN mkdir /app && chown -R 1000:1000 /app

# Set the working directory to /app
WORKDIR /app

# Copy the app code into the container
COPY ./app /app

# Create a non-root user and set ownership of the app directory
RUN useradd -m user && chown -R user:user /app

# Switch to the non-root user
USER user

# Set the default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
