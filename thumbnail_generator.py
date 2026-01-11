import base64
import os
import re
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

try:
    from unidecode import unidecode
except ImportError:
    print("⚠️  unidecode 패키지가 없습니다. 설치 중...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'unidecode'])
    from unidecode import unidecode

def image_to_base64(image_path):
    """이미지를 base64로 인코딩"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
    }
    mime = mime_types.get(ext, 'image/png')
    
    return f"data:{mime};base64,{encoded}"

def get_border_style(border_type):
    """테두리 스타일 CSS 반환"""
    borders = {
        "none": "",
        "shadow": "box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);",
        "neon": "box-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff, 0 0 60px #00ffff;",
        "gradient": "border: 8px solid transparent; background: linear-gradient(white, white) padding-box, linear-gradient(135deg, #667eea, #764ba2, #f093fb, #4facfe) border-box;",
        "double": "border: 4px solid white; box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.3);",
        "rounded": "border-radius: 30px; border: 6px solid white; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);"
    }
    return borders.get(border_type, "")

def sanitize_filename(text):
    """한글을 영문으로 변환하고 안전한 파일명 생성"""
    romanized = unidecode(text)
    clean = re.sub(r'[^a-zA-Z0-9\-_\s]', '', romanized)
    clean = re.sub(r'\s+', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    clean = clean.strip('_').lower()
    
    if not clean:
        clean = 'untitled'
    
    return clean[:30]

def get_thumbnail_html(title, subtitle, style="default", border="shadow", logo_path=None, logo_size=80):
    """썸네일 HTML 생성 (새로운 프레임 디자인)"""
    
    # 로고 처리
    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        logo_data = image_to_base64(logo_path)
        logo_html = f"""
        <div class="logo">
            <img src="{logo_data}" alt="Logo" style="width: {logo_size}px; height: {logo_size}px; object-fit: contain;">
        </div>
        """
    
    # 스타일별 설정
    styles = {
        "default": {
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "title_color": "#ffffff",
            "subtitle_color": "#f0f0f0",
            "frame_color": "#667eea"
        },
        "military": {
            "background": "linear-gradient(135deg, #2d3436 0%, #636e72 100%)",
            "title_color": "#dfe6e9",
            "subtitle_color": "#b2bec3",
            "frame_color": "#636e72"
        },
        "fire": {
            "background": "linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)",
            "title_color": "#ffffff",
            "subtitle_color": "#ffe8d0",
            "frame_color": "#ff6a00"
        },
        "tech": {
            "background": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
            "title_color": "#00d4ff",
            "subtitle_color": "#a8dadc",
            "frame_color": "#00d4ff"
        },
        "minimal": {
            "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
            "title_color": "#2d3436",
            "subtitle_color": "#636e72",
            "frame_color": "#636e72"
        },
        "gradient": {
            "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
            "title_color": "#2d3436",
            "subtitle_color": "#636e72",
            "frame_color": "#fed6e3"
        }
    }
    
    current_style = styles.get(style, styles["default"])
    border_css = get_border_style(border)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Noto Sans KR', sans-serif;
                background: {current_style['background']};
                width: 1280px;
                height: 720px;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }}
            /* 외곽 프레임 */
            .frame {{
                position: absolute;
                border: 4px solid {current_style['frame_color']};
                pointer-events: none;
            }}
            .frame.top-left {{
                top: 40px;
                left: 40px;
                width: 100px;
                height: 100px;
                border-right: none;
                border-bottom: none;
            }}
            .frame.top-right {{
                top: 40px;
                right: 40px;
                width: 100px;
                height: 100px;
                border-left: none;
                border-bottom: none;
            }}
            .frame.bottom-left {{
                bottom: 40px;
                left: 40px;
                width: 100px;
                height: 100px;
                border-right: none;
                border-top: none;
            }}
            .frame.bottom-right {{
                bottom: 40px;
                right: 40px;
                width: 100px;
                height: 100px;
                border-left: none;
                border-top: none;
            }}
            .logo {{
                position: absolute;
                top: 30px;
                left: 30px;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                z-index: 10;
            }}
            .content {{
                text-align: center;
                padding: 60px;
                max-width: 900px;
                z-index: 5;
            }}
            h1 {{
                font-size: 88px;
                font-weight: 900;
                color: {current_style['title_color']};
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
                line-height: 1.2;
                position: relative;
                display: inline-block;
            }}
            /* 제목 밑줄 */
            h1::after {{
                content: '';
                position: absolute;
                bottom: -15px;
                left: 50%;
                transform: translateX(-50%);
                width: 60%;
                height: 4px;
                background: {current_style['frame_color']};
            }}
            h2 {{
                font-size: 48px;
                font-weight: 400;
                color: {current_style['subtitle_color']};
                text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        <!-- 외곽 프레임 -->
        <div class="frame top-left"></div>
        <div class="frame top-right"></div>
        <div class="frame bottom-left"></div>
        <div class="frame bottom-right"></div>
        
        {logo_html}
        
        <div class="content">
            <h1>{title}</h1>
            <h2>{subtitle}</h2>
        </div>
    </body>
    </html>
    """
    return html

def generate_image(html, filename, width=1280, height=720):
    """HTML을 이미지로 변환"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.set_content(html)
        page.screenshot(path=filename)
        browser.close()

def create_thumbnail(title, subtitle, style="default", border="shadow", logo_path=None, logo_size=80, output_dir="static/images/thumbnails"):
    """썸네일 생성 메인 함수"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = sanitize_filename(title)
    filename = f"thumbnail_{safe_title}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    html = get_thumbnail_html(title, subtitle, style, border, logo_path, logo_size)
    generate_image(html, filepath)
    
    relative_path = filepath.replace("static/", "/")
    print(f"✅ 썸네일 생성 완료: {relative_path}")
    print(f"📝 파일명: {filename}")
    
    absolute_path = os.path.abspath(filepath)
    return (relative_path, absolute_path)

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 새로운 프레임 디자인 테스트")
    print("=" * 60)
    
    test_cases = [
        ("K2", "K2 흑표 전차", "fire"),
        ("원양어선 취업", "월급·연봉 총정리", "tech"),
        ("Stock Market", "2024 Analysis", "minimal")
    ]
    
    for title, subtitle, style in test_cases:
        relative, absolute = create_thumbnail(title, subtitle, style)
        print(f"\n제목: {title}")
        print(f"파일: {os.path.basename(absolute)}")
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료! 파일을 확인하세요:")
    print("   open static/images/thumbnails/")
    print("=" * 60)
