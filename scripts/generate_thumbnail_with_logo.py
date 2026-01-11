#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from thumbnail_generator import create_thumbnail

def get_input(prompt):
    """사용자 입력 받기"""
    print(prompt, end='', flush=True)
    return input().strip()

if __name__ == "__main__":
    try:
        # 사용자 입력 받기
        title = get_input("제목을 입력하세요: ")
        if not title:
            print("❌ 제목이 필요합니다.")
            sys.exit(1)
        
        subtitle = get_input("부제목을 입력하세요: ")
        if not subtitle:
            print("❌ 부제목이 필요합니다.")
            sys.exit(1)
        
        print("\n사용 가능한 스타일:")
        print("1. default (보라색 그라데이션)")
        print("2. military (군사 다크)")
        print("3. fire (불꽃 레드/오렌지)")
        print("4. tech (테크 블루)")
        print("5. minimal (미니멀 그레이)")
        print("6. gradient (파스텔 그라데이션)")
        
        style_input = get_input("\n스타일 번호 또는 이름 (기본: default): ")
        
        # 스타일 매핑
        style_map = {
            "1": "default",
            "2": "military",
            "3": "fire",
            "4": "tech",
            "5": "minimal",
            "6": "gradient"
        }
        
        style = style_map.get(style_input, style_input if style_input else "default")
        
        # 로고 경로 입력
        logo_path = get_input("\n로고 파일 경로 (기본: static/images/logo.png): ")
        if not logo_path:
            logo_path = "static/images/logo.png"
        
        if not os.path.exists(logo_path):
            print(f"⚠️  경고: 로고 파일을 찾을 수 없습니다: {logo_path}")
            use_logo = get_input("로고 없이 계속하시겠습니까? (y/n): ")
            if use_logo.lower() != 'y':
                print("❌ 취소되었습니다.")
                sys.exit(1)
            logo_path = None
        
        # 로고 크기 입력
        logo_size = 80
        if logo_path:
            logo_size_input = get_input("\n로고 크기 (픽셀, 기본: 80): ")
            if logo_size_input:
                try:
                    logo_size = int(logo_size_input)
                except ValueError:
                    print("⚠️  잘못된 크기입니다. 기본값 80을 사용합니다.")
        
        # 썸네일 생성
        print(f"\n🎨 썸네일 생성 중...")
        print(f"   제목: {title}")
        print(f"   스타일: {style}")
        if logo_path:
            print(f"   로고: {logo_path} ({logo_size}px)")
        
        path = create_thumbnail(title, subtitle, style, logo_path, logo_size)
        
        print(f"\n✅ 썸네일이 생성되었습니다!")
        print(f"📁 경로: {path}")
        print(f"\n📋 Front Matter에 추가할 내용:")
        print(f"cover:")
        print(f"  image: {path}")
        
    except KeyboardInterrupt:
        print("\n\n❌ 취소되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)
