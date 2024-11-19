FROM python:3.9-slim

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory structure and set permissions
RUN mkdir -p /app/db && \
    chown -R www-data:www-data /app

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R www-data:www-data /app/db

# Run as non-root user for security
USER www-data

EXPOSE 5000

ENV FLASK_APP=app.app:app
ENV SQLITE_DATABASE_URI="sqlite:///db/database.db"

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]