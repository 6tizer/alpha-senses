#!/usr/bin/env python3
"""
TextToSpeech — 文字转语音
将文字转换为自然语音音频文件（基于MiniMax Speech 2.8 HD）

用法:
    python run.py --text "你好世界" --voice sweet_lady --output ./output.mp3
    python run.py --text "重要公告" --voice executive --speed 0.9 --emotion serious
    python run.py --text "测试所有音色" --test-all-voices

音色选项:
    # 中文音色
    sweet_lady    - 甜美女生 (温柔可爱)
    executive     - 商务男声 (稳重专业)
    wise_woman    - 知性女声 (成熟睿智)
    news_anchor   - 新闻主播 (中性正式)
    gentle_youth  - 温柔青年 (男声)
    warm_girl     - 温暖女生 (亲切自然)
    
    # 英文音色
    female_en     - 英文女声
    male_en       - 英文男声
"""
import argparse
import os
import sys
import time
import urllib.request
from typing import Optional, List, Dict
from dataclasses import dataclass

import fal_client

# FAL API Key
FAL_KEY = os.environ.get(
    "FAL_API_KEY",
    "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
)


@dataclass
class VoiceConfig:
    """音色配置类"""
    voice_id: str
    name: str
    description: str
    gender: str  # male/female/neutral
    language: str  # zh/en


# MiniMax Speech 2.8 HD 完整中文音色列表
# 来源: https://platform.minimax.io/docs/faq/system-voice-id
VOICE_CONFIGS: Dict[str, VoiceConfig] = {
    # === 中文音色 (Mandarin) ===
    "sweet_lady": VoiceConfig(
        voice_id="Chinese (Mandarin)_Sweet_Lady",
        name="甜美女生",
        description="温柔可爱的年轻女声，适合日常对话、故事讲述",
        gender="female",
        language="zh",
    ),
    "executive": VoiceConfig(
        voice_id="Chinese (Mandarin)_Reliable_Executive",
        name="商务男声",
        description="稳重专业的男声，适合商务播报、正式场合",
        gender="male",
        language="zh",
    ),
    "wise_woman": VoiceConfig(
        voice_id="Chinese (Mandarin)_Wise_Woman",
        name="知性女声",
        description="成熟睿智的女声，适合知识分享、深度内容",
        gender="female",
        language="zh",
    ),
    "news_anchor": VoiceConfig(
        voice_id="Chinese (Mandarin)_News_Anchor",
        name="新闻主播",
        description="标准中性新闻播报声音，适合资讯播报",
        gender="neutral",
        language="zh",
    ),
    "gentle_youth": VoiceConfig(
        voice_id="Chinese (Mandarin)_Gentle_Youth",
        name="温柔青年",
        description="温文尔雅的年轻男声，适合轻松内容",
        gender="male",
        language="zh",
    ),
    "warm_girl": VoiceConfig(
        voice_id="Chinese (Mandarin)_Warm_Girl",
        name="温暖女生",
        description="亲切自然的女声，适合情感类内容",
        gender="female",
        language="zh",
    ),
    
    # === 扩展中文音色 ===
    "mature_woman": VoiceConfig(
        voice_id="Chinese (Mandarin)_Mature_Woman",
        name="成熟女性",
        description="富有韵味的成熟女声",
        gender="female",
        language="zh",
    ),
    "gentleman": VoiceConfig(
        voice_id="Chinese (Mandarin)_Gentleman",
        name="绅士男声",
        description="优雅绅士风格的男声",
        gender="male",
        language="zh",
    ),
    "cute_spirit": VoiceConfig(
        voice_id="Chinese (Mandarin)_Cute_Spirit",
        name="可爱精灵",
        description="活泼可爱的少女声音",
        gender="female",
        language="zh",
    ),
    
    # === 英文音色 ===
    "female_en": VoiceConfig(
        voice_id="female-english",
        name="英文女声",
        description="专业英文女声",
        gender="female",
        language="en",
    ),
    "male_en": VoiceConfig(
        voice_id="male-english",
        name="英文男声",
        description="专业英文男声",
        gender="male",
        language="en",
    ),
}

# 情绪选项（MiniMax Speech 2.8 HD支持）
EMOTION_OPTIONS = {
    "neutral": None,  # 默认，不指定
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "fearful": "fearful",
    "surprised": "surprised",
    "calm": "calm",
    "serious": "calm",  # calm可用于严肃场合
    "fluent": "fluent",
}

# 测试用的中文文本
TEST_TEXT = """
你好，我是AI语音助手。今天我要测试不同的中文音色效果。
人工智能正在改变我们的生活方式，让技术更加人性化。
感谢你的聆听，希望这次测试对你有帮助。
""".strip()


