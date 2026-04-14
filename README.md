# Timesheet Tracker - DevSecOps Demo Application

A simple FastAPI-based timesheet tracking application demonstrating DevSecOps principles at **Security Maturity Level 1** (baseline). This application allows users to register, authenticate, create projects, and log their daily working hours.

## Features

- **Health Check**: Simple endpoint to verify application status
- **User Authentication**: JWT-based authentication with bcrypt password hashing
- **Project Management**: Create and manage projects
- **Timesheet Tracking**: Log, update, and delete timesheet entries
- **Data Persistence**: SQLite database with SQLModel ORM
- **Input Validation**: Pydantic models for request validation
- **Role-Based Access**: Users can only access their own data
- **Containerization**: Docker and Docker Compose support
- **CI/CD**: GitHub Actions workflow for testing and linting

## Architecture

```
backend/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration management
│   ├── models.py         # SQLModel database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── db.py             # Database setup and session management
│   ├── auth.py           # JWT and password hashing utilities
│   ├── dependencies.py   # FastAPI dependencies
│   └── routers/          # API route handlers
│       ├── health.py
│       ├── auth.py
│       ├── projects.py
│       └── timesheets.py
├── tests/                # Pytest test suite
├── requirements.txt      # Python dependencies
└── pyproject.toml        # Project configuration and dev dependencies

Dockerfile               # Container image definition
docker-compose.yml       # Local development setup
.github/workflows/       # GitHub Actions CI/CD
README.md               # This file
Makefile                # Development convenience commands
```

## Prerequisites

- Python 3.9 or later
- pip or poetry
- Docker and Docker Compose (optional, for containerized deployment)
- curl or similar HTTP client for testing

## Quick Start

### Option 1: Local Development (Python Virtual Environment)

1. **Clone and change directory**:
   ```bash
   cd /path/to/Timesheet-tracker
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   make install-dev
   ```

4. **Set JWT_SECRET and run**:
   ```bash
   export JWT_SECRET="your-super-secret-key-change-in-production"
   make run
   ```

   Or manually:
   ```bash
   cd backend
   JWT_SECRET="your-secret-key" uvicorn app.main:app --reload
   ```

5. **Test the application**:
   Access the API documentation at: http://localhost:8000/docs

### Option 2: Using Docker Compose

1. **Start the application**:
   ```bash
   JWT_SECRET="your-secret-key" docker-compose up app
   ```

2. **Development mode with auto-reload**:
   ```bash
   JWT_SECRET="dev-secret" docker-compose up --profile dev app-dev
   ```

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `JWT_SECRET` | - | Yes | Secret key for signing JWT tokens. Must be set before app starts. |
| `JWT_ALGORITHM` | HS256 | No | Algorithm for JWT signing |
| `JWT_EXPIRATION_MINUTES` | 30 | No | JWT token expiration time in minutes |
| `DATABASE_URL` | sqlite:///./app.db | No | Database connection string |
| `DEBUG` | false | No | Enable debug logging |

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### Authentication

#### Register a new user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Projects (Requires Authentication)

#### Create a project
```bash
curl -X POST http://localhost:8000/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Q1 2024 website redesign project"
  }'
```

#### List user's projects
```bash
curl http://localhost:8000/projects \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get project details
```bash
curl http://localhost:8000/projects/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update a project
```bash
curl -X PUT http://localhost:8000/projects/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign - Updated"
  }'
```

#### Delete a project
```bash
curl -X DELETE http://localhost:8000/projects/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Timesheets (Requires Authentication)

#### Create a timesheet entry
```bash
curl -X POST http://localhost:8000/timesheets \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "date": "2024-01-15",
    "hours": 8.5,
    "note": "Completed frontend components"
  }'
```

#### List user's timesheet entries
```bash
curl http://localhost:8000/timesheets \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get timesheet entry
```bash
curl http://localhost:8000/timesheets/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update a timesheet entry
```bash
curl -X PUT http://localhost:8000/timesheets/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hours": 7.5,
    "note": "Updated note"
  }'
```

#### Delete a timesheet entry
```bash
curl -X DELETE http://localhost:8000/timesheets/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Running Tests

Run the test suite:
```bash
make test
```

Or manually:
```bash
cd backend
JWT_SECRET=test-secret pytest tests/ -v
```

Run tests with coverage:
```bash
make test-cov
```

## Linting and Code Formatting

Lint the code:
```bash
make lint
```

Format code:
```bash
make format
```

## Project Structure Details

### Models (SQLModel)
- **User**: Email, hashed password, timestamps
- **Project**: Name, description, user reference, timestamps
- **Timesheet**: Project reference, date, hours, note, user reference, timestamps

### Security Features (Level 1)
- ✅ Password hashing using bcrypt
- ✅ JWT token-based authentication
- ✅ Token expiration (30 minutes default)
- ✅ Role-based access (users see only their data)
- ✅ Input validation via Pydantic
- ✅ Parameterized database queries (ORM)
- ✅ Environment variable configuration
- ⏳ (Level 2+) SAST/SCA scanning
- ⏳ (Level 2+) DAST testing
- ⏳ (Level 2+) Secrets management
- ⏳ (Level 2+) SBOM generation

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push to `main` and pull request:

1. **Test on multiple Python versions** (3.9, 3.11)
2. **Linting** with ruff
3. **Unit tests** with pytest
4. **Artifact upload** for reports

## Docker Deployment

The application is containerized with a `Dockerfile` that:
- Uses Python 3.11 slim image
- Installs dependencies
- Runs as non-root user (UID 1000)
- Includes health check
- Exposes port 8000

### Build image manually
```bash
docker build -t timesheet-tracker:1.0.0 .
```

### Run container
```bash
docker run -e JWT_SECRET="your-secret" -p 8000:8000 timesheet-tracker:1.0.0
```

## Database

The application uses SQLite by default for simplicity. The database file is created as `app.db` in the working directory.

### Change database
Modify `DATABASE_URL` environment variable:
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql+pymysql://user:password@localhost/dbname`
- SQLite: `sqlite:///./app.db`

## Logging

Logs are output to stdout with the format:
```
2024-01-15 10:30:00,123 - app.routers.auth - INFO - New user registered: user@example.com
```

Configure log level with `DEBUG` environment variable.

## Troubleshooting

### JWT_SECRET not set error
```
ValueError: JWT_SECRET environment variable is required but not set.
```

**Solution**: Set the environment variable before running:
```bash
export JWT_SECRET="your-secret-key"
```

### Database lock error with SQLite
If using concurrent requests, consider upgrading to PostgreSQL for production.

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Development Workflow

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test: `make test`
3. Lint code: `make lint`
4. Commit and push
5. Create pull request
6. CI pipeline runs automatically
7. Merge when all checks pass

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Documentation](https://jwt.io/)
- [DevSecOps Best Practices](https://owasp.org/www-project-devsecops/)

## License

MIT License - See LICENSE file for details

## Notes for Future Levels

**Security Maturity Level 2+** will add:
- Static Application Security Testing (SAST)
- Software Composition Analysis (SCA)
- Dynamic Application Security Testing (DAST)
- Secret scanning and management
- Infrastructure as Code scanning
- Software Bill of Materials (SBOM)
- Code signing and attestation
- Policy-as-code enforcement
- Advanced logging and monitoring
- Rate limiting and DDoS protection
