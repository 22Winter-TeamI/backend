import boto3

#사용자 접근 키#
AWS_ACCESS_KEY_ID="AKIAUJGODXEMWZOTIF4E"
AWS_SECRET_ACCESS_KEY="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"

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