#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from thumbnail_generator import create_thumbnail

# 10개 프리셋 정의
presets = [
    ("1. Professional Dark", "원양어선 취업", "월급·연봉 총정리", "military"),
    ("2. Fire Storm", "K9 자주포", "세계 1위의 비밀", "fire"),
    ("3. Tech Glow", "AI 혁명", "인공지능의 미래", "tech"),
    ("4. Minimal Clean", "블로그 시작하기", "초보자 가이드", "minimal"),
    ("5. Rainbow Pop", "여행 떠나기", "제주도 3박4일", "gradient"),
    ("6. Classic Frame", "투자 가이드", "주식 입문 완벽 정리", "default"),
    ("7. Dark Neon", "게임 공략", "최고 등급 달성 팁", "military"),
    ("8. Soft Gradient", "맛집 탐방", "서울 핫플레이스", "gradient"),
    ("9. Fire Frame", "긴급 속보", "중요 공지사항", "fire"),
    ("10. Tech Border", "스타트업", "혁신 아이디어", "tech")
]

print("=" * 60)
print("🎨 10개 프리셋 예시 썸네일 생성 중...")
print("=" * 60)

for name, title, subtitle, style in presets:
    print(f"\n생성 중: {name}")
    try:
        path = create_thumbnail(
            title=f"{name}",
            subtitle=f"{title} - {subtitle}",
            style=style
        )
        print(f"✅ {path}")
    except Exception as e:
        print(f"❌ 오류: {e}")

print("\n" + "=" * 60)
print("✅ 모든 예시 생성 완료!")
print("=" * 60)
print("\n📁 생성 위치:")
print("   static/images/thumbnails/")
print("\n🖼️  이미지 보기:")
print("   open static/images/thumbnails/")
