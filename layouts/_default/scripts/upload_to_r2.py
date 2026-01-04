#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from datetime import datetime
import mimetypes

import boto3
from botocore.config import Config
from dotenv import load_dotenv

# .env 로드 (프로젝트 루트에 .env 가 있다고 가정)
# VS Code에서 실행할 때도 이 경로에서 실행되도록 맞추는 게 좋습니다.
load_dotenv()

# --- R2 환경 변수 읽기 ---
ACCOUNT_ID         = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY      = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY      = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET          = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_URL      = os.getenv("R2_PUBLIC_URL")  # 예: https://img.example.com

missing = [
    name for name, value in [
        ("R2_ACCOUNT_ID", ACCOUNT_ID),
        ("R2_ACCESS_KEY_ID", R2_ACCESS_KEY),
        ("R2_SECRET_ACCESS_KEY", R2_SECRET_KEY),
        ("R2_BUCKET_NAME", R2_BUCKET),
        ("R2_PUBLIC_URL", R2_PUBLIC_URL),
    ] if not value
]

if missing:
    print("[ERROR] .env 에 다음 값들이 비어 있습니다:", ", ".join(missing), file=sys.stderr)
    sys.exit(1)

R2_ENDPOINT = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"

# --- R2(S3 호환) 클라이언트 ---
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto",                    # Cloudflare R2 는 보통 auto
    config=Config(signature_version="s3v4")
)


def upload_image(file_path: str) -> str:
    """
    이미지를 R2에 업로드하고 최종 공개 URL 을 반환합니다.
    """
    path = Path(file_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    # 날짜별 디렉터리 구조 + 원래 파일명 사용 (원하면 바꾸셔도 됩니다)
    today = datetime.now().strftime("%Y/%m/%d")
    key = f"images/{today}/{path.name}"

    # MIME 타입 추측 (브라우저에서 Content-Type 제대로 나오도록)
    content_type, _ = mimetypes.guess_type(str(path))
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    print(f"[INFO] 업로드 중: {path} → s3://{R2_BUCKET}/{key}")

    with path.open("rb") as f:
        s3.upload_fileobj(f, R2_BUCKET, key, ExtraArgs=extra_args)

    # 공개 URL (예: https://도메인/images/2026/01/04/파일.webp)
    url = f"{R2_PUBLIC_URL.rstrip('/')}/{key}"
    return url


def main():
    # 1) 명령행 인자로 파일 경로를 받았으면 그걸 사용
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    else:
        # 2) 아니면 터미널에서 직접 입력 받기
        file_path = input("업로드할 이미지 파일 경로를 입력하세요: ").strip()

    try:
        url = upload_image(file_path)
    except Exception as e:
        print(f"[ERROR] 업로드 실패: {e}", file=sys.stderr)
        sys.exit(1)

    md = f"![이미지 설명을 입력하세요]({url})"

    print("\n[OK] 업로드 완료")
    print("아래 마크다운 코드를 복사해서 본문에 붙여 넣으세요:\n")
    print(md)


if __name__ == "__main__":
    main()
