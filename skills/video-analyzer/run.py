#!/usr/bin/env python3
"""
VideoAnalyzer — 视频内容分析 Skill
使用 Moonshot Kimi-k2.5 多模态模型分析视频内容

用法:
    python run.py --video <视频路径或URL> [--lang zh] [--output ./analysis.md] [--mode summary]
    python run.py --video "https://example.com/video.mp4" --lang en --mode detail

模式选项:
    summary - 内容摘要 + 关键场景 + 推荐标签 (默认)
    detail  - 详细分析 + 时间线 + 完整场景描述
"""
import argparse
import os
import sys
import time
from typing import Optional
from openai import OpenAI

# Moonshot API 配置
MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY", "")
MOONSHOT_BASE_URL = "https://api.moonshot.cn/v1"
MOONSHOT_MODEL = "kimi-k2.5"


def analyze_video(
    video_path: str,
    lang: str = "zh",
    mode: str = "summary",
) -> dict:
    """
    使用 Moonshot Kimi-k2.5 分析视频内容
    
    Args:
        video_path: 视频文件路径或 URL
        lang: 输出语言 (zh/en)
        mode: 分析模式 (summary/detail)
        
    Returns:
        dict: 分析结果
    """
    if not MOONSHOT_API_KEY:
        raise ValueError("未设置 MOONSHOT_API_KEY 环境变量")
    
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url=MOONSHOT_BASE_URL,
    )
    
    # 构建系统提示词
    if lang == "zh":
        if mode == "summary":
            system_prompt = """你是一位专业的视频内容分析师。请分析用户提供的视频，并以结构化格式输出：

## 内容摘要
用2-3句话概括视频的核心内容。

## 关键场景
- 场景1: [时间戳] [简要描述]
- 场景2: [时间戳] [简要描述]
- 场景3: [时间戳] [简要描述]

## 推荐标签
#标签1 #标签2 #标签3 #标签4 #标签5

请确保分析客观准确，突出视频的核心价值。"""
        else:  # detail mode
            system_prompt = """你是一位专业的视频内容分析师。请对用户提供的视频进行详细分析，并以结构化格式输出：

## 内容概述
详细描述视频的主题、背景、目的和整体结构。

## 时间线分析
- [00:00-00:30] 开场/引入: [描述]
- [00:30-01:00] 第一部分: [描述]
- [后续时间段...]

## 关键场景详解
1. **场景1** ([时间])
   - 视觉元素: [描述]
   - 音频/对话: [描述]
   - 情感氛围: [描述]

2. **场景2** ([时间])
   - [同上结构]

## 技术质量评估
- 画面质量: [评价]
- 音频质量: [评价]
- 剪辑节奏: [评价]

## 推荐标签
#标签1 #标签2 #标签3 #标签4 #标签5 #标签6"""
    else:  # English
        if mode == "summary":
            system_prompt = """You are a professional video content analyst. Please analyze the video provided and output in structured format:

## Content Summary
Summarize the video's core content in 2-3 sentences.

## Key Scenes
- Scene 1: [timestamp] [brief description]
- Scene 2: [timestamp] [brief description]
- Scene 3: [timestamp] [brief description]

## Recommended Tags
#tag1 #tag2 #tag3 #tag4 #tag5

Ensure your analysis is objective and highlights the video's core value."""
        else:
            system_prompt = """You are a professional video content analyst. Please provide a detailed analysis of the video in structured format:

## Content Overview
Detailed description of the video's theme, background, purpose, and overall structure.

## Timeline Analysis
- [00:00-00:30] Opening/Introduction: [description]
- [00:30-01:00] Part 1: [description]
- [subsequent timestamps...]

## Key Scenes Detail
1. **Scene 1** ([time])
   - Visual elements: [description]
   - Audio/Dialogue: [description]
   - Emotional tone: [description]

2. **Scene 2** ([time])
   - [same structure]

## Technical Quality Assessment
- Visual quality: [assessment]
- Audio quality: [assessment]
- Pacing/Editing: [assessment]

## Recommended Tags
#tag1 #tag2 #tag3 #tag4 #tag5 #tag6"""
    
    # 构建用户消息内容
    content = [
        {"type": "text", "text": "请分析这个视频的内容。" if lang == "zh" else "Please analyze the content of this video."}
    ]
    
    # 判断是 URL 还是本地文件
    if video_path.startswith("http://") or video_path.startswith("https://"):
        # 直接使用 URL
        content.append({
            "type": "video_url",
            "video_url": {"url": video_path}
        })
    else:
        # 本地文件，读取并转为 base64
        import base64
        import mimetypes
        
        mime_type, _ = mimetypes.guess_type(video_path)
        if not mime_type:
            mime_type = "video/mp4"
        
        with open(video_path, "rb") as f:
            video_data = base64.b64encode(f.read()).decode('utf-8')
        
        content.append({
            "type": "video_url",
            "video_url": {
                "url": f"data:{mime_type};base64,{video_data}"
            }
        })
    
    print(f"🎬 正在分析视频: {video_path}")
    print(f"🌐 语言: {'中文' if lang == 'zh' else 'English'}")
    print(f"📊 模式: {'摘要' if mode == 'summary' else '详细'}")
    print()
    
    try:
        start = time.time()
        response = client.chat.completions.create(
            model=MOONSHOT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=1.0,
            max_tokens=4096,
        )
        elapsed = time.time() - start
        
        analysis = response.choices[0].message.content
        
        return {
            "analysis": analysis,
            "time": elapsed,
            "success": True,
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="视频内容分析器 (Powered by Moonshot Kimi-k2.5)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析视频并生成中文摘要
  python run.py --video ./myvideo.mp4
  
  # 分析在线视频，输出英文详细分析
  python run.py --video "https://example.com/video.mp4" --lang en --mode detail
  
  # 指定输出文件
  python run.py --video ./video.mp4 --output ./report.md
        """
    )
    parser.add_argument(
        "--video", "-v",
        required=True,
        help="视频文件路径或 URL（必填）"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en"],
        default="zh",
        help="输出语言 (默认: zh)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./analysis.md",
        help="输出文件路径 (默认: ./analysis.md)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["summary", "detail"],
        default="summary",
        help="分析模式: summary(摘要) 或 detail(详细) (默认: summary)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("VideoAnalyzer — 视频内容分析")
    print("Powered by Moonshot Kimi-k2.5")
    print("=" * 60)
    print()
    
    try:
        result = analyze_video(
            video_path=args.video,
            lang=args.lang,
            mode=args.mode,
        )
        
        if not result.get("success"):
            raise Exception(result.get("error", "分析失败"))
        
        # 保存到文件
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# 视频分析报告\n\n")
            f.write(f"**视频来源**: {args.video}\n\n")
            f.write(f"**分析模式**: {args.mode}\n\n")
            f.write(f"**分析时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(result["analysis"])
        
        print("=" * 60)
        print("分析完成")
        print("=" * 60)
        print(f"\n✅ 分析耗时: {result['time']:.1f}s")
        print(f"📝 结果已保存: {args.output}")
        print(f"\n📊 分析报告预览:")
        print("-" * 60)
        # 打印前500字符预览
        preview = result["analysis"][:500]
        print(preview + "..." if len(result["analysis"]) > 500 else preview)
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
