---
name: voice-clone
description: 克隆声音样本并合成指定文字内容的语音
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: audio
  updated: 2026-02-21
---

# VoiceClone

克隆声音样本并合成指定文字内容的语音

## 环境变量
- `FAL_KEY`：fal.ai API Key

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --sample <样本音频> --text "要合成的文字" [--output ./cloned.mp3] [--lang zh]
```

## 示例
```bash
python run.py --sample ./voice_sample.mp3 --text "你好，这是克隆的声音"
python run.py --sample ./english_voice.wav --text "Hello world" --lang en --speed 0.9
python run.py --sample ./myvoice.mp3 --text "欢迎使用" --output ./welcome.mp3
```
