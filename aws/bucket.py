from .connection import Connect
#from .config import S3_BUCKET
from botocore.exceptions import ClientError
#S3버킷 이름#
S3_BUCKET="uploadedphoto"

#버킷 업로드#
def post_bucket(image_file: str, key_name: str):
    connect = Connect()
    print(key_name)
    with connect as client:
        try:
            client = connect.connect()
            client.put_object(
                Body=image_file, Bucket=S3_BUCKET, Key=key_name, ContentType="image.jpeg"
            )
        except ClientError as e:
            print("Error during image upload. {}".format(e.response["Error"]["Code"]))

#버킷 다운로드#
def pull_bucket(img_name:str):
    connect=Connect()
    with connect as client:
        try:
            client=connect.connect()
            client.get_object(
                Bucket=S3_BUCKET, Key=img_name, ResponseContentType="image.jpeg"
            )
        except ClientError as e:
             print("Error during image download. {}".format(e.response["Error"]["Code"]))
        try:
            client.download_file(S3_BUCKET,img_name,img_name)
        except ClientError as e:
            print("Error save...")