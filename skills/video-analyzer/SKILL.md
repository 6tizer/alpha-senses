---
name: video-analyzer
description: "Analyze video content using Moonshot Kimi-k2.5 multimodal model and generate structured reports."
version: "1.0.0"
---

# VideoAnalyzer

使用 Moonshot Kimi-k2.5 多模态模型分析视频内容并生成结构化报告

## 环境变量
- `MOONSHOT_API_KEY`：Moonshot API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --video <视频路径或URL> [--lang zh] [--output ./analysis.md] [--mode summary]
```

## 示例
```bash
python run.py --video ./myvideo.mp4
python run.py --video "https://example.com/video.mp4" --lang en --mode detail
python run.py --video ./video.mp4 --output ./report.md
```
