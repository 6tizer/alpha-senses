---
name: tweet-image-gen
description: "Automatically generate social media images based on tweet content and style."
version: "1.0.0"
---

# TweetImageGen

根据推文内容和风格自动生成社交媒体配图

## 环境变量
- `FAL_KEY`：fal.ai API Key
- `MOONSHOT_API_KEY`：Moonshot API Key（用于优化 prompt）

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python run.py --tweet "推文内容" [--style crypto] [--output ./output.png]
```

## 示例
```bash
python run.py --tweet "比特币突破10万美元！🚀" --style crypto
python run.py --tweet "产品发布" --style minimal --output ./product.png
python run.py --mode thread --tweet-file ./article.txt --style news
```
