import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from app.core.config import settings
import uuid

class S3Service:
    def __init__(self):
        aws_region = getattr(settings, 'AWS_REGION', 'us-east-1')
        aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        self.bucket_name = getattr(settings, 'AWS_S3_BUCKET', None)
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET no está configurado en settings")
        self.s3_client = boto3.client(
            's3',
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def upload_image(self, file_obj, filename: str = None, content_type: str = None) -> str:
        """
        Sube una imagen a S3 y retorna la URL pública.
        :param file_obj: archivo tipo file-like (por ejemplo, UploadFile.file)
        :param filename: nombre opcional, si no se provee se genera uno único
        :param content_type: tipo de contenido opcional
        :return: URL pública de la imagen subida
        """
        if not filename:
            filename = f"images/{uuid.uuid4()}.jpg"
        try:
            extra_args = {'ACL': 'public-read'}
            if content_type:
                extra_args['ContentType'] = content_type
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs=extra_args
            )
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
            return url
        except (NoCredentialsError, ClientError) as e:
            raise Exception(f"Error al subir la imagen a S3: {e}")

s3_service = S3Service() 