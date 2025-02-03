# Faculty Hours Payrolls Service

## Overview
The Faculty Hours Payrolls service is a microservice component of the Faculty Hours system, responsible for managing and processing faculty payroll data.

## Tech Stack
- **Python 3.11**
- **FastAPI** (v0.109.2) - Modern web framework for building APIs
- **GraphQL** with Strawberry (v0.237.3) - API query language
- **SQLAlchemy** (v2.0.35) - SQL toolkit and ORM
- **PostgreSQL** - Primary database (via psycopg2)
- **Pandas** (v2.2.3) - Data manipulation and analysis
- **Uvicorn** (v0.27.1) - ASGI server implementation
- **Docker** - Containerization
- **Poetry** - Dependency management

## Development Tools
- **Black** - Code formatting
- **isort** - Import sorting
- **pre-commit** - Git hooks framework
- **pytest** - Testing framework

## Setup Instructions

### Prerequisites
- Python 3.11
- Poetry
- Docker and Docker Compose
- PostgreSQL

### Local Development Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd faculty-hours-payrolls
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Configure the following variables:
     - Database connection settings
     - API endpoints for related services
     - Authentication settings

4. Run the service:
   ```bash
   poetry run uvicorn payrolls.main:app --reload
   ```

### Docker Setup
1. Build and run using Docker Compose:
   ```bash
   docker-compose -f .docker/docker-compose.yml up --build
   ```

## Service Connections
This service is part of the Faculty Hours system and interacts with:

1. **Faculty Hours Gateway**
   - Main gateway service that routes requests
   - Handles authentication and authorization

2. **Faculty Hours Report**
   - Receives payroll data for report generation
   - Exchanges faculty workload information

## API Documentation
- GraphQL endpoint: `/graphql`
- API documentation available at `/docs` (Swagger UI)
- GraphQL Playground available at `/graphql`
