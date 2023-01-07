import boto3
from .aws_key import ACCESS_KEY_ID,SECRET_ACCESS_KEY
#사용자 접근 키#
AWS_ACCESS_KEY_ID=ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=SECRET_ACCESS_KEY

class Connect:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def __enter__(self):
        return self 

    def connect(self):
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...