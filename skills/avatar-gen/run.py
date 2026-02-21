#!/usr/bin/env python3
"""
AvatarGen — 动态 Avatar 生成 Skill
使用 fal-ai/bytedance/dreamactor/v2 将人物图片转换为动态视频

用法:
    python run.py --image <人物图片路径或URL> [--motion <动作视频>] [--output ./avatar.mp4] [--duration 5]
    python run.py --image ./portrait.png --motion ./dance.mp4 --duration 10

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


def upload_file_if_needed(file_path: str) -> str:
    """
    如果是本地文件，上传到 FAL 获取 URL
    
    Args:
        file_path: 文件路径或 URL
        
    Returns:
        str: 可访问的 URL
    """
    if file_path.startswith("http://") or file_path.startswith("https://"):
        return file_path
    
    print(f"📤 上传本地文件: {file_path}")
    url = fal_client.upload_file(file_path)
    print(f"   ✅ 上传完成")
    return url


def generate_avatar(
    image_path: str,
    motion_path: Optional[str] = None,
    duration: int = 5,
    output_path: str = "./avatar.mp4",
) -> dict:
    """
    使用 DreamActor v2 生成动态 Avatar 视频
    
    Args:
        image_path: 人物图片路径或 URL
        motion_path: 动作参考视频路径或 URL (可选)
        duration: 视频时长 (5 或 10 秒)
        output_path: 输出文件路径
        
    Returns:
        dict: 生成结果
    """
    if not FAL_KEY:
        raise ValueError("未设置 FAL_KEY 环境变量")
    
    os.environ["FAL_KEY"] = FAL_KEY
    
    # 上传图片
    image_url = upload_file_if_needed(image_path)
    
    # 构建参数
    arguments = {
        "image_url": image_url,
        "duration": duration,
    }
    
    # 如果提供了动作视频，添加 motion_url
    if motion_path:
        motion_url = upload_file_if_needed(motion_path)
        arguments["video_url"] = motion_url
    
    print(f"🎭 正在生成动态 Avatar...")
    print(f"👤 参考图片: {image_path}")
    if motion_path:
        print(f"💃 动作参考: {motion_path}")
    print(f"⏱️  视频时长: {duration}秒")
    print()
    
    try:
        start = time.time()
        
        # 提交异步任务
        handler = fal_client.submit(
            "fal-ai/bytedance/dreamactor/v2",
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
            video_url = result.get("video", {}).get("url") if isinstance(result.get("video"), dict) else None
            if not video_url:
                video_url = result.get("video_url")
            if not video_url:
                # 可能直接返回视频对象
                video_data = result.get("video", result)
                if isinstance(video_data, dict):
                    video_url = video_data.get("url")
        
        if video_url:
            urllib.request.urlretrieve(video_url, output_path)
            return {
                "url": video_url,
                "local": output_path,
                "time": elapsed,
                "request_id": handler.request_id,
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
        description="动态 Avatar 生成器 (Powered by DreamActor v2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础使用（生成 5 秒视频，使用默认动作）
  python run.py --image ./portrait.png
  
  # 指定动作参考视频，生成 10 秒
  python run.py --image ./portrait.png --motion ./dance.mp4 --duration 10
  
  # 使用在线图片
  python run.py --image "https://example.com/photo.jpg" --output ./myavatar.mp4
  
  # 本地图片 + 在线动作视频
  python run.py --image ./photo.png --motion "https://example.com/motion.mp4"
        """
    )
    parser.add_argument(
        "--image", "-i",
        required=True,
        help="人物图片路径或 URL（必填）"
    )
    parser.add_argument(
        "--motion", "-m",
        default=None,
        help="动作参考视频路径或 URL（可选，用于驱动 Avatar 动作）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./avatar.mp4",
        help="输出文件路径 (默认: ./avatar.mp4)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        choices=[5, 10],
        default=5,
        help="视频时长，可选 5 或 10 秒 (默认: 5)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AvatarGen — 动态 Avatar 生成")
    print("Powered by fal-ai/bytedance/dreamactor/v2")
    print("=" * 60)
    print()
    
    try:
        result = generate_avatar(
            image_path=args.image,
            motion_path=args.motion,
            duration=args.duration,
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
        print(f"\n🎬 视频时长: {args.duration}秒")
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
