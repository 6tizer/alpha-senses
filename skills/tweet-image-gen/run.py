#!/usr/bin/env python3
"""
TweetImageGen — 推文配图生成器
根据推文内容和风格自动生成配图

用法:
    # 单推文模式（默认）
    python run.py --tweet "推文内容" --style crypto --output ./output.png
    python run.py --tweet "比特币突破10万美元！" --style crypto
    
    # Thread/文章多图模式
    python run.py --mode thread --tweet "段落1\n\n段落2\n\n段落3" --style crypto
    
    # 从文件读取长文本
    python run.py --mode thread --tweet-file ./article.txt --style news

风格选项:
    crypto   - 加密货币/科技感 (默认)
    minimal  - 极简白底风格
    news     - 新闻感/信息图风格
"""
import argparse
import os
import re
import sys
import time
import urllib.request
from typing import Optional, List

import fal_client
from openai import OpenAI

# FAL API Key
FAL_KEY = os.environ.get(
    "FAL_API_KEY",
    "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
)

# Moonshot API配置
MOONSHOT_API_KEY = os.environ.get(
    "MOONSHOT_API_KEY",
    "sk-EZhdBSl7i7qn4N3DZFlMbqAGSblpJKX6gxCaUjYSxqVBVRPAImM7"
)
MOONSHOT_BASE_URL = "https://api.moonshot.cn/v1"
MOONSHOT_MODEL = "moonshot-v1-8k"

# 模型端点
MODELS = {
    "kling": "fal-ai/kling-image/v3/text-to-image",
    "glm": "fal-ai/glm-image",
    "grok": "xai/grok-imagine-image",
}

# 风格预设 - 针对不同风格优化的基础描述
STYLE_BASE = {
    "crypto": (
        "futuristic, neon accents, dark background with electric blue and purple gradients, "
        "blockchain aesthetic, high-tech visualization, professional social media graphic, 4K quality"
    ),
    "minimal": (
        "pure white background, simple geometric shapes, elegant typography space, "
        "subtle shadows, Scandinavian design aesthetic, plenty of white space, modern and professional"
    ),
    "news": (
        "editorial layout, bold headlines space, information graphic aesthetic, "
        "professional news media style, blue and white color scheme, trustworthy and authoritative look"
    ),
}


def get_moonshot_client() -> OpenAI:
    """创建Moonshot客户端"""
    return OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url=MOONSHOT_BASE_URL,
    )


