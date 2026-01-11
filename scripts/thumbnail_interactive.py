#!/usr/bin/env python3
import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 강제로 표준 출력 플러시
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from thumbnail_generator import create_thumbnail

def print_flush(text):
    """출력 후 즉시 플러시"""
    print(text, flush=True)

def input_flush(prompt):
    """입력 받기 전 플러시"""
    print(prompt, end='', flush=True)
    return input().strip()

# 프리셋 정의
PRESETS = {
    "1": {"name": "Professional Dark", "style": "military", "border": "shadow"},
    "2": {"name": "Fire Storm", "style": "fire", "border": "neon"},
    "3": {"name": "Tech Glow", "style": "tech", "border": "neon"},
    "4": {"name": "Minimal Clean", "style": "minimal", "border": "rounded"},
    "5": {"name": "Rainbow Pop", "style": "gradient", "border": "gradient"},
    "6": {"name": "Classic Frame", "style": "default", "border": "double"},
    "7": {"name": "Dark Neon", "style": "military", "border": "gradient"},
    "8": {"name": "Soft Gradient", "style": "gradient", "border": "shadow"},
    "9": {"name": "Fire Frame", "style": "fire", "border": "double"},
    "10": {"name": "Tech Border", "style": "tech", "border": "rounded"}
}

try:
    print_flush("=" * 60)
    print_flush("🎨 썸네일 생성기")
    print_flush("=" * 60)
    
    # 1. 제목 입력
    title = input_flush("\n📝 제목: ")
    if not title:
        print_flush("❌ 제목이 필요합니다.")
        sys.exit(1)
    
    # 2. 부제목 입력
    subtitle = input_flush("📝 부제목: ")
    if not subtitle:
        print_flush("❌ 부제목이 필요합니다.")
        sys.exit(1)
    
    # 3. 프리셋 선택
    print_flush("\n🎨 스타일 프리셋:")
    for key, preset in PRESETS.items():
        print_flush(f"  {key}. {preset['name']}")
    
    preset_choice = input_flush("\n프리셋 번호 (1-10): ").strip() or "1"
    preset = PRESETS.get(preset_choice, PRESETS["1"])
    
    # 4. 로고 선택
    logo_path = None
    logo_files = glob.glob("static/images/logos/*.png") + glob.glob("static/images/logos/*.jpg")
    
    if logo_files:
        print_flush("\n🖼️  사용 가능한 로고:")
        print_flush("  0. 로고 없음")
        for i, logo in enumerate(logo_files, 1):
            logo_name = os.path.basename(logo)
            print_flush(f"  {i}. {logo_name}")
        
        logo_choice = input_flush(f"\n로고 선택 (0-{len(logo_files)}): ").strip() or "0"
        
        try:
            logo_idx = int(logo_choice)
            if logo_idx > 0 and logo_idx <= len(logo_files):
                logo_path = logo_files[logo_idx - 1]
                print_flush(f"✅ 선택된 로고: {os.path.basename(logo_path)}")
        except ValueError:
            print_flush("⚠️  잘못된 입력입니다. 로고 없이 진행합니다.")
    else:
        print_flush("\n⚠️  로고 파일이 없습니다. (static/images/logos/ 폴더에 추가하세요)")
    
    # 5. 로고 크기 (로고가 있을 때만)
    logo_size = 80
    if logo_path:
        size_input = input_flush("📏 로고 크기 (픽셀, 기본 80): ").strip()
        if size_input:
            try:
                logo_size = int(size_input)
            except ValueError:
                print_flush("⚠️  잘못된 크기입니다. 기본값 80을 사용합니다.")
    
    # 6. 썸네일 생성
    print_flush("\n" + "=" * 60)
    print_flush("🎨 썸네일 생성 중...")
    print_flush("=" * 60)
    print_flush(f"📝 제목: {title}")
    print_flush(f"📝 부제목: {subtitle}")
    print_flush(f"🎨 프리셋: {preset['name']}")
    if logo_path:
        print_flush(f"🖼️  로고: {os.path.basename(logo_path)} ({logo_size}px)")
    else:
        print_flush(f"🖼️  로고: 없음")
    print_flush("=" * 60)
    
    path = create_thumbnail(
        title=title,
        subtitle=subtitle,
        style=preset['style'],
        border=preset['border'],
        logo_path=logo_path,
        logo_size=logo_size
    )
    
    print_flush("\n✅ 썸네일 생성 완료!")
    print_flush(f"📁 경로: {path}")
    print_flush("\n📋 Front Matter에 추가할 내용:")
    print_flush("cover:")
    print_flush(f"  image: {path}")
    
except KeyboardInterrupt:
    print_flush("\n\n❌ 취소되었습니다.")
    sys.exit(1)
except Exception as e:
    print_flush(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
