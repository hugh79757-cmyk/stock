import os
from datetime import datetime

# 설정
BASE_DIR = "/Users/twinssn/Desktop/stock-blog"
OUTPUT_FILE = f"/Users/twinssn/Desktop/stock-blog-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"

# 제외할 폴더/파일
EXCLUDE_DIRS = {
    '.git',
    'node_modules',
    'public',
    'resources',
    '.hugo_build.lock',
    '__pycache__',
    '.DS_Store',
    'themes'  # 테마는 제외 (필요시 주석 해제)
}

# 포함할 확장자 (빈 set이면 모든 파일 포함)
INCLUDE_EXTENSIONS = {
    '.toml', '.yaml', '.yml', '.md', '.html', '.css', '.js', '.json'
}

def should_include(path, name):
    """파일/폴더 포함 여부 확인"""
    if name in EXCLUDE_DIRS:
        return False
    if name.startswith('.'):
        return False
    return True

def get_file_content(filepath):
    """파일 내용 읽기"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return "[바이너리 파일 - 내용 생략]"
    except Exception as e:
        return f"[읽기 오류: {e}]"

def export_files():
    """모든 파일 구조와 내용 추출"""
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append(f"Stock Blog 파일 구조 및 내용 추출")
    output_lines.append(f"추출 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"기준 경로: {BASE_DIR}")
    output_lines.append("=" * 80)
    output_lines.append("")
    
    # 1. 폴더 구조 먼저 출력
    output_lines.append("## 폴더 구조")
    output_lines.append("-" * 40)
    
    for root, dirs, files in os.walk(BASE_DIR):
        # 제외 폴더 필터링
        dirs[:] = [d for d in dirs if should_include(root, d)]
        
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root) or 'stock-blog'
        output_lines.append(f"{indent}📁 {folder_name}/")
        
        subindent = '  ' * (level + 1)
        for file in sorted(files):
            if should_include(root, file):
                ext = os.path.splitext(file)[1].lower()
                if not INCLUDE_EXTENSIONS or ext in INCLUDE_EXTENSIONS:
                    output_lines.append(f"{subindent}📄 {file}")
    
    output_lines.append("")
    output_lines.append("")
    
    # 2. 각 파일 내용 출력
    output_lines.append("## 파일 내용")
    output_lines.append("=" * 80)
    
    file_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if should_include(root, d)]
        
        for file in sorted(files):
            if not should_include(root, file):
                continue
                
            ext = os.path.splitext(file)[1].lower()
            if INCLUDE_EXTENSIONS and ext not in INCLUDE_EXTENSIONS:
                continue
            
            filepath = os.path.join(root, file)
            relative_path = filepath.replace(BASE_DIR, '').lstrip(os.sep)
            
            output_lines.append("")
            output_lines.append(f"### 파일: {relative_path}")
            output_lines.append("-" * 60)
            output_lines.append("")
            
            content = get_file_content(filepath)
            output_lines.append(content)
            
            output_lines.append("")
            output_lines.append("-" * 60)
            
            file_count += 1
    
    output_lines.append("")
    output_lines.append(f"총 {file_count}개 파일 추출 완료")
    
    # 파일 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"✅ 추출 완료!")
    print(f"📄 저장 위치: {OUTPUT_FILE}")
    print(f"📊 총 파일 수: {file_count}개")

if __name__ == "__main__":
    export_files()
