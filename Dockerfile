FROM python:3.13.11-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy the application code
COPY ./ /app/

# Install dependencies
RUN pip install uv
RUN uv sync --frozen

# Install cron task
RUN apt-get update && apt-get install -y cron && apt-get clean
RUN echo "0 9 * * * cd /app && /usr/local/bin/uv run python main.py >> /proc/1/fd/1 2>&1" > /etc/cron.d/news_alert
RUN chmod 644 /etc/cron.d/news_alert
RUN crontab /etc/cron.d/news_alert

# Start cron
CMD ["cron", "-f"]