def text_to_speech(
    text: str,
    voice_id: str,
    output_path: str = "./output.mp3",
    speed: float = 1.0,
    emotion: Optional[str] = None,
    verbose: bool = True,
) -> dict:
    """
    将文字转换为语音
    
    Args:
        text: 要转换的文字内容
        voice_id: MiniMax原生voice ID
        output_path: 输出文件路径
        speed: 语速，范围0.5-2.0，默认1.0
        emotion: 情绪选项 (happy/sad/angry/fearful/surprised/calm/fluent)
        verbose: 是否打印详细信息
        
    Returns:
        dict: 生成结果，包含 url、local 路径和 duration
    """
    # 验证参数
    if not (0.5 <= speed <= 2.0):
        raise ValueError(f"语速参数speed必须在0.5-2.0范围内，当前: {speed}")
    
    if verbose:
        print(f"📝 文字内容: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"🔊 Voice ID: {voice_id}")
        print(f"⚡ 语速: {speed}x")
        if emotion:
            print(f"😊 情绪: {emotion}")
        print()
    
    os.environ["FAL_KEY"] = FAL_KEY
    
    # 构建API参数
    arguments = {
        "prompt": text,
        "voice_id": voice_id,
        "speed": speed,
    }
    
    # 添加情绪参数（如果指定）
    if emotion and emotion in EMOTION_OPTIONS:
        emotion_value = EMOTION_OPTIONS[emotion]
        if emotion_value:
            arguments["emotion"] = emotion_value
    
    if verbose:
        print(f"🚀 调用 MiniMax Speech-2.8-HD 生成中...")
        print(f"   参数: {arguments}")
    
    try:
        start = time.time()
        result = fal_client.run(
            "fal-ai/minimax/speech-2.8-hd",
            arguments=arguments,
        )
        elapsed = time.time() - start
        
        # 解析结果
        audio_data = result.get("audio", {})
        audio_url = audio_data.get("url")
        duration_ms = result.get("duration_ms")
        duration = duration_ms / 1000 if duration_ms else None
        
        if audio_url:
            urllib.request.urlretrieve(audio_url, output_path)
            
            if verbose:
                print(f"   ✅ 成功 ({elapsed:.1f}s)")
                print(f"   💾 已保存: {output_path}")
                if duration:
                    print(f"   ⏱️  音频时长: {duration:.1f}秒")
            
            return {
                "url": audio_url,
                "local": output_path,
                "time": elapsed,
                "duration": duration,
                "voice_id": voice_id,
                "speed": speed,
                "emotion": emotion,
                "success": True,
            }
        else:
            raise Exception(f"无音频返回: {result}")
            
    except Exception as e:
        if verbose:
            print(f"   ❌ 失败: {e}")
        return {
            "error": str(e),
            "voice_id": voice_id,
            "success": False,
        }


def list_voices(language: Optional[str] = None) -> List[VoiceConfig]:
    """
    列出可用音色
    
    Args:
        language: 筛选语言 ('zh'/'en')，None表示全部
        
    Returns:
        List[VoiceConfig]: 音色配置列表
    """
    voices = list(VOICE_CONFIGS.values())
    if language:
        voices = [v for v in voices if v.language == language]
    return voices


def print_voice_list():
    """打印可用音色列表"""
    print("=" * 60)
    print("可用音色列表")
    print("=" * 60)
    
    # 中文音色
    print("\n🀄 中文音色:")
    zh_voices = list_voices("zh")
    for key, config in VOICE_CONFIGS.items():
        if config.language == "zh":
            gender_emoji = "👩" if config.gender == "female" else "👨" if config.gender == "male" else "🧑"
            print(f"  {gender_emoji} {key:15} - {config.name:10} | {config.description}")
    
    # 英文音色
    print("\n🇺🇸 英文音色:")
    for key, config in VOICE_CONFIGS.items():
        if config.language == "en":
            gender_emoji = "👩" if config.gender == "female" else "👨"
            print(f"  {gender_emoji} {key:15} - {config.name:10} | {config.description}")


def test_all_voices(output_dir: str = "./voice_test"):
    """
    测试所有中文音色并生成对比报告
    
    Args:
        output_dir: 测试音频输出目录
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🎙️  中文音色对比测试")
    print("=" * 60)
    print(f"\n测试文本:\n{TEST_TEXT}\n")
    print(f"输出目录: {output_dir}\n")
    
    zh_voices = list_voices("zh")
    results = []
    
    for i, config in enumerate(zh_voices, 1):
        # 找到对应的key
        voice_key = None
        for k, v in VOICE_CONFIGS.items():
            if v.voice_id == config.voice_id:
                voice_key = k
                break
        
        output_path = os.path.join(output_dir, f"test_{voice_key}.mp3")
        
        print(f"\n{'='*60}")
        print(f"[{i}/{len(zh_voices)}] 测试音色: {config.name}")
        print(f"Voice ID: {config.voice_id}")
        print(f"{'='*60}")
        
        result = text_to_speech(
            text=TEST_TEXT,
            voice_id=config.voice_id,
            output_path=output_path,
            speed=1.0,
            emotion=None,
            verbose=True,
        )
        
        results.append({
            "key": voice_key,
            "config": config,
            **result,
        })
    
    # 输出对比报告
    print("\n" + "=" * 60)
    print("📊 测试报告汇总")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    print(f"\n✅ 成功: {success_count}/{len(results)}")
    
    print("\n| 序号 | 音色Key | 名称 | 性别 | 时长 | 状态 | 文件路径 |")
    print("|------|---------|------|------|------|------|----------|")
    
    for i, r in enumerate(results, 1):
        config = r["config"]
        gender = "女" if config.gender == "female" else "男" if config.gender == "male" else "中"
        duration = f"{r['duration']:.1f}s" if r.get("duration") else "N/A"
        status = "✅" if r.get("success") else "❌"
        path = r.get("local", "N/A") if r.get("success") else r.get("error", "失败")
        
        print(f"| {i:2} | {r['key']:12} | {config.name:8} | {gender} | {duration:6} | {status} | {path} |")
    
    # 保存报告到文件
    report_path = os.path.join(output_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# MiniMax Speech 2.8 HD 中文音色测试报告\n\n")
        f.write(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 测试文本\n\n```\n{TEST_TEXT}\n```\n\n")
        f.write("## 测试结果\n\n")
        f.write("| 序号 | 音色Key | 名称 | 性别 | 描述 | 时长 | 状态 |\n")
        f.write("|------|---------|------|------|------|------|------|\n")
        
        for i, r in enumerate(results, 1):
            config = r["config"]
            gender = "女" if config.gender == "female" else "男" if config.gender == "male" else "中"
            duration = f"{r['duration']:.1f}s" if r.get("duration") else "N/A"
            status = "✅ 成功" if r.get("success") else f"❌ 失败: {r.get('error', '未知错误')}"
            
            f.write(f"| {i} | {r['key']} | {config.name} | {gender} | {config.description} | {duration} | {status} |\n")
        
        f.write("\n## 推荐音色\n\n")
        f.write("- **甜美女声**: sweet_lady - 适合日常对话、故事讲述\n")
        f.write("- **商务男声**: executive - 适合正式播报、商务场景\n")
        f.write("- **知性女声**: wise_woman - 适合知识分享、深度内容\n")
        f.write("- **新闻主播**: news_anchor - 适合新闻资讯、标准播报\n")
    
    print(f"\n📝 详细报告已保存: {report_path}")


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="文字转语音 (MiniMax Speech 2.8 HD)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础使用
  python run.py --text "你好，世界！" --voice sweet_lady
  
  # 调整语速和情绪
  python run.py --text "重要通知" --voice executive --speed 0.9 --emotion calm
  
  # 快速语速
  python run.py --text "快速播报" --voice news_anchor --speed 1.3
  
  # 列出所有音色
  python run.py --list-voices
  
  # 测试所有中文音色并生成报告
  python run.py --test-all-voices --output-dir ./voice_test
        """
    )
    parser.add_argument(
        "--text", "-t",
        help="要转换的文字内容"
    )
    parser.add_argument(
        "--voice", "-v",
        choices=list(VOICE_CONFIGS.keys()),
        default="sweet_lady",
        help="音色选项 (默认: sweet_lady)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output.mp3",
        help="输出文件路径 (默认: ./output.mp3)"
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=1.0,
        help="语速，范围0.5-2.0 (默认: 1.0)"
    )
    parser.add_argument(
        "--emotion", "-e",
        choices=list(EMOTION_OPTIONS.keys()),
        default=None,
        help="情绪选项 (默认: neutral)"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="列出所有可用音色"
    )
    parser.add_argument(
        "--test-all-voices",
        action="store_true",
        help="测试所有中文音色并生成对比报告"
    )
    parser.add_argument(
        "--output-dir",
        default="./voice_test",
        help="测试音频输出目录 (默认: ./voice_test)"
    )
    
    args = parser.parse_args()
    
    # 列出音色
    if args.list_voices:
        print_voice_list()
        return 0
    
    # 测试所有音色
    if args.test_all_voices:
        test_all_voices(args.output_dir)
        return 0
    
    # 验证text参数
    if not args.text:
        parser.error("请提供 --text 参数（或使用 --list-voices / --test-all-voices）")
    
    print("=" * 60)
    print("TextToSpeech — 文字转语音")
    print("Powered by MiniMax Speech-2.8-HD")
    print("=" * 60)
    print()
    
    # 获取音色配置
    voice_config = VOICE_CONFIGS[args.voice]
    
    try:
        result = text_to_speech(
            text=args.text,
            voice_id=voice_config.voice_id,
            output_path=args.output,
            speed=args.speed,
            emotion=args.emotion,
            verbose=True,
        )
        
        if not result.get("success"):
            raise Exception(result.get("error", "未知错误"))
        
        print("\n" + "=" * 60)
        print("生成结果")
        print("=" * 60)
        print(f"\n🎙️  音色: {voice_config.name} ({voice_config.description})")
        print(f"🔊 Voice ID: {voice_config.voice_id}")
        print(f"🔗 URL: {result['url']}")
        print(f"💾 本地: {result['local']}")
        print(f"⚡ 语速: {result['speed']}x")
        if result.get('emotion'):
            print(f"😊 情绪: {result['emotion']}")
        print(f"⏱️  耗时: {result['time']:.1f}s")
        if result.get('duration'):
            print(f"🎵 音频时长: {result['duration']:.1f}秒")
        
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
