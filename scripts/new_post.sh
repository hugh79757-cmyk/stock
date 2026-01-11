#!/bin/bash
cd /Users/twinssn/Desktop/stock-blog
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
FILENAME="content/ko/posts/${DATE}-new-post-${TIME}.md"

cat > "$FILENAME" << 'TEMPLATE'
---
title: "새 글"
description: ""
date: DATE_PLACEHOLDER
draft: true
tags: []
categories: []
cover:
  image: ""
---

여기에 내용을 작성하세요.
TEMPLATE

sed -i '' "s/DATE_PLACEHOLDER/$(date -Iseconds)/" "$FILENAME"
echo "✅ 생성됨: $FILENAME"
