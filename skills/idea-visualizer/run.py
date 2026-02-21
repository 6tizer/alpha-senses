#!/usr/bin/env python3
"""
IdeaVisualizer — 文字转图像 Skill
根据文字描述生成图像，支持多模型对比

用法:
    python run.py --idea "你的想法描述" [--output ./output.png] [--model kling]
    python run.py --idea "太空熊猫" --model grok
    python run.py --idea "赛博朋克城市" --compare

模型选项:
    kling - 快手 Kling v3 (默认，效果最佳)
    glm   - 智谱 GLM-Image
    grok  - xAI Grok (速度最快)
"""
import argparse
import os
import sys
import time
import urllib.request
from typing import Optional

import fal_client

FAL_KEY = os.environ.get(
    "FAL_API_KEY",
    "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
)

# 模型端点
MODELS = {
    "kling": "fal-ai/kling-image/v3/text-to-image",
    "glm": "fal-ai/glm-image",
    "grok": "xai/grok-imagine-image",
}


def visualize_with_model(
    model_key: str,
    idea: str,
    image_size: str = "square_hd"
) -> dict:
    """
    使用指定模型生成图像
    
    Args:
        model_key: 模型标识 (kling/glm/grok)
        idea: 图像描述
        image_size: 图像尺寸
        
    Returns:
        dict: 生成结果
    """
    os.environ["FAL_KEY"] = FAL_KEY
    
    model_id = MODELS[model_key]
    start = time.time()
    
    result = fal_client.run(
        model_id,
        arguments={
            "prompt": idea,
            "image_size": image_size,
        },
    )
    
    elapsed = time.time() - start
    images = result.get("images", [])
    
    if images:
        return {
            "url": images[0]["url"],
            "time": elapsed,
        }
    return {"error": "无图像返回", "raw": str(result)}


def visualize(
    idea: str,
    output_path: str = "./idea-output.png",
    model: str = "kling",
    compare: bool = False,
) -> dict:
    """
    将文字想法转换为图像
    
    Args:
        idea: 图像描述
        output_path: 输出文件路径
        model: 使用的模型 (kling/glm/grok)
        compare: 是否对比所有模型
        
    Returns:
        dict: 生成结果
    """
    # 验证模型参数
    if model not in MODELS:
        raise ValueError(f"不支持的模型: {model}。可选: {list(MODELS.keys())}")
    
    print(f"💡 想法描述: {idea}")
    print(f"🤖 使用模型: {model}")
    print()
    
    results = {}
    
    # 主模型生成
    print(f"🚀 使用 {model.upper()} 生成中...")
    try:
        result = visualize_with_model(model, idea)
        if "url" in result:
            urllib.request.urlretrieve(result["url"], output_path)
            results[model] = {
                "url": result["url"],
                "local": output_path,
                "time": result["time"],
            }
            print(f"   ✅ 成功 ({result['time']:.1f}s) → {output_path}")
        else:
            results[model] = result
            print(f"   ❌ 失败: {result.get('error')}")
    except Exception as e:
        results[model] = {"error": str(e)}
        print(f"   ❌ 失败: {e}")
    
    # 对比测试其他模型
    if compare:
        print("\n📊 对比测试其他模型...")
        for other_model in MODELS.keys():
            if other_model == model:
                continue
            
            print(f"🚀 使用 {other_model.upper()} 生成中...")
            try:
                result = visualize_with_model(other_model, idea)
                if "url" in result:
                    compare_path = output_path.replace(".png", f"-{other_model}.png")
                    urllib.request.urlretrieve(result["url"], compare_path)
                    results[other_model] = {
                        "url": result["url"],
                        "local": compare_path,
                        "time": result["time"],
                    }
                    print(f"   ✅ 成功 ({result['time']:.1f}s) → {compare_path}")
                else:
                    results[other_model] = result
            except Exception as e:
                results[other_model] = {"error": str(e)}
                print(f"   ❌ 失败: {e}")
    
    return results


def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(
        description="文字转图像生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py --idea "太空熊猫在月球"
  python run.py --idea "赛博朋克城市" --model grok
  python run.py --idea "未来汽车" --compare
        """
    )
    parser.add_argument(
        "--idea", "-i",
        required=True,
        help="用文字描述你想生成的图像（必填）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./idea-output.png",
        help="输出文件路径 (默认: ./idea-output.png)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["kling", "glm", "grok"],
        default="kling",
        help="使用的模型 (默认: kling)"
    )
    parser.add_argument(
        "--compare", "-c",
        action="store_true",
        help="对比测试所有模型"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("IdeaVisualizer — 文字转图像")
    print("=" * 60)
    print()
    
    try:
        results = visualize(
            idea=args.idea,
            output_path=args.output,
            model=args.model,
            compare=args.compare,
        )
        
        print("\n" + "=" * 60)
        print("生成结果")
        print("=" * 60)
        
        for model_name, result in results.items():
            if "url" in result:
                print(f"\n📷 {model_name.upper()}:")
                print(f"   URL: {result['url']}")
                print(f"   本地: {result['local']}")
                print(f"   耗时: {result['time']:.1f}s")
            else:
                print(f"\n❌ {model_name.upper()}: {result.get('error', '未知错误')}")
        
        return 0
        
    except ValueError as e:
        print(f"\n❌ 参数错误: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
