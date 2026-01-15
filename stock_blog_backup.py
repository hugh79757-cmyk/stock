import os
from pathlib import Path

# 핵심 파일만 백업 (용량 최소화)
TARGET_FILES = {
    'hugo.toml',
    'config.toml', 
    'config.yaml',
}

# 핵심 폴더의 특정 파일만
TARGET_DIRS_EXTENSIONS = {
    'layouts': {'.html'},
    'themes': {'.html', '.css'},
    'assets': {'.css', '.scss'},
    'config': {'.toml', '.yaml', '.yml'},
}

IGNORE_DIRS = {'venv', '.git', '__pycache__', 'node_modules', 'public', 'resources', 'content', 'static', 'data', 'i18n', 'thumbnails', 'scripts'}

def create_backup():
    root_dir = Path.home() / 'Desktop' / 'stock-blog'
    output_file = root_dir / 'stock_blog_backup.txt'
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("=== STOCK-BLOG CORE STRUCTURE ===\n\n")
        
        # 1. 루트 설정 파일
        for name in TARGET_FILES:
            path = root_dir / name
            if path.exists():
                try:
                    content = path.read_text(encoding='utf-8')
                    outfile.write(f"### FILE: {name}\n")
                    outfile.write("-" * 50 + "\n")
                    outfile.write(content)
                    outfile.write("\n" + "=" * 50 + "\n\n")
                    print(f"✅ {name}")
                except Exception as e:
                    print(f"❌ {name}: {e}")
        
        # 2. 핵심 폴더별 파일
        for dir_name, extensions in TARGET_DIRS_EXTENSIONS.items():
            target_dir = root_dir / dir_name
            if not target_dir.exists():
                continue
                
            outfile.write(f"\n### === {dir_name.upper()} === ###\n\n")
            
            for path in sorted(target_dir.rglob('*')):
                if path.is_dir():
                    continue
                if any(part in IGNORE_DIRS for part in path.parts):
                    continue
                if path.suffix not in extensions:
                    continue
                    
                try:
                    content = path.read_text(encoding='utf-8')
                    relative_path = path.relative_to(root_dir)
                    outfile.write(f"### FILE: {relative_path}\n")
                    outfile.write("-" * 50 + "\n")
                    outfile.write(content)
                    outfile.write("\n" + "=" * 50 + "\n\n")
                    print(f"✅ {relative_path}")
                except Exception as e:
                    print(f"❌ {path}: {e}")

    file_size = output_file.stat().st_size / 1024
    print(f"\n🎉 완료! 용량: {file_size:.1f}KB")

if __name__ == '__main__':
    create_backup()
