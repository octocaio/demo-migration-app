# Demo Migration App

A realistic Python application demonstrating user authentication, database pooling, and API endpoints. This codebase is designed for code review and migration testing.

## Overview

The Demo Migration App provides:
- User authentication with password hashing and token management
- Database connection pooling for efficient resource management
- RESTful API endpoints for user management
- Utility functions for data validation and formatting

## Project Structure

```
demo-migration-app/
├── src/
│   ├── auth.py          # Authentication and token management
│   ├── database.py      # Database connection pooling
│   ├── api.py           # Flask API routes
│   └── utils.py         # Utility functions
├── tests/
│   └── test_auth.py     # Unit tests for auth module
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd demo-migration-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

Execute the test suite with pytest:

```bash
pytest tests/
```

Run with verbose output:
```bash
pytest tests/ -v
```

## Running the API

Start the Flask development server:

```bash
python src/api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns service status

### Users

- **GET** `/users` — List all users
- **POST** `/users` — Create new user
  - Request body: `{"username": "...", "email": "..."}`
- **GET** `/users/<id>` — Get user by ID
- **DELETE** `/users/<id>` — Delete user

## Modules

### auth.py
- `hash_password(password, salt)` — Hash password using SHA-256
- `verify_password(password, hash, salt)` — Verify password against stored hash
- `generate_salt()` — Generate cryptographic salt
- `TokenManager` — Manage JWT-like tokens with expiration and revocation

### database.py
- `DatabasePool` — Connection pool manager with configurable size
- `get_connection()` — Retrieve connection from pool
- `release_connection(conn)` — Return connection to pool

### api.py
- Flask application with CRUD endpoints for user management
- Error handling and JSON responses

### utils.py
- `validate_email(email)` — Validate email format
- `sanitize_input(text)` — Remove potentially dangerous characters
- `format_date(timestamp)` — Convert timestamp to ISO 8601 format
- `is_valid_username(username)` — Validate username format

## License

MIT
