import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION_NAME = os.getenv("S3_BUCKET_REGION")
FILE_SERVICE_TYPE = os.getenv("FILE_SERVICE_TYPE")
