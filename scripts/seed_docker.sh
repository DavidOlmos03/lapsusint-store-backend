#!/bin/bash

echo "🌱 Seeding DynamoDB with test data..."

# Check if containers are running
if ! docker compose ps | grep -q "app-1"; then
    echo "❌ Application containers are not running. Please start them first with:"
    echo "   docker compose up -d"
    exit 1
fi

# Wait for DynamoDB to be ready
echo "⏳ Waiting for DynamoDB to be ready..."
sleep 10

# Run the seeding script inside the app container
echo "🚀 Running seeding script..."
docker compose exec -w /app app python -c "
import sys
sys.path.append('/app')
from scripts.seed_data import main
main()
"

echo "✅ Seeding completed!"
echo ""
echo "📋 You can now test the API with these accounts:"
echo "   - Admin: admin / admin123"
echo "   - Developer: developer / dev123"
echo "   - User: user1 / user123"
echo "   - User: user2 / user123"
echo "   - Moderator: moderator / mod123"
echo ""
echo "🌐 API Documentation: http://localhost:8000/docs" 