import boto3
from app.core.config import settings

class DynamoDB:
    client = None
    resource = None

    def connect_to_dynamodb(self):
        if settings.ENV == "development" and settings.DYNAMODB_ENDPOINT_URL:
            # Use local DynamoDB for development
            self.client = boto3.client(
                'dynamodb', 
                region_name=settings.DYNAMODB_REGION,
                endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
            self.resource = boto3.resource(
                'dynamodb', 
                region_name=settings.DYNAMODB_REGION,
                endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            # Use AWS DynamoDB for production
            self.client = boto3.client('dynamodb', region_name=settings.DYNAMODB_REGION)
            self.resource = boto3.resource('dynamodb', region_name=settings.DYNAMODB_REGION)
        
        print("Connected to DynamoDB.")

    def create_tables(self):
        """Create DynamoDB tables if they don't exist"""
        try:
            # Create Licenses table
            licenses_table = self.resource.create_table(
                TableName=settings.DYNAMODB_TABLE,
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
            print(f"Created table: {settings.DYNAMODB_TABLE}")
        except Exception as e:
            if "Table already exists" in str(e):
                print(f"Table {settings.DYNAMODB_TABLE} already exists.")
            else:
                print(f"Error creating table: {e}")

        try:
            # Create Users table
            users_table = self.resource.create_table(
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

dynamodb = DynamoDB() 