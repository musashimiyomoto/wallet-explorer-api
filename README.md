[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/wallet-explorer-api/actions/workflows/ci.yml/badge.svg)](https://github.com/musashimiyomoto/wallet-explorer-api/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Wallet Explorer API

## Prerequisites

- **Docker & Docker Compose** - for containerized development
- **Poetry** - for local development and dependency management

## Setup

1. Clone the repository
2. Create environment file:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   # Using development script (recommended)
   ./dev.sh install

   # Or manually
   poetry install --with dev,test
   pre-commit install
   ```

## Quick Start

The fastest way to get started is using our unified development script:

```bash
# Make script executable (first time only)
chmod +x dev.sh

# Run full development cycle: install dependencies, format code, check lint, run tests, and build Docker
./dev.sh

# Or run specific operations:
./dev.sh install    # Install dependencies with Poetry
./dev.sh format     # Format code with isort and black
./dev.sh check      # Check code formatting and lint (ruff + pyright)
./dev.sh test       # Run tests with pytest and coverage
./dev.sh build      # Build and run Docker Compose

# Get help with all available commands:
./dev.sh help

# Database migrations:
./dev.sh migrate generate "Add user table"   # Generate new migration
./dev.sh migrate upgrade                     # Apply all pending migrations
./dev.sh migrate downgrade                   # Rollback last migration
./dev.sh migrate downgrade base              # Rollback to base
./dev.sh migrate history                     # Show migration history
./dev.sh migrate current                     # Show current migration
```

## Docker Development (Recommended)

### Starting the Application

```bash
# Using development script (recommended)
./dev.sh build

# Or manually
docker-compose up --build
```

### Accessing Services

After successful launch:
- **API**: http://localhost:8000
- **DB UI**: http://localhost:8080
  - System: PostgreSQL
  - Server: db
  - Username: postgres
  - Password: postgres
  - Database: explorer
- **Broker UI**: http://localhost:3000
- **Redis UI**: http://localhost:5540

### Docker Commands

```bash
# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f api

# Execute commands in running container
docker-compose exec api bash
```

## Local Development

### Database Migrations

The development script automatically handles environment switching for migrations:

```bash
# Generate new migration
./dev.sh migrate generate "Add user table"

# Apply all pending migrations
./dev.sh migrate upgrade

# Show migration history
./dev.sh migrate history

# Show current migration
./dev.sh migrate current

# Rollback last migration
./dev.sh migrate downgrade

# Rollback to specific migration or base
./dev.sh migrate downgrade base
```

### Code Formatting & Quality Checks

```bash
# Format code (isort + black)
./dev.sh format

# Check code formatting and lint (black --check, isort --check, ruff, pyright)
./dev.sh check

# Or manually
poetry run isort .
poetry run black .
poetry run ruff check .
poetry run pyright .
```

### Running Tests

```bash
# Using development script (includes coverage reports)
./dev.sh test

# Or manually with coverage
poetry run pytest -v --cov=. --cov-report=term-missing --cov-report=xml

# Simple test run
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_api/test_admin/ -v
```
