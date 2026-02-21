#!/usr/bin/env python3
"""
ImageStyler — 图片风格转换器
将图片转换成指定艺术风格

用法:
    python run.py --image <path_or_url> --style cyberpunk --output ./styled.png
    python run.py --image ./photo.jpg --style anime --strength 0.8

风格选项:
    cyberpunk  - 赛博朋克，霓虹+暗调
    minimal    - 极简，清爽白底
    anime      - 动漫插画风
    cinematic  - 电影感，高对比度
"""
import argparse
import os
import sys
import time
import urllib.request
from typing import Optional

import fal_client

# FAL API Key
FAL_KEY = os.environ.get(
    "FAL_API_KEY",
    "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
)

# 风格预设 - 针对不同风格优化的prompt模板
STYLE_PROMPTS = {
    "cyberpunk": (
        "Transform into cyberpunk style: neon lights, dark atmosphere, "
        "futuristic city vibes, electric blue and purple glow, rain reflections, "
        "high contrast, sci-fi aesthetic, blade runner inspired"
    ),
    "minimal": (
        "Transform into minimalist style: clean white background, simple composition, "
        "reduced elements, elegant simplicity, Scandinavian design, "
        "soft shadows, modern aesthetic, plenty of negative space"
    ),
    "anime": (
        "Transform into anime illustration style: vibrant colors, clean lines, "
        "studio ghibli inspired, cel shading, detailed background, "
        "manga aesthetic, expressive, high quality digital art"
    ),
    "cinematic": (
        "Transform into cinematic style: dramatic lighting, film grain, "
        "anamorphic lens effect, high contrast, moody atmosphere, "
        "color grading like a movie, professional photography, 4K quality"
    ),
}

# 模型端点
MODELS = {
    "kling": "fal-ai/kling-image/v3/image-to-image",
    "glm": "fal-ai/glm-image/image-to-image",
    "grok": "xai/grok-imagine-image/edit",
}


def is_url(path: str) -> bool:
    """检查是否为URL"""
    return path.startswith(("http://", "https://"))


def style_image_with_model(
    model_id: str,
    image_path: str,
    prompt: str,
    strength: float = 0.7,
) -> dict:
    """
    使用指定模型进行风格转换
    
    Args:
        model_id: 模型端点ID
        image_path: 本地图片路径或URL
        prompt: 风格转换提示词
        strength: 风格强度 (0.1-1.0)
        
    Returns:
        dict: 包含 images 的响应数据
    """
    os.environ["FAL_KEY"] = FAL_KEY
    
    # 如果是本地路径，需要上传到fal（这里简化处理，假设可以直接使用）
    # 实际上fal支持URL，本地文件需要先上传
    
    arguments = {
        "prompt": prompt,
    }
    
    # 处理图片输入
    if is_url(image_path):
        # 直接使用URL
        arguments["image_url"] = image_path
    else:
        # 本地文件需要上传 - 使用 fal_client 的文件上传功能
        try:
            image_url = fal_client.upload_file(image_path)
            arguments["image_url"] = image_url
        except Exception as e:
            # 如果上传失败，尝试直接读取为data URI
            import base64
            import mimetypes
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = "image/png"
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
                arguments["image_url"] = f"data:{mime_type};base64,{image_data}"
    
    # 不同模型的参数略有差异
    if "kling" in model_id:
        arguments["strength"] = strength
        arguments["num_inference_steps"] = 30
    elif "glm" in model_id:
        arguments["strength"] = strength
    
    result = fal_client.run(model_id, arguments=arguments)
    return result


