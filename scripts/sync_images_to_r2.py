#!/usr/bin/env python3
import os
import re
import boto3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

R2_ENDPOINT = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.getenv('R2_BUCKET_NAME')
R2_PUBLIC_URL = os.getenv('R2_PUBLIC_URL')

s3 = boto3.client('s3', endpoint_url=R2_ENDPOINT, aws_access_key_id=R2_ACCESS_KEY, aws_secret_access_key=R2_SECRET_KEY)

def upload_to_r2(local_path):
    file_name = Path(local_path).name
    try:
        with open(local_path, 'rb') as f:
            s3.put_object(Bucket=R2_BUCKET, Key=file_name, Body=f, ContentType='image/webp')
        return f"{R2_PUBLIC_URL}/{file_name}"
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

def process_markdown_files(content_dir):
    content_path = Path(content_dir)
    static_path = Path("static")
    processed = 0
    
    for md_file in content_path.rglob("*.md"):
        print(f"\nProcessing: {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = r'!\[([^\]]*)\]\(([^)]+\.(webp|jpg|jpeg|png|gif))\)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        if not matches:
            continue
        
        modified = False
        new_content = content
        
        for alt_text, image_path, ext in matches:
            if image_path.startswith('http'):
                continue
            
            image_name = Path(image_path).name
            local_image = static_path / image_name
            
            if not local_image.exists():
                print(f"  Image not found: {image_name}")
                continue
            
            print(f"  Uploading: {image_name}")
            r2_url = upload_to_r2(local_image)
            
            if r2_url:
                old = f'![{alt_text}]({image_path})'
                new = f'![{alt_text}]({r2_url})'
                new_content = new_content.replace(old, new)
                modified = True
                print(f"  Done: {r2_url}")
        
        if modified:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            processed += 1
    
    print(f"\n\nComplete! Processed {processed} files")

if __name__ == "__main__":
    process_markdown_files("content")
