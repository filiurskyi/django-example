# Description

The project is a Django application designed to provide a platform for managing and displaying quotes. It includes functionalities such as storing quotes in a database, retrieving and displaying them on a webpage, and asynchronous task handling using Celery.

# Setup

## Prerequisites

- Docker
- Docker Compose

# Installation

Clone the repository:

```bash
git clone https://github.com/filiurskyi/django-example
```

Navigate to the project directory:

```bash
cd django-example
```

Rename file `.env.dist` into `.env` and specify your **development environment** variables. Here's an example:

```plaintext
DJANGO_SECRET_KEY=<your_secret_key>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<pg-password>
POSTGRES_DB=postgres
REDIS_HOST=redis
REDIS_PORT=6379
```

Build and start the Docker containers:

```bash
docker-compose up --build
```

# Usage
Once the setup is complete, you can access the Django development server at http://localhost:8000.

## Scripts and Commands

The start.sh script automates the setup process and starts the Django development server and Celery worker. Here's how to use it:

```bash
./start.sh
```

## Docker Compose Configuration (docker-compose.yml)
The docker-compose.yml file defines the services required for the project, including Redis, PostgreSQL, and Django. To start the containers defined in this file, run:

```bash
docker-compose up
```

Dockerfile
The Dockerfile sets up the environment for running the Django application. It installs the necessary dependencies and sets the entry point to start.sh. To build the Docker image, use:

```bash
docker build -t your-image-name .
```

## Requirements

The requirements.txt file lists all Python dependencies required for the project. To install these dependencies, run:

```bash
pip install -r requirements.txt
```

# Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.

# License
This project is licensed under the MIT License.
