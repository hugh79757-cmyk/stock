from thumbnail_generator import create_thumbnail

# 로고 없이
create_thumbnail("제목", "부제목", "default")

# 로고와 함께
create_thumbnail(
    title="원양어선 취업",
    subtitle="월급·연봉 총정리",
    style="military",
    logo_path="static/images/logo.png",
    logo_size=100
)
