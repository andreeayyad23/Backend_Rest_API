FROM python:3.12.8-slim
LABEL maintainer="London App Developer LTD"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Create a non-root user (for slim, using `useradd`)
RUN useradd -m user

# Set the user to `user` (ensure the user has access to the /app folder)
USER user

# Final command to run the app (adjust according to your app's entry point)
CMD ["python", "manage.py", "runserver"]
