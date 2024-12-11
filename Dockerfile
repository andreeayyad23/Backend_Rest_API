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
    libjpeg-dev \
    libpq-dev \
    musl-dev \
    zlib1g \
    zlib1g-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Create and set permissions for the /app directory
RUN mkdir /app && chown -R 1000:1000 /app

# Create media and static directories with proper permissions
RUN mkdir -p /web/media /web/static \
    && chown -R 1000:1000 /web/media /web/static \
    && chmod -R 755 /web/media /web/static

# Set the working directory to /app
WORKDIR /app

# Copy the app code into the container
COPY ./app /app

# Create a non-root user and set ownership of necessary directories
RUN useradd -m user && chown -R user:user /app /web/media /web/static

# Set volumes for media and static directories
VOLUME ["/web/media", "/web/static"]

# Switch to the non-root user
USER user

# Set the default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
