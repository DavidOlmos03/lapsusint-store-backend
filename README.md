# LapsusINt Store Backend

A professional FastAPI backend for managing software licenses and users, using AWS DynamoDB as the database. Includes JWT-based authentication, user roles, and Docker support for both development and production environments.

## Features
- CRUD for Licenses
- CRUD for Users with Roles (admin, dev, user)
- JWT Access Token Authentication
- AWS DynamoDB support (local and cloud)
- Docker and Docker Compose support
- Professional, modular project structure

## Requirements
- Docker and Docker Compose
- AWS CLI (for production with AWS DynamoDB)

## Quick Start with Docker

### Development Environment (with local DynamoDB)

1. Clone the repository
```bash
git clone <repo-url>
cd LapsusINt-Store-Backend
```

2. Start the development environment
```bash
docker-compose up --build
```

This will start:
- FastAPI application on http://localhost:8000
- Local DynamoDB instance on port 8000 (internal)

3. Access the API
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Production Environment (with AWS DynamoDB)

1. Configure AWS credentials
```bash
aws configure
```

2. Set up environment variables
```bash
cp env.production .env
# Edit .env with your production values
```

3. Start production environment
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Manual Setup (without Docker)

### 1. Create and activate the virtual environment
```bash
python3 -m venv venv_lapsusint
source venv_lapsusint/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

#### For Development (with local DynamoDB):
```bash
cp env.development .env
```

#### For Production (with AWS DynamoDB):
```bash
cp env.production .env
```

Then edit the `.env` file with your specific values:
```env
ENV=development  # or production
DYNAMODB_REGION=us-east-1
DYNAMODB_TABLE=Licenses
DYNAMODB_ENDPOINT_URL=http://localhost:8000  # Only for development
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the application
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get access token
- `POST /auth/register` - Register new user

### Users
- `GET /users/` - Get all users
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Licenses
- `GET /licenses/` - Get all licenses
- `POST /licenses/` - Create new license
- `GET /licenses/{license_id}` - Get specific license
- `PUT /licenses/{license_id}` - Update license
- `DELETE /licenses/{license_id}` - Delete license

## Project Structure
```
LapsusINt-Store-Backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── license.py
│   │   ├── user.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── license.py
│   │   └── user.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── dynamodb.py
│   ├── models/
│   │   ├── license.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── license.py
│   │   └── user.py
│   └── main.py
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── .dockerignore
├── env.development
├── env.production
├── .gitignore
└── README.md
```

## Database Setup

### Development (Local DynamoDB)
The Docker Compose setup automatically starts a local DynamoDB instance. The application will create the necessary tables on startup.

### Production (AWS DynamoDB)
1. Configure AWS credentials
2. The application will create DynamoDB tables automatically on startup
3. Ensure your AWS user has the necessary DynamoDB permissions

## Docker Commands

### Development
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

### Production
```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment (development/production) | development |
| `DYNAMODB_REGION` | AWS DynamoDB region | us-east-1 |
| `DYNAMODB_TABLE` | DynamoDB table name for licenses | Licenses |
| `DYNAMODB_ENDPOINT_URL` | Local DynamoDB endpoint (development only) | None |
| `SECRET_KEY` | JWT secret key | supersecret |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | 30 |

## License
MIT 