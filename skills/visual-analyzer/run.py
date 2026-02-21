#!/usr/bin/env python3
"""VisualAnalyzer — 图像分析 Skill
用法: python run.py --image <url_or_path> [--prompt "具体问题"]
"""
import argparse, os, sys
import fal_client

FAL_KEY = os.environ.get("FAL_API_KEY", "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e")

def upload_if_needed(path: str) -> str:
    """如果是本地文件则上传，返回 URL"""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    print(f"📤 正在上传本地图片...")
    url = fal_client.upload_file(path)
    print(f"✅ 上传完成: {url}")
    return url

def analyze(image_path: str, prompt: str) -> str:
    os.environ["FAL_KEY"] = FAL_KEY
    image_url = upload_if_needed(image_path)
    result = fal_client.run(
        "fal-ai/florence-2-large/detailed-caption",
        arguments={"image_url": image_url},
    )
    if isinstance(result, dict):
        r = result.get("results", "")
        if isinstance(r, str):
            caption = r
        elif isinstance(r, dict):
            caption = r.get("detailed_caption", str(r))
        else:
            caption = result.get("output", str(result))
    else:
        caption = str(result)
    return caption

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="图片 URL 或本地路径")
    parser.add_argument("--prompt", default="请详细描述这张图片的内容、风格和氛围，并给出改进或使用建议。")
    args = parser.parse_args()
    print(analyze(args.image, args.prompt))
