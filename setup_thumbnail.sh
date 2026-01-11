#!/bin/bash

echo "🎨 썸네일 생성기 설정 중..."

# 가상환경 활성화
source venv/bin/activate

# Chromium 설치 (아직 안 했다면)
echo "🌐 Chromium 설치..."
./venv/bin/python -m playwright install chromium

# 테스트
echo "🧪 썸네일 생성 테스트..."
python test_thumbnail.py

# 결과 확인
echo "📸 생성된 썸네일:"
ls -lh thumbnails/

echo "🎉 설정 완료!"
echo "💡 테스트 이미지 확인: open thumbnails/"
