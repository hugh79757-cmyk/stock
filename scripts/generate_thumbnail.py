#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from thumbnail_generator import create_thumbnail

def main():
    if len(sys.argv) < 3:
        print("❌ 사용법: python generate_thumbnail.py '제목' '부제목' [스타일] [로고경로] [로고크기]")
        sys.exit(1)
    
    title = sys.argv[1]
    subtitle = sys.argv[2]
    style = sys.argv[3] if len(sys.argv) > 3 else "default"
    logo_path = sys.argv[4] if len(sys.argv) > 4 else None
    logo_size = int(sys.argv[5]) if len(sys.argv) > 5 else 80
    
    output_dir = "static/images/thumbnails"
    path = create_thumbnail(
        title, 
        subtitle, 
        style, 
        output_dir, 
        logo_path=logo_path,
        logo_size=logo_size
    )
    
    relative_path = path.replace("static", "")
    print(f"경로: {relative_path}")

if __name__ == "__main__":
    main()
