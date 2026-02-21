#!/usr/bin/env python3
"""
VoiceClone — 声音克隆 Skill
使用 fal-ai/minimax/speech-2.8-hd 克隆声音并合成语音

用法:
    python run.py --sample <样本音频> --text "要合成的文字" [--output ./cloned.mp3] [--lang zh] [--speed 1.0]
    python run.py --sample ./voice_sample.mp3 --text "你好，这是克隆的声音" --lang zh --speed 1.0

注意: 样本音频需要 3 秒以上，本地文件会自动上传到 FAL
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


def upload_audio_if_needed(audio_path: str) -> str:
    """
    如果是本地文件，上传到 FAL 获取 URL
    
    Args:
        audio_path: 音频路径或 URL
        
    Returns:
        str: 可访问的 URL
    """
    if audio_path.startswith("http://") or audio_path.startswith("https://"):
        return audio_path
    
    print(f"📤 上传声音样本: {audio_path}")
    url = fal_client.upload_file(audio_path)
    print(f"   ✅ 上传完成")
    return url


def clone_voice(
    sample_path: str,
    text: str,
    lang: str = "zh",
    speed: float = 1.0,
    output_path: str = "./cloned.mp3",
) -> dict:
    """
    使用声音克隆合成语音
    
    Args:
        sample_path: 声音样本文件路径或 URL（3秒以上）
        text: 要合成的文字内容
        lang: 语言 (zh/en)
        speed: 语速，范围 0.5-2.0
        output_path: 输出文件路径
        
    Returns:
        dict: 生成结果
    """
    if not FAL_KEY:
        raise ValueError("未设置 FAL_KEY 环境变量")
    
    # 验证语速参数
    if not (0.5 <= speed <= 2.0):
        raise ValueError(f"语速参数 speed 必须在 0.5-2.0 范围内，当前: {speed}")
    
    os.environ["FAL_KEY"] = FAL_KEY
    
    # 上传样本音频
    sample_url = upload_audio_if_needed(sample_path)
    
    # 构建参数
    arguments = {
        "prompt": text,
        "reference_audio": sample_url,
        "speed": speed,
    }
    
    print(f"🎙️  正在克隆声音...")
    print(f"📄 合成文本: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"🌐 语言: {lang}")
    print(f"⚡ 语速: {speed}x")
    print()
    
    try:
        start = time.time()
        
        # 使用 MiniMax Speech-2.8-HD 进行声音克隆
        result = fal_client.run(
            "fal-ai/minimax/speech-2.8-hd",
            arguments=arguments,
        )
        
        elapsed = time.time() - start
        
        # 解析结果 - MiniMax 返回格式: {'audio': {'url': '...', ...}, 'duration_ms': 2772}
        audio_data = result.get("audio", {})
        audio_url = audio_data.get("url")
        duration_ms = result.get("duration_ms")
        duration = duration_ms / 1000 if duration_ms else None
        
        if audio_url:
            urllib.request.urlretrieve(audio_url, output_path)
            return {
                "url": audio_url,
                "local": output_path,
                "duration": duration,
                "time": elapsed,
                "text": text,
                "speed": speed,
                "success": True,
            }
        else:
            return {
                "error": "未获取到音频URL",
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
        description="声音克隆合成器 (Powered by MiniMax Speech-2.8-HD with Voice Cloning)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础使用（中文，默认语速）
  python run.py --sample ./voice_sample.mp3 --text "你好，这是克隆的声音"
  
  # 英文合成，调整语速
  python run.py --sample ./english_voice.wav --text "Hello, this is cloned voice." --lang en --speed 0.9
  
  # 指定输出文件
  python run.py --sample ./myvoice.mp3 --text "欢迎使用声音克隆技术" --output ./welcome.mp3
  
  # 使用在线样本
  python run.py --sample "https://example.com/voice.mp3" --text "在线样本测试"

注意:
  - 样本音频建议 3 秒以上，音质越好克隆效果越好
  - 语速范围: 0.5-2.0 (默认 1.0)
        """
    )
    parser.add_argument(
        "--sample", "-s",
        required=True,
        help="声音样本文件路径或 URL（必填，建议 3 秒以上）"
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="要合成的文字内容（必填）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./cloned.mp3",
        help="输出文件路径 (默认: ./cloned.mp3)"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en"],
        default="zh",
        help="语言 (默认: zh)"
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="语速，范围 0.5-2.0 (默认: 1.0)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("VoiceClone — 声音克隆")
    print("Powered by MiniMax Speech-2.8-HD")
    print("=" * 60)
    print()
    
    try:
        result = clone_voice(
            sample_path=args.sample,
            text=args.text,
            lang=args.lang,
            speed=args.speed,
            output_path=args.output,
        )
        
        if not result.get("success"):
            raise Exception(result.get("error", "生成失败"))
        
        print("=" * 60)
        print("生成完成")
        print("=" * 60)
        print(f"\n✅ 合成耗时: {result['time']:.1f}s")
        print(f"🔊 音频URL: {result['url']}")
        print(f"💾 本地保存: {result['local']}")
        if result.get('duration'):
            print(f"⏱️  音频时长: {result['duration']:.1f}秒")
        print(f"\n📝 合成文本: {result['text']}")
        print(f"⚡ 语速: {result['speed']}x")
        print(f"🌐 语言: {args.lang}")
        
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
