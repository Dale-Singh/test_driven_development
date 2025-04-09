# Use a lightweight Python image as a base for the container
FROM python:3.13-slim

# Create a system group and a user called 'nonroot' with limited access before copying files
# This avoids running the container as root, which is a security risk
RUN addgroup --system nonroot && adduser --system --no-create-home --disabled-password --group nonroot

# Create a virtual environment inside the container
# RUN only makes temporary changes during the build, but filesystem changes (like creating a venv) persist in the image
RUN python -m venv /venv

# Modify PATH in the container to prioritize the virtual environment’s Python and pip  
# ENV makes this change persist for all future container commands  
# We do this instead of using `source /venv/bin/activate`, which doesn’t persist across Dockerfile steps  
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file from the host machine into the container
COPY requirements.txt requirements.txt

# Install required frameworks/libraries/modules inside the virtual environment
RUN pip install -r requirements.txt

# Copy the project source code and set ownership to nonroot, required to inherit 
# read.write privileges to db.sqlite3 and other files
COPY --chown=nonroot:nonroot src /src

# Set the working directory of the container
WORKDIR /src

# Collect static files, this is required as Whitenoise does not auto-discover static files in production
RUN python manage.py collectstatic

# Set an environment variable, works with settings.py to initialise a production environment
ENV DJANGO_DEBUG_FALSE=1

# Applies all migrations to build or update the database schema
# RUN python manage.py migrate --noinput

# **SECURITY: Avoid running the container as root**
# By default, Docker containers run as the root user, which is a security risk.
# If an attacker gains control, they would have unrestricted access inside the container,
# potentially modifying system files or escalating privileges.
# Instead, we create a new non-root user (`nonroot`) to limit potential damage.
# This user has restricted permissions and only the necessary access to run the application.

# Switch to the non-root user
USER nonroot

# Start Gunicorn a WSGI production server, binding to 0.0.0.0:8888, this will serve the Django application.
# Specify the WSGI application location, which initialises the Django app and handles communication
# between Gunicorn and Django
CMD gunicorn --bind 0.0.0.0:8888 superlists.wsgi:application
