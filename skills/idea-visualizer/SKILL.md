---
name: idea-visualizer
description: 将文字想法转换为高质量图像，支持多模型对比
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: image-generation
  updated: 2026-02-21
---

# IdeaVisualizer

将文字想法转换为高质量图像，支持多模型对比

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --idea "你的想法描述" [--output ./output.png] [--model kling]
```

## 示例
```bash
python run.py --idea "太空熊猫在月球"
python run.py --idea "赛博朋克城市" --model grok
python run.py --idea "未来汽车" --compare
```
