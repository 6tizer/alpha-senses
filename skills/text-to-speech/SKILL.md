---
name: text-to-speech
description: "Convert text to natural speech with multiple Chinese voices and emotion support."
version: "1.0.0"
---

# TextToSpeech

将文字转换为自然语音，支持多种中文音色和情绪

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --text "你好世界" --voice sweet_lady --output ./output.mp3
```

## 示例
```bash
python run.py --text "你好，世界！" --voice sweet_lady
python run.py --text "重要公告" --voice executive --speed 0.9 --emotion serious
python run.py --list-voices
python run.py --test-all-voices --output-dir ./voice_test
```
