#!/bin/bash

echo "🚀 Initializing LapsusINt Store Backend..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from env.development..."
    cp env.development .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

# Build and start the development environment
echo "🔨 Building and starting development environment..."
docker compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 15

# Check if the application is running
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Application is running successfully!"
    
    # Seed the database with test data
    echo "🌱 Seeding database with test data..."
    ./scripts/seed_docker.sh
    
    echo ""
    echo "🌐 Access your application:"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo "   - Health Check: http://localhost:8000/health"
    echo ""
    echo "📋 Test accounts created:"
    echo "   - Admin: admin / admin123"
    echo "   - Developer: developer / dev123"
    echo "   - User: user1 / user123"
    echo "   - User: user2 / user123"
    echo "   - Moderator: moderator / mod123"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker compose logs -f"
    echo "   - Stop services: docker compose down"
    echo "   - Restart: docker compose restart"
    echo "   - Re-seed data: ./scripts/seed_docker.sh"
else
    echo "❌ Application failed to start. Check logs with: docker compose logs"
    exit 1
fi 