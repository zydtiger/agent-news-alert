# Agent News Alert

Agent News Alert is a Python-based project that ingests RSS feeds, evaluates them using an LLM agent to prioritize news, and sends an email summary to the user. The project is managed with Poetry for dependency management and supports both development and production environments.

## How It Works

1. **Ingestion**:

   - Reads RSS feeds from `/src/conf/sources.json`.

2. **Evaluation**:

   - Uses an LLM agent to evaluate and prioritize articles based on the configuration in `/src/conf/agents.yml`.

3. **Email Notification**:

   - Sends a daily email at **9:00 AM (New York time)** with the top-priority articles to the user, as defined in `/src/conf/secrets.py`.

## Installation and Usage

### Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (for production)
- Set up `/src/conf/secrets.py` with fields listed in `/src/conf/secrets.template.py`

### Development Mode

1. **Install Poetry**:

   ```bash
   pip install poetry
   ```

2. **Install Dependencies**:
   Run the following command to install project dependencies. Poetry will automatically create a virtual environment in a temporary folder:

   ```bash
   poetry install
   ```

3. **Run the Application**:
   To run the application in development mode:

   ```bash
   poetry run python main.py
   ```

### Production Mode

1. **Build and Run with Docker**:
   To run the application in production mode, use Docker Compose:

   ```bash
   docker compose up -d
   ```

2. **Details**:
   - This will create a Docker container named `news_alert`.
   - The application will automatically send an email every day at **9:00 AM (New York time)**.

## Configuration

### RSS Feeds

- RSS feeds are defined in `/src/conf/sources.json`.
- Add or update sources in this file to customize the feeds ingested by the application.

### LLM Agent

- The agent configuration is defined in `/src/conf/agents.yml`.
- This file determines the model and prompt used by the LLM agent.

### Secrets

- User-specific secrets (e.g., email credentials) are defined in `/src/conf/secrets.py`.
- This file is ignored by Git for security purposes. Use the template file `/src/conf/secrets.template.py` to create your own `secrets.py`.
