# Use a lightweight Python image as a base for the container
FROM python:3.13-slim

# Create a virtual environment inside the container  
# RUN only makes temporary changes during the build, but filesystem changes (like creating a venv) persist in the image
RUN python -m venv /venv

# Modify PATH in the container to prioritize the virtual environment’s Python and pip  
# ENV makes this change persist for all future container commands  
# We do this instead of using `source /venv/bin/activate`, which doesn’t persist across Dockerfile steps  
ENV PATH="/venv/bin:$PATH"

# Install required frameworks/libraries/modules inside the virtual environment
RUN pip install "django<6" gunicorn whitenoise

# Copy the src directory from the host machine into the container
COPY src /src

# Set the working directory of the container
WORKDIR /src

# Applies all migrations to build or update the database schema
RUN python manage.py migrate --noinput

# Start Gunicorn a WSGI production server, binding to 0.0.0.0:8888, this will serve the Django application.
# Specify the WSGI application location, which initialises the Django app and handles communication
# between Gunicorn and Django.
CMD gunicorn --bind 0.0.0.0:8888 superlists.wsgi:application


