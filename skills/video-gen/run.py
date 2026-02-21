#!/usr/bin/env python3
"""
VideoGen — AI 视频生成 Skill
使用 fal-ai/bytedance/seedance/v1/pro 或 fal-ai/kling-video/v3/pro 生成短视频

用法:
    # 文字生成视频
    python run.py --prompt "一只猫在弹钢琴" --duration 5 --style realistic
    
    # 图片生成视频
    python run.py --image ./photo.png --duration 10 --style cinematic
    
    # 使用 Kling 模型
    python run.py --prompt "太空漫步" --model kling --duration 5

注意: 本地图片会自动上传到 FAL
"""
import argparse
import os
import sys
import time
import urllib.request
from typing import Optional

import fal_client

# FAL API Key
FAL_KEY = os.environ.get("FAL_KEY", "")

# 模型端点
MODELS = {
    "kling": "fal-ai/kling-video/v3/pro/text-to-video",
    "seedance": "fal-ai/bytedance/seedance/v1/pro",
}

# 风格预设
STYLE_PRESETS = {
    "realistic": "realistic, photorealistic, high quality, detailed",
    "anime": "anime style, animated, cartoon, japanese animation style",
    "cinematic": "cinematic, film look, dramatic lighting, movie quality, professional cinematography",
}


def upload_image_if_needed(image_path: str) -> str:
    """
    如果是本地文件，上传到 FAL 获取 URL
    
    Args:
        image_path: 图片路径或 URL
        
    Returns:
        str: 可访问的 URL
    """
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path
    
    print(f"📤 上传本地图片: {image_path}")
    url = fal_client.upload_file(image_path)
    print(f"   ✅ 上传完成")
    return url


def generate_video(
    prompt: Optional[str] = None,
    image_path: Optional[str] = None,
    duration: int = 5,
    style: str = "realistic",
    model: str = "kling",
    output_path: str = "./output.mp4",
) -> dict:
    """
    使用 AI 模型生成视频
    
    Args:
        prompt: 文字描述（与 image_path 二选一）
        image_path: 图片路径或 URL（与 prompt 二选一）
        duration: 视频时长 (5 或 10 秒)
        style: 风格 (realistic/anime/cinematic)
        model: 模型 (seedance/kling)
        output_path: 输出文件路径
        
    Returns:
        dict: 生成结果
    """
    if not FAL_KEY:
        raise ValueError("未设置 FAL_KEY 环境变量")
    
    if not prompt and not image_path:
        raise ValueError("请提供 --prompt 或 --image 参数之一")
    
    if prompt and image_path:
        raise ValueError("--prompt 和 --image 参数不能同时使用")
    
    os.environ["FAL_KEY"] = FAL_KEY
    
    model_id = MODELS.get(model, MODELS["seedance"])
    
    # 构建参数
    arguments = {}
    
    # 添加提示词或图片
    if prompt:
        # 组合风格和提示词
        style_desc = STYLE_PRESETS.get(style, STYLE_PRESETS["realistic"])
        full_prompt = f"{prompt}, {style_desc}"
        arguments["prompt"] = full_prompt
    else:
        # 上传图片
        image_url = upload_image_if_needed(image_path)
        arguments["image_url"] = image_url
        
        # 对于图生视频，可以添加运动描述
        if style != "realistic":
            style_desc = STYLE_PRESETS.get(style, "")
            arguments["prompt"] = style_desc
    
    # 添加时长（如果模型支持）
    if model == "seedance":
        arguments["duration"] = duration
    elif model == "kling":
        # Kling 可能需要不同的参数名
        arguments["duration"] = duration
    
    print(f"🎬 正在生成视频...")
    if prompt:
        print(f"📝 提示词: {prompt}")
    if image_path:
        print(f"🖼️  参考图片: {image_path}")
    print(f"🎨 风格: {style}")
    print(f"🤖 模型: {model}")
    print(f"⏱️  时长: {duration}秒")
    print()
    
    try:
        start = time.time()
        
        # 提交异步任务
        handler = fal_client.submit(
            model_id,
            arguments=arguments,
        )
        
        print(f"🚀 任务已提交，等待生成...")
        print(f"   请求ID: {handler.request_id}")
        print()
        
        # 等待完成并获取结果
        result = handler.get()
        elapsed = time.time() - start
        
        # 解析结果
        video_url = None
        
        if isinstance(result, dict):
            # 尝试不同可能的返回格式
            if isinstance(result.get("video"), dict):
                video_url = result["video"].get("url")
            else:
                video_url = result.get("video_url")
            
            if not video_url:
                # 可能返回的是视频对象列表
                videos = result.get("videos", [])
                if videos and isinstance(videos[0], dict):
                    video_url = videos[0].get("url")
            
            if not video_url:
                # 直接检查 result 的 url 字段
                video_url = result.get("url")
        
        if video_url:
            urllib.request.urlretrieve(video_url, output_path)
            return {
                "url": video_url,
                "local": output_path,
                "time": elapsed,
                "request_id": handler.request_id,
                "model": model,
                "success": True,
            }
        else:
            return {
                "error": "未获取到视频URL",
                "raw": str(result),
                "success": False,
            }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="AI 视频生成器 (Powered by Seedance/Kling)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文字生成视频（默认 Kling 模型）
  python run.py --prompt "一只猫在弹钢琴"

  # 指定风格和时长
  python run.py --prompt "太空漫步的宇航员" --style cinematic --duration 10

  # 图片生成视频
  python run.py --image ./photo.png --duration 5 --style realistic

  # 使用 Seedance 模型（备选）
  python run.py --prompt "日落海滩" --model seedance --duration 5

  # 动漫风格
  python run.py --prompt "樱花树下的少女" --style anime --duration 5

