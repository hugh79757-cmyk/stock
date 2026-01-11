#!/usr/bin/env python3
"""Front Matter CMS 환경변수 테스트"""
import os
import sys

print("=" * 50, flush=True)
print("🔍 Front Matter CMS 환경변수 확인", flush=True)
print("=" * 50, flush=True)

# 모든 환경변수 중 FM 관련 출력
for key, value in sorted(os.environ.items()):
    if 'FM' in key.upper() or 'FRONT' in key.upper():
        print(f"{key}: {value}", flush=True)

print("\n📁 현재 작업 디렉토리:", os.getcwd(), flush=True)
print("📄 sys.argv:", sys.argv, flush=True)

# stdin 확인
print("\n📥 stdin 데이터 확인 중...", flush=True)
if not sys.stdin.isatty():
    stdin_data = sys.stdin.read()
    if stdin_data:
        print(f"stdin: {stdin_data[:500]}", flush=True)
    else:
        print("stdin: (비어있음)", flush=True)
else:
    print("stdin: (tty 모드)", flush=True)

print("\n✅ 테스트 완료!", flush=True)
