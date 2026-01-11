#!/usr/bin/env python3
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from thumbnail_generator import create_thumbnail
    
    # 간단한 테스트 썸네일 생성
    path = create_thumbnail(
        title="테스트 썸네일",
        subtitle="Front Matter 연동 테스트",
        style="default"
    )
    
    print(f"\n✅ 성공!")
    print(f"경로: {path}")
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
