from typing import List, Optional
import boto3
from boto3.dynamodb.conditions import Key
import uuid
from datetime import datetime
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate
from app.core.config import settings

class LicenseCRUD:
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
        
        self.table = self.dynamodb.Table(settings.DYNAMODB_TABLE)

    async def create(self, license_in: LicenseCreate) -> dict:
        license_id = str(uuid.uuid4())
        license_data = license_in.model_dump()
        license_data["license_id"] = license_id
        license_data["create_at"] = datetime.utcnow().isoformat()
        license_data["update_at"] = datetime.utcnow().isoformat()
        
        self.table.put_item(Item=license_data)
        return license_data

    async def get(self, license_id: str) -> Optional[dict]:
        response = self.table.get_item(Key={"license_id": license_id})
        return response.get("Item")

    async def get_multi(self, skip: int = 0, limit: int = 10) -> List[dict]:
        response = self.table.scan(Limit=limit)
        items = response.get("Items", [])
        return items[skip:skip+limit]

    async def update(self, license_id: str, license_in: LicenseUpdate) -> Optional[dict]:
        update_data = license_in.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.utcnow().isoformat()
        
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for key, value in update_data.items():
            if key != "license_id":
                update_expression += f"#{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
                expression_attribute_names[f"#{key}"] = key
        
        update_expression = update_expression.rstrip(", ")
        
        try:
            response = self.table.update_item(
                Key={"license_id": license_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
                ReturnValues="ALL_NEW"
            )
            return response.get("Attributes")
        except Exception as e:
            print(f"Error updating license: {e}")
            return None

    async def delete(self, license_id: str) -> bool:
        try:
            self.table.delete_item(Key={"license_id": license_id})
            return True
        except Exception as e:
            print(f"Error deleting license: {e}")
            return False

license_crud = LicenseCRUD() 