def style_image(
    image: str,
    style: str = "cyberpunk",
    strength: float = 0.7,
    output_path: str = "./output.png",
    compare: bool = False,
) -> dict:
    """
    转换图片风格
    
    Args:
        image: 图片路径或URL
        style: 目标风格 (cyberpunk/minimal/anime/cinematic)
        strength: 风格强度 0.1-1.0
        output_path: 输出文件路径
        compare: 是否对比多个模型
        
    Returns:
        dict: 转换结果
    """
    # 验证风格参数
    if style not in STYLE_PROMPTS:
        raise ValueError(f"不支持的风格: {style}。可选: {list(STYLE_PROMPTS.keys())}")
    
    # 验证强度参数
    if not 0.1 <= strength <= 1.0:
        raise ValueError("strength 必须在 0.1-1.0 之间")
    
    # 获取风格prompt
    style_prompt = STYLE_PROMPTS[style]
    
    print(f"🖼️  输入图片: {image}")
    print(f"🎨 目标风格: {style}")
    print(f"💪 风格强度: {strength}")
    print(f"📝 风格Prompt: {style_prompt[:60]}...")
    print()
    
    results = {}
    
    # 主模型: Kling v3
    print("🚀 使用 Kling v3 转换中...")
    try:
        start = time.time()
        result = style_image_with_model(
            MODELS["kling"],
            image,
            style_prompt,
            strength
        )
        elapsed = time.time() - start
        
        images = result.get("images", [])
        if images:
            url = images[0]["url"]
            urllib.request.urlretrieve(url, output_path)
            results["kling"] = {
                "url": url,
                "local": output_path,
                "time": elapsed,
            }
            print(f"   ✅ 成功 ({elapsed:.1f}s) → {output_path}")
        else:
            print(f"   ❌ 失败: 无图像返回")
            results["kling"] = {"error": "无图像返回"}
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results["kling"] = {"error": str(e)}
    
    # 对比测试其他模型
    if compare:
        print("\n📊 对比测试其他模型...")
        
        # GLM
        print("🚀 使用 GLM 转换中...")
        try:
            start = time.time()
            result = style_image_with_model(
                MODELS["glm"],
                image,
                style_prompt,
                strength
            )
            elapsed = time.time() - start
            
            images = result.get("images", [])
            if images:
                url = images[0]["url"]
                compare_path = output_path.replace(".png", "-glm.png")
                urllib.request.urlretrieve(url, compare_path)
                results["glm"] = {
                    "url": url,
                    "local": compare_path,
                    "time": elapsed,
                }
                print(f"   ✅ 成功 ({elapsed:.1f}s) → {compare_path}")
            else:
                results["glm"] = {"error": "无图像返回"}
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            results["glm"] = {"error": str(e)}
        
        # Grok
        print("🚀 使用 Grok 转换中...")
        try:
            start = time.time()
            result = style_image_with_model(
                MODELS["grok"],
                image,
                style_prompt,
                strength
            )
            elapsed = time.time() - start
            
            images = result.get("images", [])
            if images:
                url = images[0]["url"]
                compare_path = output_path.replace(".png", "-grok.png")
                urllib.request.urlretrieve(url, compare_path)
                results["grok"] = {
                    "url": url,
                    "local": compare_path,
                    "time": elapsed,
                }
                print(f"   ✅ 成功 ({elapsed:.1f}s) → {compare_path}")
            else:
                results["grok"] = {"error": "无图像返回"}
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            results["grok"] = {"error": str(e)}
    
    return results


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="图片风格转换器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py --image ./photo.jpg --style cyberpunk
  python run.py --image https://example.com/pic.png --style anime --strength 0.8
  python run.py --image ./me.png --style cinematic --compare
        """
    )
    parser.add_argument(
        "--image", "-i",
        required=True,
        help="输入图片路径或URL（必填）"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["cyberpunk", "minimal", "anime", "cinematic"],
        default="cyberpunk",
        help="目标风格 (默认: cyberpunk)"
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=0.7,
        help="风格强度 0.1-1.0 (默认: 0.7)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output.png",
        help="输出文件路径 (默认: ./output.png)"
    )
    parser.add_argument(
        "--compare", "-c",
        action="store_true",
        help="对比测试多个模型（生成额外图片）"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ImageStyler — 图片风格转换器")
    print("=" * 60)
    print()
    
    try:
        results = style_image(
            image=args.image,
            style=args.style,
            strength=args.strength,
            output_path=args.output,
            compare=args.compare,
        )
        
        print("\n" + "=" * 60)
        print("转换结果")
        print("=" * 60)
        
        for model, result in results.items():
            if "url" in result:
                print(f"\n📷 {model.upper()}:")
                print(f"   URL: {result['url']}")
                print(f"   本地: {result['local']}")
                print(f"   耗时: {result['time']:.1f}s")
            else:
                print(f"\n❌ {model.upper()}: {result.get('error', '未知错误')}")
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ 参数错误: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 转换失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
