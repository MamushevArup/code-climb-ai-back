from typing import BinaryIO

import boto3

class S3Service:
    def __init__(self, acces_key, secret_key):
        self.s3 = boto3.client("s3")
        self.access_key = acces_key
        self.secret_key = secret_key

    def upload_file(self, file: BinaryIO, filename: str):
        bucket = "arupmamushev-bucket"
        filekey = f"avatar/{filename}"

        self.s3.upload_fileobj(file, bucket, filekey)

        bucket_location = boto3.client("s3").get_bucket_location(
            Bucket=bucket
        )
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )
        return object_url
    # delete file
    def delete_file(self, filename: str):
        bucket = "arupmamushev-bucket"
        filekey = f"avatar/{filename}"
        self.s3.delete_object(Bucket=bucket, Key=filekey)
        return True