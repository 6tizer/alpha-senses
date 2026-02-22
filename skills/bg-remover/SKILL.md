---
name: bg-remover
description: "Intelligently remove image backgrounds while preserving the main subject."
version: "1.0.0"
---

# BackgroundRemover

智能去除图片背景，保留主体内容

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --image <图片路径或URL> [--output ./no-bg.png]
```

## 示例
```bash
python run.py --image ./photo.jpg
python run.py --image "https://example.com/image.png" --output ./clean.png
```
