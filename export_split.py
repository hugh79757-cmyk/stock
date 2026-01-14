import os
from datetime import datetime

# 설정
BASE_DIR = "/Users/twinssn/Desktop/stock-blog"
OUTPUT_DIR = "/Users/twinssn/Desktop"
SPLIT_COUNT = 4  # 분할 개수 (3 또는 4로 변경 가능)

# 제외할 폴더/파일
EXCLUDE_DIRS = {
    '.git',
    'node_modules',
    'public',
    'resources',
    '.hugo_build.lock',
    '__pycache__',
    '.DS_Store',
    'themes'
}

# 포함할 확장자
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

def collect_all_files():
    """모든 파일 경로와 내용 수집"""
    files_data = []
    
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
            content = get_file_content(filepath)
            
            files_data.append({
                'path': relative_path,
                'content': content
            })
    
    return files_data

def generate_folder_structure():
    """폴더 구조 문자열 생성"""
    lines = []
    lines.append("## 폴더 구조")
    lines.append("-" * 40)
    
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if should_include(root, d)]
        
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root) or 'stock-blog'
        lines.append(f"{indent}📁 {folder_name}/")
        
        subindent = '  ' * (level + 1)
        for file in sorted(files):
            if should_include(root, file):
                ext = os.path.splitext(file)[1].lower()
                if not INCLUDE_EXTENSIONS or ext in INCLUDE_EXTENSIONS:
                    lines.append(f"{subindent}📄 {file}")
    
    return '\n'.join(lines)

def split_list(lst, n):
    """리스트를 n개로 균등 분할"""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def export_files():
    """파일을 분할하여 저장"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # 모든 파일 수집
    all_files = collect_all_files()
    total_count = len(all_files)
    
    # 폴더 구조
    folder_structure = generate_folder_structure()
    
    # 파일 분할
    split_files = split_list(all_files, SPLIT_COUNT)
    
    print(f"📊 총 파일 수: {total_count}개")
    print(f"📦 {SPLIT_COUNT}개 파일로 분할합니다.\n")
    
    for i, file_group in enumerate(split_files, 1):
        output_lines = []
        
        # 헤더
        output_lines.append("=" * 80)
        output_lines.append(f"Stock Blog 파일 추출 (Part {i}/{SPLIT_COUNT})")
        output_lines.append(f"추출 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append(f"기준 경로: {BASE_DIR}")
        output_lines.append(f"이 파일의 파일 수: {len(file_group)}개 / 전체 {total_count}개")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        # 첫 번째 파일에만 폴더 구조 포함
        if i == 1:
            output_lines.append(folder_structure)
            output_lines.append("")
            output_lines.append("")
        
        # 파일 내용
        output_lines.append(f"## 파일 내용 (Part {i}/{SPLIT_COUNT})")
        output_lines.append("=" * 80)
        
        for file_data in file_group:
            output_lines.append("")
            output_lines.append(f"### 파일: {file_data['path']}")
            output_lines.append("-" * 60)
            output_lines.append("")
            output_lines.append(file_data['content'])
            output_lines.append("")
            output_lines.append("-" * 60)
        
        output_lines.append("")
        output_lines.append(f"[Part {i}/{SPLIT_COUNT} 끝] - {len(file_group)}개 파일")
        
        # 파일 저장
        output_file = f"{OUTPUT_DIR}/stock-blog-export-{timestamp}-part{i}of{SPLIT_COUNT}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        print(f"✅ Part {i}/{SPLIT_COUNT} 저장 완료: {len(file_group)}개 파일")
        print(f"   📄 {output_file}")
    
    print(f"\n🎉 모든 분할 완료!")

if __name__ == "__main__":
    export_files()
