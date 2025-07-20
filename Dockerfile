# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# --- User and Permission Setup ---
# Add arguments for user and group IDs, with a default value
ARG PUID=1000
ARG PGID=1000

# Create a group and user with the specified IDs
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -s /bin/sh -m appuser

# --- Application Setup ---
# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# and set ownership to our new user
COPY . .
RUN chown -R appuser:appgroup /app

# Set the user to run the application
USER appuser

# Tell Docker that the container will listen on port 8000
EXPOSE 8000

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "app:app"]