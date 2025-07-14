#!/usr/bin/env python3
"""
Script to populate DynamoDB with test data for LapsusINt Store Backend
"""

import boto3
import uuid
from datetime import datetime
from app.core.security import get_password_hash
from app.models.user import UserRole
import os
from decimal import Decimal

# Test data for licenses
LICENSES_DATA = [
    {
        "product_name": "Steam Account - Cyberpunk 2077",
        "description": "Premium Steam account with Cyberpunk 2077 and all DLCs included",
        "price": 29.99,
        "supported_platforms": "Windows, macOS",
        "supported_launchers": "Steam",
        "recommendations": "High-end gaming PC recommended",
        "product_version": "2.0",
        "has_spoofer": True,
        "language": "English, Spanish",
        "stock_quantity": 15,
        "is_active": True,
        "image_url": "https://example.com/cyberpunk.jpg",
        "category": "Gaming"
    },
    {
        "product_name": "Epic Games - Fortnite Battle Pass",
        "description": "Epic Games account with Fortnite Battle Pass and exclusive skins",
        "price": 19.99,
        "supported_platforms": "Windows, macOS, PlayStation, Xbox",
        "supported_launchers": "Epic Games",
        "recommendations": "Stable internet connection required",
        "product_version": "Season 5",
        "has_spoofer": False,
        "language": "English",
        "stock_quantity": 25,
        "is_active": True,
        "image_url": "https://example.com/fortnite.jpg",
        "category": "Gaming"
    },
    {
        "product_name": "Origin - FIFA 24 Ultimate Edition",
        "description": "Origin account with FIFA 24 Ultimate Edition and bonus content",
        "price": 89.99,
        "supported_platforms": "Windows, macOS",
        "supported_launchers": "Origin",
        "recommendations": "8GB RAM minimum",
        "product_version": "2024",
        "has_spoofer": True,
        "language": "English, Spanish, French",
        "stock_quantity": 8,
        "is_active": True,
        "image_url": "https://example.com/fifa24.jpg",
        "category": "Sports"
    },
    {
        "product_name": "Battle.net - Call of Duty: Warzone",
        "description": "Battle.net account with Call of Duty: Warzone and battle pass",
        "price": 39.99,
        "supported_platforms": "Windows, PlayStation, Xbox",
        "supported_launchers": "Battle.net",
        "recommendations": "16GB RAM recommended",
        "product_version": "Season 3",
        "has_spoofer": True,
        "language": "English",
        "stock_quantity": 12,
        "is_active": True,
        "image_url": "https://example.com/warzone.jpg",
        "category": "FPS"
    },
    {
        "product_name": "Uplay - Assassin's Creed Valhalla",
        "description": "Uplay account with Assassin's Creed Valhalla and season pass",
        "price": 59.99,
        "supported_platforms": "Windows, PlayStation, Xbox",
        "supported_launchers": "Uplay",
        "recommendations": "SSD recommended for faster loading",
        "product_version": "Complete Edition",
        "has_spoofer": False,
        "language": "English, Spanish",
        "stock_quantity": 6,
        "is_active": True,
        "image_url": "https://example.com/valhalla.jpg",
        "category": "Action-Adventure"
    }
]

# Test data for users
USERS_DATA = [
    {
        "username": "admin",
        "email": "admin@lapsusint.com",
        "password": "admin123",
        "role": UserRole.admin,
        "is_active": True
    },
    {
        "username": "developer",
        "email": "dev@lapsusint.com",
        "password": "dev123",
        "role": UserRole.dev,
        "is_active": True
    },
    {
        "username": "user1",
        "email": "user1@example.com",
        "password": "user123",
        "role": UserRole.user,
        "is_active": True
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "password": "user123",
        "role": UserRole.user,
        "is_active": True
    },
    {
        "username": "moderator",
        "email": "mod@lapsusint.com",
        "password": "mod123",
        "role": UserRole.dev,
        "is_active": True
    }
]

