from typing import List, Optional
import boto3
from boto3.dynamodb.conditions import Key
import uuid
from datetime import datetime
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import settings
from app.core.security import get_password_hash, verify_password

class UserCRUD:
    def __init__(self):
        if settings.ENV == "development" and settings.DYNAMODB_ENDPOINT_URL:
            # Use local DynamoDB for development
            self.dynamodb = boto3.resource(
                'dynamodb', 
                region_name=settings.DYNAMODB_REGION,
                endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            # Use AWS DynamoDB for production
            self.dynamodb = boto3.resource('dynamodb', region_name=settings.DYNAMODB_REGION)
        
        self.table = self.dynamodb.Table("Users")

    async def create(self, user_in: UserCreate) -> dict:
        user_id = str(uuid.uuid4())
        user_data = user_in.model_dump(exclude={"password"})
        user_data["user_id"] = user_id
        user_data["hashed_password"] = get_password_hash(user_in.password)
        user_data["create_at"] = datetime.utcnow().isoformat()
        user_data["update_at"] = datetime.utcnow().isoformat()
        
        self.table.put_item(Item=user_data)
        return user_data

    async def get(self, user_id: str) -> Optional[dict]:
        response = self.table.get_item(Key={"user_id": user_id})
        return response.get("Item")

    async def get_by_email(self, email: str) -> Optional[dict]:
        response = self.table.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response.get("Items", [])
        return items[0] if items else None

    async def get_by_username(self, username: str) -> Optional[dict]:
        response = self.table.query(
            IndexName="username-index",
            KeyConditionExpression=Key("username").eq(username)
        )
        items = response.get("Items", [])
        return items[0] if items else None

    async def get_multi(self, skip: int = 0, limit: int = 10) -> List[dict]:
        response = self.table.scan(Limit=limit)
        items = response.get("Items", [])
        return items[skip:skip+limit]

    async def update(self, user_id: str, user_in: UserUpdate) -> Optional[dict]:
        update_data = user_in.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.utcnow().isoformat()
        
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for key, value in update_data.items():
            if key != "user_id":
                update_expression += f"#{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
                expression_attribute_names[f"#{key}"] = key
        
        update_expression = update_expression.rstrip(", ")
        
        try:
            response = self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
                ReturnValues="ALL_NEW"
            )
            return response.get("Attributes")
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    async def delete(self, user_id: str) -> bool:
        try:
            self.table.delete_item(Key={"user_id": user_id})
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    async def authenticate(self, username: str, password: str) -> Optional[dict]:
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    async def authenticate_by_email(self, email: str, password: str) -> Optional[dict]:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

user_crud = UserCRUD() 