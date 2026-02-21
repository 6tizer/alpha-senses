#!/usr/bin/env python3
"""Grok API 可用性测试脚本"""
import os
import fal_client
import time

FAL_KEY = "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
os.environ["FAL_KEY"] = FAL_KEY

test_prompt = "一只穿着宇航服的熊猫在月球上插旗，背景是地球，卡通风格"

print("=" * 60)
print("任务一：Grok 图像 API 调研")
print("=" * 60)

# 1. 测试 Grok 文生图
print("\n📋 测试 1: xai/grok-imagine-image (文生图)")
print("-" * 40)
try:
    start = time.time()
    result = fal_client.run(
        "xai/grok-imagine-image",
        arguments={
            "prompt": test_prompt,
            "image_size": "square_hd",
        },
    )
    elapsed = time.time() - start
    images = result.get("images", [])
    if images:
        print(f"✅ 状态: 可用")
        print(f"⏱️  耗时: {elapsed:.2f}秒")
        print(f"🔗 URL: {images[0]['url'][:60]}...")
        grok_available = True
    else:
        print(f"⚠️  返回异常: {result}")
        grok_available = False
except Exception as e:
    print(f"❌ 错误: {e}")
    grok_available = False

# 2. 测试 Grok 图生图 (需要一张测试图)
print("\n📋 测试 2: xai/grok-imagine-image/edit (图生图)")
print("-" * 40)
if grok_available:
    try:
        # 先用文生图生成一张测试图
        test_image_url = images[0]["url"]
        start = time.time()
        result = fal_client.run(
            "xai/grok-imagine-image/edit",
            arguments={
                "image_url": test_image_url,
                "prompt": "将背景变成火星红色沙漠",
            },
        )
        elapsed = time.time() - start
        edit_images = result.get("images", [])
        if edit_images:
            print(f"✅ 状态: 可用")
            print(f"⏱️  耗时: {elapsed:.2f}秒")
            print(f"🔗 URL: {edit_images[0]['url'][:60]}...")
            grok_edit_available = True
        else:
            print(f"⚠️  返回异常: {result}")
            grok_edit_available = False
    except Exception as e:
        print(f"❌ 错误: {e}")
        grok_edit_available = False
else:
    print("⏭️  跳过: 文生图不可用")
    grok_edit_available = False

# 3. 测试 Kling v3 作为对比
print("\n📋 测试 3: fal-ai/kling-image/v3 (对比基准)")
print("-" * 40)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/kling-image/v3/text-to-image",
        arguments={
            "prompt": test_prompt,
            "image_size": "square_hd",
        },
    )
    elapsed = time.time() - start
    kling_images = result.get("images", [])
    if kling_images:
        print(f"✅ 状态: 可用")
        print(f"⏱️  耗时: {elapsed:.2f}秒")
        print(f"🔗 URL: {kling_images[0]['url'][:60]}...")
        kling_available = True
    else:
        print(f"⚠️  返回异常: {result}")
        kling_available = False
except Exception as e:
    print(f"❌ 错误: {e}")
    kling_available = False

# 4. 测试 GLM 作为对比
print("\n📋 测试 4: fal-ai/glm-image (对比基准)")
print("-" * 40)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/glm-image",
        arguments={
            "prompt": test_prompt,
            "image_size": "square_hd",
        },
    )
    elapsed = time.time() - start
    glm_images = result.get("images", [])
    if glm_images:
        print(f"✅ 状态: 可用")
        print(f"⏱️  耗时: {elapsed:.2f}秒")
        print(f"🔗 URL: {glm_images[0]['url'][:60]}...")
        glm_available = True
    else:
        print(f"⚠️  返回异常: {result}")
        glm_available = False
except Exception as e:
    print(f"❌ 错误: {e}")
    glm_available = False

# 保存结果供后续使用
print("\n" + "=" * 60)
print("调研结果汇总")
print("=" * 60)
results = {
    "grok_text2img": grok_available,
    "grok_img2img": grok_edit_available,
    "kling_v3": kling_available,
    "glm": glm_available,
}
for name, status in results.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {name}: {'可用' if status else '不可用'}")

# 将结果写入文件供其他脚本使用
with open("/tmp/grok_test_results.txt", "w") as f:
    f.write(f"grok_available={grok_available}\n")
    f.write(f"grok_edit_available={grok_edit_available}\n")
    f.write(f"kling_available={kling_available}\n")
    f.write(f"glm_available={glm_available}\n")
    if grok_available:
        f.write(f"grok_sample_url={images[0]['url']}\n")
    if kling_available:
        f.write(f"kling_sample_url={kling_images[0]['url']}\n")
    if glm_available:
        f.write(f"glm_sample_url={glm_images[0]['url']}\n")

print("\n💾 结果已保存到 /tmp/grok_test_results.txt")
