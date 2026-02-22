---
name: avatar-gen
description: "Convert portrait photos into animated avatar videos with customizable motion references."
version: "1.0.0"
---

# AvatarGen

将人物图片转换为动态 Avatar 视频，支持自定义动作参考

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --image <人物图片> [--motion <动作视频>] [--output ./avatar.mp4] [--duration 5]
```

## 示例
```bash
python run.py --image ./portrait.png
python run.py --image ./portrait.png --motion ./dance.mp4 --duration 10
python run.py --image "https://example.com/photo.jpg" --output ./myavatar.mp4
```
