#!/usr/bin/env python3
"""BackgroundRemover — 去背景 Skill
用法: python run.py --image <url_or_path> [--output ./output.png]
"""
import argparse, os, urllib.request
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

def remove_bg(image_path: str, output_path: str = "./no-bg.png") -> dict:
    os.environ["FAL_KEY"] = FAL_KEY
    image_url = upload_if_needed(image_path)
    result = fal_client.run(
        "fal-ai/bria/background/remove",
        arguments={"image_url": image_url},
    )
    # 兼容不同返回格式
    img = result.get("image") or result.get("images")
    if isinstance(img, dict):
        url = img.get("url", "")
    elif isinstance(img, list) and img:
        url = img[0].get("url", "")
    else:
        return {"error": "unexpected response", "raw": str(result)}
    if url:
        urllib.request.urlretrieve(url, output_path)
        return {"url": url, "local": output_path}
    return {"error": "no output url", "raw": str(result)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="图片 URL 或本地路径")
    parser.add_argument("--output", default="./no-bg.png")
    args = parser.parse_args()
    result = remove_bg(args.image, args.output)
    if "url" in result:
        print(f"✅ 去背景成功")
        print(f"URL:   {result['url']}")
        print(f"本地:  {result['local']}")
    else:
        print(f"❌ 失败: {result}")
