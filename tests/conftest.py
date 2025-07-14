import os
import pytest
import boto3
from time import sleep

def wait_for_table(dynamodb, table_name, timeout=10):
    table = dynamodb.Table(table_name)
    for _ in range(timeout):
        table.load()
        if table.table_status == "ACTIVE":
            return
        sleep(1)
    raise RuntimeError(f"Table {table_name} not ACTIVE after {timeout} seconds")

@pytest.fixture(scope="session", autouse=True)
def setup_dynamodb_tables():
    # Connect to local DynamoDB
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv("DYNAMODB_REGION", "us-east-1"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "dummy"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "dummy")
    )

    # Create Licenses table
    try:
        dynamodb.create_table(
            TableName=os.getenv("DYNAMODB_TABLE", "Licenses"),
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
        print("Created table: Licenses")
    except Exception as e:
        if "Table already exists" in str(e):
            print("Table Licenses already exists.")
        else:
            print(f"Error creating Licenses table: {e}")
    wait_for_table(dynamodb, os.getenv("DYNAMODB_TABLE", "Licenses"))

    # Create Users table
    try:
        dynamodb.create_table(
            TableName="Users",
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
        print("Created table: Users")
    except Exception as e:
        if "Table already exists" in str(e):
            print("Table Users already exists.")
        else:
            print(f"Error creating Users table: {e}")
    wait_for_table(dynamodb, "Users")

    yield 