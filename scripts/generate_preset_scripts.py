#!/usr/bin/env python3
"""프리셋 스크립트들을 자동 생성"""

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

TEMPLATE = '''#!/usr/bin/env python3
"""
Front Matter CMS용 프리셋: {name}
자동 생성된 파일입니다.
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from thumbnail_generator import create_thumbnail

PRESET_STYLE = "{style}"
PRESET_BORDER = "{border}"
PRESET_NAME = "{name}"

def get_frontmatter_data():
    fm_data = {{}}
    file_path = os.environ.get('FM_SELECTED_FILE', '')
    
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            for line in yaml_content.split('\\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    fm_data[key.strip()] = value.strip().strip('"\\\'')
    
    return fm_data, file_path

def update_frontmatter(file_path, image_path):
    if not file_path or not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'cover:' in content:
        content = re.sub(
            r'cover:\\s*\\n\\s*image:.*',
            f'cover:\\n  image: {{image_path}}',
            content
        )
    else:
        content = re.sub(
            r'\\n---',
            f'\\ncover:\\n  image: {{image_path}}\\n---',
            content,
            count=1
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print(f"🎨 {{PRESET_NAME}} 썸네일 생성 시작...", flush=True)
    
    fm_data, file_path = get_frontmatter_data()
    
    title = fm_data.get('title', '')
    description = fm_data.get('description', '')
    
    if not title:
        print("❌ 제목을 찾을 수 없습니다.", flush=True)
        print("   마크다운 파일을 선택한 후 다시 시도해주세요.", flush=True)
        sys.exit(1)
    
    subtitle = description if description else ""
    
    print(f"📝 제목: {{title}}", flush=True)
    print(f"📝 부제목: {{subtitle}}", flush=True)
    print(f"🎨 스타일: {{PRESET_NAME}}", flush=True)
    
    try:
        result = create_thumbnail(
            title=title,
            subtitle=subtitle,
            style=PRESET_STYLE,
            border=PRESET_BORDER,
            logo_path=None,
            logo_size=80
        )
        
        if isinstance(result, tuple):
            relative_path, absolute_path = result
        else:
            relative_path = result
        
        print(f"\\n✅ 썸네일 생성 완료!", flush=True)
        print(f"📁 경로: {{relative_path}}", flush=True)
        
        if file_path:
            if update_frontmatter(file_path, relative_path):
                print(f"✅ Front matter 업데이트 완료!", flush=True)
        
    except Exception as e:
        print(f"❌ 오류: {{e}}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

def generate_filename(name):
    """프리셋 이름을 파일명으로 변환"""
    return name.lower().replace(' ', '_')

def main():
    import os
    
    script_dir = os.path.dirname(__file__)
    
    for num, preset in PRESETS.items():
        filename = f"preset_{num}_{generate_filename(preset['name'])}.py"
        filepath = os.path.join(script_dir, filename)
        
        content = TEMPLATE.format(
            name=preset['name'],
            style=preset['style'],
            border=preset['border']
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        os.chmod(filepath, 0o755)
        
        print(f"✅ 생성됨: {filename}")
    
    print(f"\n🎉 총 {len(PRESETS)}개의 프리셋 스크립트가 생성되었습니다!")

if __name__ == "__main__":
    main()
