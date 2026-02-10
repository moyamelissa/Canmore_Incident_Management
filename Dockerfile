# Use an official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose ports (adjust if needed)
EXPOSE 5000 8001

# Start both servers using supervisord
RUN pip install supervisor
COPY supervisord.conf /etc/supervisord.conf

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
