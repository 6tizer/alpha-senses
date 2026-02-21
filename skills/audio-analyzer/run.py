#!/usr/bin/env python3
"""
AudioAnalyzer — 音频分析 Skill
使用 fal-ai/personaplex 进行语音转文字、情绪分析和内容摘要

用法:
    python run.py --audio <音频路径或URL> [--lang auto] [--output ./transcript.md] [--emotion]
    python run.py --audio ./recording.mp3 --lang zh --emotion

支持格式: mp3, wav, m4a, ogg, flac
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
    
    print(f"📤 上传本地音频: {audio_path}")
    url = fal_client.upload_file(audio_path)
    print(f"   ✅ 上传完成")
    return url


def analyze_audio(
    audio_path: str,
    lang: str = "auto",
    emotion: bool = True,
) -> dict:
    """
    使用 fal-ai/personaplex 分析音频
    
    Args:
        audio_path: 音频文件路径或 URL
        lang: 语言 (zh/en/auto，默认 auto)
        emotion: 是否进行情绪分析
        
    Returns:
        dict: 分析结果包含 transcript, emotion, summary
    """
    if not FAL_KEY:
        raise ValueError("未设置 FAL_KEY 环境变量")
    
    os.environ["FAL_KEY"] = FAL_KEY
    
    # 上传本地文件
    audio_url = upload_audio_if_needed(audio_path)
    
    # 构建参数
    arguments = {
        "audio_url": audio_url,
    }
    
    if lang != "auto":
        arguments["language"] = lang
    
    print(f"🎙️  正在分析音频...")
    print(f"🌐 语言: {lang}")
    print(f"😊 情绪分析: {'开启' if emotion else '关闭'}")
    print()
    
    try:
        start = time.time()
        result = fal_client.run(
            "fal-ai/personaplex",
            arguments=arguments,
        )
        elapsed = time.time() - start
        
        # 解析结果
        transcript = ""
        segments = []
        
        if isinstance(result, dict):
            # 尝试不同可能的返回格式
            transcript = result.get("text", "")
            if not transcript:
                transcript = result.get("transcript", "")
            
            segments = result.get("segments", [])
            if not segments and "chunks" in result:
                segments = result.get("chunks", [])
        
        # 如果没有获得文本，尝试其他方式
        if not transcript and segments:
            transcript = " ".join([s.get("text", "") for s in segments])
        
        # 情绪分析（如果开启且没有直接返回）
        emotion_result = None
        if emotion:
            emotion_result = analyze_emotion(transcript) if transcript else None
        
        return {
            "transcript": transcript,
            "segments": segments,
            "emotion": emotion_result,
            "raw": result,
            "time": elapsed,
            "success": True,
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }


def analyze_emotion(transcript: str) -> dict:
    """
    对转录文本进行情绪分析
    
    Args:
        transcript: 转录文本
        
    Returns:
        dict: 情绪分析结果
    """
    # 简单的关键词情绪分析
    # 实际生产环境可以使用更复杂的 NLP 模型
    
    emotion_keywords = {
        "positive": ["好", "棒", "优秀", "开心", "喜欢", "感谢", "赞", "完美", "good", "great", "excellent", "happy", "love", "thanks", "amazing"],
        "negative": ["差", "糟", "讨厌", "失望", "难过", "坏", "问题", "错误", "bad", "terrible", "hate", "disappointed", "sad", "wrong", "error"],
        "excited": ["激动", "兴奋", "太棒了", "哇", "天哪", "excited", "wow", "amazing", "incredible"],
        "calm": ["平静", "放松", "安静", "舒适", "calm", "relax", "peaceful", "comfortable"],
    }
    
    transcript_lower = transcript.lower()
    
    scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for kw in keywords if kw in transcript_lower)
        scores[emotion] = score
    
    # 找出主要情绪
    total = sum(scores.values())
    if total > 0:
        dominant = max(scores, key=scores.get)
        percentages = {k: round(v / total * 100, 1) for k, v in scores.items()}
    else:
        dominant = "neutral"
        percentages = {k: 0 for k in emotion_keywords.keys()}
        percentages["neutral"] = 100
    
    return {
        "dominant": dominant,
        "percentages": percentages,
        "scores": scores,
    }


def summarize_transcript(transcript: str, lang: str = "zh") -> str:
    """
    生成内容摘要
    
    Args:
        transcript: 转录文本
        lang: 语言
        
    Returns:
        str: 摘要
    """
    # 简单的摘要生成
    # 实际生产环境可以使用 LLM
    
    sentences = transcript.split("。") if lang == "zh" else transcript.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 3:
        return transcript
    
    # 取前几句作为摘要
    summary_count = min(3, len(sentences) // 3 + 1)
    if lang == "zh":
        summary = "。".join(sentences[:summary_count]) + "。"
    else:
        summary = ". ".join(sentences[:summary_count]) + "."
    
    return summary


def format_output(result: dict, emotion: bool = True) -> str:
    """
    格式化输出结果
    
    Args:
        result: 分析结果
        emotion: 是否包含情绪分析
        
    Returns:
        str: 格式化的 Markdown 文本
    """
    lines = []
    
    # 完整转录
    lines.append("# 音频分析报告")
    lines.append("")
    lines.append("## 完整转录")
    lines.append("")
    lines.append("```")
    lines.append(result.get("transcript", "N/A"))
    lines.append("```")
    lines.append("")
    
    # 内容摘要
    transcript = result.get("transcript", "")
    if transcript:
        summary = summarize_transcript(transcript)
        lines.append("## 内容摘要")
        lines.append("")
        lines.append(summary)
        lines.append("")
    
    # 情绪分析
    if emotion and result.get("emotion"):
        emotion_data = result["emotion"]
        lines.append("## 情绪分析")
        lines.append("")
        lines.append(f"**主要情绪**: {emotion_data.get('dominant', 'neutral')}")
        lines.append("")
        lines.append("**情绪分布**:")
        for emotion_type, percentage in emotion_data.get("percentages", {}).items():
            lines.append(f"- {emotion_type}: {percentage}%")
        lines.append("")
    
    # 时间线
    segments = result.get("segments", [])
    if segments:
        lines.append("## 时间线")
        lines.append("")
        for seg in segments[:20]:  # 最多显示20段
            start = seg.get("start", 0)
            end = seg.get("end", 0)
            text = seg.get("text", "")
            
            # 格式化时间
            start_str = f"{int(start // 60):02d}:{int(start % 60):02d}"
            end_str = f"{int(end // 60):02d}:{int(end % 60):02d}"
            
            lines.append(f"**[{start_str} - {end_str}]** {text}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="音频分析器 (Powered by fal-ai/personaplex)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础使用（自动检测语言）
  python run.py --audio ./recording.mp3
  
  # 指定中文，开启情绪分析
  python run.py --audio ./meeting.wav --lang zh --emotion
  
  # 分析在线音频
  python run.py --audio "https://example.com/audio.mp3" --output ./report.md
  
  # 仅转录，不输出情绪分析
  python run.py --audio ./podcast.mp3 --no-emotion
        """
    )
    parser.add_argument(
        "--audio", "-a",
        required=True,
        help="音频文件路径或 URL（必填，支持 mp3/wav/m4a/ogg/flac）"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en", "auto"],
        default="auto",
        help="语言 (默认: auto 自动检测)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./transcript.md",
        help="输出文件路径 (默认: ./transcript.md)"
    )
    parser.add_argument(
        "--emotion", "-e",
        action="store_true",
        default=True,
        help="输出情绪分析 (默认开启)"
    )
    parser.add_argument(
        "--no-emotion",
        action="store_true",
        help="关闭情绪分析"
    )
    
    args = parser.parse_args()
    
    # 处理 --no-emotion
    emotion = not args.no_emotion
    
    print("=" * 60)
    print("AudioAnalyzer — 音频分析")
    print("Powered by fal-ai/personaplex")
    print("=" * 60)
    print()
    
    try:
        result = analyze_audio(
            audio_path=args.audio,
            lang=args.lang,
            emotion=emotion,
        )
        
        if not result.get("success"):
            raise Exception(result.get("error", "分析失败"))
        
        # 格式化输出
        output_content = format_output(result, emotion)
        
        # 保存到文件
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        
        print("=" * 60)
        print("分析完成")
        print("=" * 60)
        print(f"\n✅ 分析耗时: {result['time']:.1f}s")
        print(f"📝 转录字数: {len(result.get('transcript', ''))}")
        print(f"💾 结果已保存: {args.output}")
        
        # 打印转录预览
        transcript = result.get("transcript", "")
        if transcript:
            print(f"\n📄 转录预览:")
            print("-" * 60)
            preview = transcript[:300]
            print(preview + "..." if len(transcript) > 300 else preview)
        
        # 打印情绪分析预览
        if emotion and result.get("emotion"):
            emotion_data = result["emotion"]
            print(f"\n😊 主要情绪: {emotion_data.get('dominant', 'neutral')}")
        
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
