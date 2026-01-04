#!/usr/bin/env python3
import os
import sys
import boto3
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

R2_ENDPOINT = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

def upload_image(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return None
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{timestamp}_{file_path.name}"
    try:
        with open(file_path, 'rb') as f:
            s3.put_object(Bucket=R2_BUCKET, Key=new_filename, Body=f, ContentType='image/webp')
        public_url = f"{R2_PUBLIC_URL}/{new_filename}"
        print(public_url)
        return public_url
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_to_r2.py <image_path>")
        sys.exit(1)
    upload_image(sys.argv[1])
