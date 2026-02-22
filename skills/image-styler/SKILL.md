---
name: image-styler
description: "Transform images into artistic styles like cyberpunk, anime, or cinematic looks."
version: "1.0.0"
---

# ImageStyler

将图片转换成赛博朋克、动漫、电影感等指定艺术风格

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --image <图片路径或URL> --style <风格> [--output ./styled.png]
```

## 示例
```bash
python run.py --image ./photo.jpg --style cyberpunk
python run.py --image ./me.png --style anime --strength 0.8
python run.py --image https://example.com/pic.png --style cinematic --compare
```
