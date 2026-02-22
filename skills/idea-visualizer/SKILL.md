---
name: idea-visualizer
description: "Transform text ideas into high-quality images with multi-model comparison support."
version: "1.0.0"
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
