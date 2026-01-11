#!/usr/bin/env python3
import sys
import os

# 환경 변수에서 입력 받기 (Front Matter용)
title = os.environ.get('FM_TITLE', '')
subtitle = os.environ.get('FM_SUBTITLE', '')

# 환경 변수가 없으면 직접 입력
if not title:
    title = input("📝 제목: ").strip()
if not subtitle:
    subtitle = input("📝 부제목: ").strip()

if not title or not subtitle:
    print("❌ 제목과 부제목이 필요합니다.")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from thumbnail_generator import create_thumbnail

logo_path = "static/images/logo.png" if os.path.exists("static/images/logo.png") else None

path = create_thumbnail(title, subtitle, "military", "shadow", logo_path, 80)
print(f"\n✅ Professional Dark 썸네일 생성 완료!")
print(f"📁 {path}")