注意:
  - --prompt 和 --image 参数二选一，不能同时提供
  - 本地图片会自动上传到 FAL
  - 视频生成需要一定时间，请耐心等待
        """
    )
    parser.add_argument(
        "--prompt", "-p",
        help="文字描述（与 --image 二选一）"
    )
    parser.add_argument(
        "--image", "-i",
        help="图片路径或 URL（与 --prompt 二选一，用于图生视频）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output.mp4",
        help="输出文件路径 (默认: ./output.mp4)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        choices=[5, 10],
        default=5,
        help="视频时长，可选 5 或 10 秒 (默认: 5)"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["realistic", "anime", "cinematic"],
        default="realistic",
        help="视频风格 (默认: realistic)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["seedance", "kling"],
        default="kling",
        help="使用模型 (默认: kling, seedance 为备选)"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.prompt and not args.image:
        parser.error("请提供 --prompt 或 --image 参数之一")
    
    if args.prompt and args.image:
        parser.error("--prompt 和 --image 参数不能同时使用，请选择一个")
    
    print("=" * 60)
    print("VideoGen — AI 视频生成")
    print(f"Powered by {MODELS[args.model]}")
    print("=" * 60)
    print()
    
    try:
        result = generate_video(
            prompt=args.prompt,
            image_path=args.image,
            duration=args.duration,
            style=args.style,
            model=args.model,
            output_path=args.output,
        )
        
        if not result.get("success"):
            raise Exception(result.get("error", "生成失败"))
        
        print("=" * 60)
        print("生成完成")
        print("=" * 60)
        print(f"\n✅ 生成耗时: {result['time']:.1f}s")
        print(f"📹 视频URL: {result['url']}")
        print(f"💾 本地保存: {result['local']}")
        print(f"🆔 请求ID: {result['request_id']}")
        print(f"🤖 使用模型: {result['model']}")
        print(f"\n🎬 视频信息:")
        print(f"   时长: {args.duration}秒")
        print(f"   风格: {args.style}")
        if args.prompt:
            print(f"   提示词: {args.prompt}")
        if args.image:
            print(f"   参考图片: {args.image}")
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ 参数错误: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
