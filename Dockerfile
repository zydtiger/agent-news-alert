FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the dependencies config into the container
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

# Install dependencies
RUN pip install poetry
RUN poetry install

# Copy the application code
COPY ./src /app

# Install cron task
RUN apt-get update && apt-get install -y cron && apt-get clean
RUN echo "0 9 * * * cd /app && /usr/local/bin/poetry run python main.py >> /proc/1/fd/1 2>&1" > /etc/cron.d/news_alert
RUN chmod 644 /etc/cron.d/news_alert
RUN crontab /etc/cron.d/news_alert

# Start cron
CMD ["cron", "-f"]
