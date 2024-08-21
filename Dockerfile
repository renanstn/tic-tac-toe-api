# =============================================================================
# Base
# =============================================================================
FROM python:3.9 AS base
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# =============================================================================
# Development
# =============================================================================
FROM base AS development
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY /src /app/
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]

# =============================================================================
# Production
# =============================================================================
FROM base AS production
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
COPY . /app/
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", ]
