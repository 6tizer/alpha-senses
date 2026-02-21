---
name: video-gen
description: 通过文字描述或参考图片生成 AI 短视频
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: video-generation
  updated: 2026-02-21
---

# VideoGen

通过文字描述或参考图片生成 AI 短视频

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --prompt "描述" [--duration 5] [--style realistic] [--model seedance]
python run.py --image <图片路径> [--duration 5] [--style cinematic]
```

## 示例
```bash
python run.py --prompt "一只猫在弹钢琴"
python run.py --prompt "太空漫步的宇航员" --style cinematic --duration 10
python run.py --image ./photo.png --duration 5 --style realistic
python run.py --prompt "日落海滩" --model kling --duration 5
```
