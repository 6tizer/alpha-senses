#!/usr/bin/env python3
"""VisualAnalyzer — 图像分析 Skill
用法: python run.py --image <url_or_path> [--prompt "具体问题"]
"""
import argparse, os, sys
import fal_client

FAL_KEY = os.environ.get("FAL_API_KEY", "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e")

def analyze(image_url: str, prompt: str) -> str:
    os.environ["FAL_KEY"] = FAL_KEY
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
