---
name: visual-analyzer
description: 分析图像内容，生成详细描述和改进建议
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: image-analysis
  updated: 2026-02-21
---

# VisualAnalyzer

分析图像内容，生成详细描述和改进建议

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --image <图片路径或URL> [--prompt "具体问题"]
```

## 示例
```bash
python run.py --image ./photo.jpg
python run.py --image "https://example.com/image.png" --prompt "描述这张图片的色彩搭配"
```
