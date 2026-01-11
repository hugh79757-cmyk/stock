from thumbnail_generator import create_thumbnail

# 1. 로고 없이 생성
print("📸 로고 없이 썸네일 생성...")
create_thumbnail(
    title="원양어선 취업",
    subtitle="월급·연봉 총정리",
    style="default"
)

# 2. 로고와 함께 생성 (로고 파일 경로 수정 필요)
logo_path = "static/images/logo.png"  # 본인의 로고 경로로 변경

if True:  # 로고 파일이 있다면
    print("\n🎨 로고와 함께 썸네일 생성...")
    
    # 다양한 스타일 테스트
    styles_to_test = ["default", "military", "fire", "tech"]
    
    for style in styles_to_test:
        create_thumbnail(
            title="원양어선 취업",
            subtitle="월급·연봉 총정리",
            style=style,
            logo_path=logo_path,
            logo_size=100
        )
        print(f"  ✅ {style} 스타일 완료")

print("\n🎉 모든 썸네일 생성 완료!")
print("💡 확인: open thumbnails/")