def refine_prompt_with_llm(raw_content: str, style: str = "crypto") -> str:
    """
    使用Moonshot LLM将原始推文/段落内容提炼成适合图像生成的英文prompt
    
    Args:
        raw_content: 原始文本内容
        style: 图片风格
        
    Returns:
        str: 提炼后的英文image prompt
    """
    client = get_moonshot_client()
    
    # 获取风格描述
    style_desc = STYLE_BASE.get(style, STYLE_BASE["crypto"])
    
    # 构建LLM prompt
    system_prompt = """You are an expert at converting text content into high-quality image generation prompts.
Your task is to transform the given content into 1-2 sentences of English description that:
1. Captures the key visual elements and mood of the content
2. Is optimized for AI image generation models
3. Focuses on visual composition, lighting, and atmosphere
4. Avoids text-heavy or typography-focused descriptions (as AI struggles with text)

Output ONLY the image prompt, nothing else."""
    
    user_prompt = f"""Convert the following content into an image generation prompt:

Content: {raw_content!r}

Style reference: {style_desc}

Generate a concise English image prompt:"""
    
    try:
        response = client.chat.completions.create(
            model=MOONSHOT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        
        refined = response.choices[0].message.content.strip()
        # 移除可能的引号
        refined = refined.strip('"\'')
        return refined
    except Exception as e:
        print(f"   ⚠️ LLM提炼失败，使用原始内容: {e}")
        # Fallback：直接使用原始内容
        return f"Illustration of: {raw_content[:200]}"


def split_content_into_segments(content: str) -> List[str]:
    """
    将长文本拆分为多个段落/片段
    
    支持的分隔符：
    - 双换行（段落）
    - 单换行（短段落）
    - 中文句号+换行
    
    Args:
        content: 原始文本内容
        
    Returns:
        List[str]: 文本片段列表
    """
    # 首先尝试双换行分隔（段落）
    segments = [s.strip() for s in content.split('\n\n') if s.strip()]
    
    # 如果段落太少，尝试单换行
    if len(segments) < 2:
        segments = [s.strip() for s in content.split('\n') if s.strip()]
    
    # 过滤掉太短的片段（少于10个字符）
    segments = [s for s in segments if len(s) >= 10]
    
    return segments


def generate_with_model(
    model_id: str,
    prompt: str,
    image_size: str = "square_hd"
) -> dict:
    """
    使用指定模型生成图像
    
    Args:
        model_id: 模型端点ID
        prompt: 图像生成提示词
        image_size: 图像尺寸
        
    Returns:
        dict: 包含 images 的响应数据
    """
    os.environ["FAL_KEY"] = FAL_KEY
    
    result = fal_client.run(
        model_id,
        arguments={
            "prompt": prompt,
            "image_size": image_size,
        },
    )
    return result


def generate_single_image(
    prompt: str,
    output_path: str,
) -> dict:
    """
    生成单张图片
    
    Args:
        prompt: 图像生成提示词
        output_path: 输出文件路径
        
    Returns:
        dict: 生成结果
    """
    print(f"🚀 使用 Kling v3 生成中...")
    print(f"   📝 Prompt: {prompt[:100]}...")
    
    try:
        start = time.time()
        result = generate_with_model(MODELS["kling"], prompt)
        elapsed = time.time() - start
        
        images = result.get("images", [])
        if images:
            url = images[0]["url"]
            urllib.request.urlretrieve(url, output_path)
            return {
                "url": url,
                "local": output_path,
                "time": elapsed,
                "success": True,
            }
        else:
            return {"error": "无图像返回", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


def generate_tweet_images_single(
    tweet: str,
    style: str = "crypto",
    output_path: str = "./output.png",
    use_llm: bool = True,
) -> dict:
    """
    单推文模式：为单条推文生成一张配图
    
    Args:
        tweet: 推文内容
        style: 图片风格
        output_path: 输出文件路径
        use_llm: 是否使用LLM提炼prompt
        
    Returns:
        dict: 生成结果
    """
    print(f"📝 推文内容: {tweet[:50]}{'...' if len(tweet) > 50 else ''}")
    print(f"🎨 风格: {style}")
    print()
    
    # 使用LLM提炼prompt
    if use_llm:
        print("🤖 使用Moonshot LLM提炼Image Prompt...")
        refined_prompt = refine_prompt_with_llm(tweet, style)
        print(f"   ✅ 提炼完成: {refined_prompt[:80]}...")
        print()
        
        # 组合最终prompt（风格+提炼内容）
        final_prompt = f"{refined_prompt}, {STYLE_BASE[style]}"
    else:
        final_prompt = f"Create an image for social media: {tweet}, {STYLE_BASE[style]}"
    
    result = generate_single_image(final_prompt, output_path)
    
    if result.get("success"):
        print(f"   ✅ 成功 ({result['time']:.1f}s) → {output_path}")
        return {
            "url": result["url"],
            "local": output_path,
            "time": result["time"],
            "prompt": final_prompt,
        }
    else:
        print(f"   ❌ 失败: {result.get('error', '未知错误')}")
        raise Exception(result.get("error", "生成失败"))


def generate_tweet_images_thread(
    content: str,
    style: str = "crypto",
    output_prefix: str = "./output",
) -> List[dict]:
    """
    Thread模式：为多段落内容生成多张配图
    
    Args:
        content: 完整文章内容
        style: 图片风格
        output_prefix: 输出文件路径前缀
        
    Returns:
        List[dict]: 每张图的生成结果
    """
    # 拆分段落
    segments = split_content_into_segments(content)
    
    if not segments:
        raise ValueError("未能从内容中提取有效段落")
    
    print(f"📄 共识别 {len(segments)} 个段落")
    print()
    
    results = []
    
    for i, segment in enumerate(segments, 1):
        print(f"\n{'='*60}")
        print(f"📌 段落 {i}/{len(segments)}")
        print(f"{'='*60}")
        print(f"📝 内容: {segment[:60]}{'...' if len(segment) > 60 else ''}")
        print()
        
        # 使用LLM提炼prompt
        print("🤖 使用Moonshot LLM提炼Image Prompt...")
        refined_prompt = refine_prompt_with_llm(segment, style)
        print(f"   ✅ 提炼完成: {refined_prompt[:80]}...")
        print()
        
        # 组合最终prompt
        final_prompt = f"{refined_prompt}, {STYLE_BASE[style]}"
        
        # 生成输出路径
        if output_prefix.endswith('.png'):
            output_path = output_prefix.replace('.png', f'-{i}.png')
        else:
            output_path = f"{output_prefix}-{i}.png"
        
        # 生成图片
        result = generate_single_image(final_prompt, output_path)
        
        if result.get("success"):
            print(f"   ✅ 成功 ({result['time']:.1f}s) → {output_path}")
            results.append({
                "segment_index": i,
                "segment_text": segment[:100],
                "prompt": refined_prompt,
                "url": result["url"],
                "local": output_path,
                "time": result["time"],
                "success": True,
            })
        else:
            print(f"   ❌ 失败: {result.get('error', '未知错误')}")
            results.append({
                "segment_index": i,
                "segment_text": segment[:100],
                "error": result.get('error', '未知错误'),
                "success": False,
            })
    
    return results


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="为推文生成配图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单推文模式（默认）
  python run.py --tweet "比特币新高！🚀" --style crypto
  python run.py --tweet "产品发布" --style minimal --output ./product.png
  
  # Thread/文章多图模式
  python run.py --mode thread --tweet "第一段内容\n\n第二段内容\n\n第三段内容"
  python run.py --mode thread --tweet-file ./article.txt --style news --output ./article.png
  
  # 跳过LLM提炼（使用原始内容生成）
  python run.py --tweet "简单测试" --no-llm
        """
    )
    parser.add_argument(
        "--tweet", "--content", "-t",
        dest="tweet",
        help="推文/文章内容 (--content 为 --tweet 的别名)"
    )
    parser.add_argument(
        "--tweet-file", "-f",
        help="从文件读取推文内容"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["single", "thread"],
        default="single",
        help="生成模式: single(单图) 或 thread(多图)，默认: single"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["crypto", "minimal", "news"],
        default="crypto",
        help="图片风格 (默认: crypto)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output.png",
        help="输出文件路径 (默认: ./output.png，thread模式下自动添加序号)"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="不使用LLM提炼prompt（直接生成）"
    )
    
    args = parser.parse_args()
    
    # 验证输入
    if not args.tweet and not args.tweet_file:
        parser.error("请提供 --tweet 或 --tweet-file 参数")
    
    # 读取内容
    if args.tweet_file:
        with open(args.tweet_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.tweet
    
    print("=" * 60)
    print("TweetImageGen — 推文配图生成器")
    print(f"模式: {args.mode} | 风格: {args.style}")
    print("=" * 60)
    print()
    
    try:
        if args.mode == "single":
            # 单图模式
            result = generate_tweet_images_single(
                tweet=content,
                style=args.style,
                output_path=args.output,
                use_llm=not args.no_llm,
            )
            
            print("\n" + "=" * 60)
            print("生成结果")
            print("=" * 60)
            print(f"\n📷 图片URL: {result['url']}")
            print(f"💾 本地路径: {result['local']}")
            print(f"⏱️  耗时: {result['time']:.1f}s")
            print(f"📝 使用Prompt: {result['prompt'][:100]}...")
            
        else:
            # Thread多图模式
            results = generate_tweet_images_thread(
                content=content,
                style=args.style,
                output_prefix=args.output,
            )
            
            print("\n" + "=" * 60)
            print("生成结果汇总")
            print("=" * 60)
            
            success_count = sum(1 for r in results if r.get("success"))
            print(f"\n✅ 成功: {success_count}/{len(results)}")
            
            for r in results:
                if r.get("success"):
                    print(f"\n📷 段落 {r['segment_index']}:")
                    print(f"   内容: {r['segment_text'][:50]}...")
                    print(f"   URL: {r['url']}")
                    print(f"   本地: {r['local']}")
                    print(f"   耗时: {r['time']:.1f}s")
                else:
                    print(f"\n❌ 段落 {r['segment_index']}: {r.get('error', '失败')}")
        
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
