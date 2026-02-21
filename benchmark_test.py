#!/usr/bin/env python3
"""
模型对比测试脚本 - 快速收集各模型性能数据
"""
import os
import time
import fal_client

FAL_KEY = "6bfc9d8b-b64d-43a4-957b-4f662fc599cb:3359f4952ea2579f32fcf6c953072c8e"
os.environ["FAL_KEY"] = FAL_KEY

TEST_PROMPT = "a cute robot reading a newspaper, cartoon style"
TEST_IMAGE_URL = "https://images.unsplash.com/photo-1535378620166-273708d44e4c?w=512&h=512&fit=crop"

print("=" * 70)
print("🧪 fal.ai 模型对比测试")
print("=" * 70)

results = []

# 1. Grok 文生图
print("\n1️⃣ 测试 Grok 文生图 (xai/grok-imagine-image)")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "xai/grok-imagine-image",
        arguments={"prompt": TEST_PROMPT, "image_size": "square_hd"}
    )
    elapsed = time.time() - start
    if result.get("images"):
        grok_url = result["images"][0]["url"]
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s")
        print(f"   🌐 URL: {grok_url[:50]}...")
        results.append({"model": "Grok", "type": "文生图", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无图像返回")
        results.append({"model": "Grok", "type": "文生图", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "Grok", "type": "文生图", "time": 0, "status": "❌"})

# 2. Grok 图生图
print("\n2️⃣ 测试 Grok 图生图 (xai/grok-imagine-image/edit)")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "xai/grok-imagine-image/edit",
        arguments={
            "image_url": TEST_IMAGE_URL,
            "prompt": "transform to cyberpunk style with neon lights"
        }
    )
    elapsed = time.time() - start
    if result.get("images"):
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s")
        results.append({"model": "Grok", "type": "图生图", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无图像返回")
        results.append({"model": "Grok", "type": "图生图", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "Grok", "type": "图生图", "time": 0, "status": "❌"})

# 3. Kling v3 文生图
print("\n3️⃣ 测试 Kling v3 文生图 (fal-ai/kling-image/v3)")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/kling-image/v3/text-to-image",
        arguments={"prompt": TEST_PROMPT, "image_size": "square_hd"}
    )
    elapsed = time.time() - start
    if result.get("images"):
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s")
        results.append({"model": "Kling v3", "type": "文生图", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无图像返回")
        results.append({"model": "Kling v3", "type": "文生图", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "Kling v3", "type": "文生图", "time": 0, "status": "❌"})

# 4. Kling v3 图生图
print("\n4️⃣ 测试 Kling v3 图生图")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/kling-image/v3/image-to-image",
        arguments={
            "image_url": TEST_IMAGE_URL,
            "prompt": "transform to cyberpunk style",
            "strength": 0.7
        }
    )
    elapsed = time.time() - start
    if result.get("images"):
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s")
        results.append({"model": "Kling v3", "type": "图生图", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无图像返回")
        results.append({"model": "Kling v3", "type": "图生图", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "Kling v3", "type": "图生图", "time": 0, "status": "❌"})

# 5. GLM 文生图
print("\n5️⃣ 测试 GLM 文生图 (fal-ai/glm-image)")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/glm-image",
        arguments={"prompt": TEST_PROMPT, "image_size": "square_hd"}
    )
    elapsed = time.time() - start
    if result.get("images"):
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s")
        results.append({"model": "GLM", "type": "文生图", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无图像返回")
        results.append({"model": "GLM", "type": "文生图", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "GLM", "type": "文生图", "time": 0, "status": "❌"})

# 6. MiniMax TTS
print("\n6️⃣ 测试 MiniMax TTS (fal-ai/minimax/speech-2.8-hd)")
print("-" * 50)
try:
    start = time.time()
    result = fal_client.run(
        "fal-ai/minimax/speech-2.8-hd",
        arguments={
            "prompt": "Hello, this is a test for AlphaPanda content generation",
            "voice_id": "female-english"
        }
    )
    elapsed = time.time() - start
    if result.get("audio"):
        duration_ms = result.get("duration_ms", 0)
        print(f"   ✅ 成功 - 耗时: {elapsed:.1f}s, 音频时长: {duration_ms/1000:.1f}s")
        results.append({"model": "MiniMax", "type": "TTS", "time": elapsed, "status": "✅"})
    else:
        print(f"   ❌ 失败: 无音频返回")
        results.append({"model": "MiniMax", "type": "TTS", "time": 0, "status": "❌"})
except Exception as e:
    print(f"   ❌ 失败: {e}")
    results.append({"model": "MiniMax", "type": "TTS", "time": 0, "status": "❌"})

# 输出汇总
print("\n" + "=" * 70)
print("📊 测试结果汇总")
print("=" * 70)
print(f"{'模型':<12} {'类型':<10} {'状态':<6} {'耗时':<10}")
print("-" * 40)
for r in results:
    time_str = f"{r['time']:.1f}s" if r['time'] > 0 else "N/A"
    print(f"{r['model']:<12} {r['type']:<10} {r['status']:<6} {time_str:<10}")

print("\n✅ 所有API测试完成!")
