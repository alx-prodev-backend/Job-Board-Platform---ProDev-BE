# Dockerfile

# 1. Base Image:
FROM python:3.11-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# 4. Set work directory
WORKDIR /app

# 5. Install dependencies
#  Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy project code
COPY . .

# 7. Set ownership of the app directory
RUN chown -R app:app /app

# 8. Switch to the non-root user
USER app

# 9. Expose the port Gunicorn will run on
EXPOSE 8000

# 10. Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "job_board_project.wsgi:application"]