def connect_to_dynamodb():
    """Connect to DynamoDB (local or AWS)"""
    # Check if we're in development mode
    if os.getenv("ENV") == "development" and os.getenv("DYNAMODB_ENDPOINT_URL"):
        # Local DynamoDB
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("DYNAMODB_REGION", "us-east-1"),
            endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL"),
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy'
        )
    else:
        # AWS DynamoDB
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("DYNAMODB_REGION", "us-east-1")
        )
    
    return dynamodb

def create_licenses_table(dynamodb):
    table_name = os.getenv("DYNAMODB_TABLE", "Licenses")
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        print(f"🛠️  Creating table: {table_name}")
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'license_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'license_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print(f"✅ Table {table_name} created.")
    else:
        print(f"ℹ️  Table {table_name} already exists.")

def create_users_table(dynamodb):
    table_name = "Users"
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        print(f"🛠️  Creating table: {table_name}")
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'username', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'username-index',
                    'KeySchema': [
                        {'AttributeName': 'username', 'KeyType': 'HASH'}
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print(f"✅ Table {table_name} created.")
    else:
        print(f"ℹ️  Table {table_name} already exists.")

def seed_licenses(dynamodb):
    """Seed licenses table with test data"""
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE", "Licenses"))
    
    print("🌱 Seeding licenses table...")
    
    for license_data in LICENSES_DATA:
        license_id = str(uuid.uuid4())
        item = {
            "license_id": license_id,
            "product_name": license_data["product_name"],
            "description": license_data["description"],
            "price": Decimal(str(license_data["price"])),
            "supported_platforms": license_data["supported_platforms"],
            "supported_launchers": license_data["supported_launchers"],
            "recommendations": license_data["recommendations"],
            "product_version": license_data["product_version"],
            "has_spoofer": license_data["has_spoofer"],
            "language": license_data["language"],
            "stock_quantity": license_data["stock_quantity"],
            "is_active": license_data["is_active"],
            "image_url": license_data["image_url"],
            "category": license_data["category"],
            "create_at": datetime.utcnow().isoformat(),
            "update_at": datetime.utcnow().isoformat()
        }
        
        try:
            table.put_item(Item=item)
            print(f"✅ Added license: {license_data['product_name']}")
        except Exception as e:
            print(f"❌ Error adding license {license_data['product_name']}: {e}")

def seed_users(dynamodb):
    """Seed users table with test data"""
    table = dynamodb.Table("Users")
    
    print("👥 Seeding users table...")
    
    for user_data in USERS_DATA:
        user_id = str(uuid.uuid4())
        item = {
            "user_id": user_id,
            "username": user_data["username"],
            "email": user_data["email"],
            "hashed_password": get_password_hash(user_data["password"]),
            "role": user_data["role"].value,
            "is_active": user_data["is_active"],
            "create_at": datetime.utcnow().isoformat(),
            "update_at": datetime.utcnow().isoformat()
        }
        
        try:
            table.put_item(Item=item)
            print(f"✅ Added user: {user_data['username']} ({user_data['role'].value})")
        except Exception as e:
            print(f"❌ Error adding user {user_data['username']}: {e}")

def main():
    """Main function to seed the database"""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    print("🚀 Starting database seeding...")
    
    try:
        # Connect to DynamoDB
        dynamodb = connect_to_dynamodb()
        print("✅ Connected to DynamoDB")
        
        # Create tables if they don't exist
        create_licenses_table(dynamodb)
        create_users_table(dynamodb)
        
        # Seed data
        seed_licenses(dynamodb)
        seed_users(dynamodb)
        
        print("\n🎉 Database seeding completed successfully!")
        print("\n📋 Test accounts created:")
        print("   Admin: admin / admin123")
        print("   Developer: developer / dev123")
        print("   User: user1 / user123")
        print("   User: user2 / user123")
        print("   Moderator: moderator / mod123")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")

if __name__ == "__main__":
    main() 