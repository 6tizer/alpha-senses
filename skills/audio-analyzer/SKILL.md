---
name: audio-analyzer
description: 将音频转换为文字并分析情绪和生成内容摘要
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: audio
  updated: 2026-02-21
---

# AudioAnalyzer

将音频转换为文字并分析情绪和生成内容摘要

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --audio <音频路径或URL> [--lang auto] [--output ./transcript.md] [--emotion]
```

## 示例
```bash
python run.py --audio ./recording.mp3
python run.py --audio ./meeting.wav --lang zh --emotion
python run.py --audio "https://example.com/audio.mp3" --output ./report.md
```
