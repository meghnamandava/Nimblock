FROM python:3.9-slim-buster

# Install dependencies
RUN pip install flask
RUN pip install gunicorn

# Copy app files to the container
COPY nimblock_api.py /app/nimblock_api.py

# Set working directory
WORKDIR /app

# Expose port 8080
EXPOSE 8080

# Start Flask app
#CMD ["python", "nimblock_api.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--timeout", "300", "nimblock_api:app"]
