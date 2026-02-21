# fal.ai 中国大陆厂商模型调研报告

> 调研时间：2026-02-21  
> 调研方法：通过 fal.ai API 直接查询

---

## 已确认可用的中国大陆厂商模型

### 1. 快手 (Kuaishou) - Kling 系列 ⭐⭐⭐⭐⭐

| 端点 | 名称 | 分类 | 特点 |
|------|------|------|------|
| `fal-ai/kling-video/v3/pro/text-to-video` | Kling Video v3 Text to Video [Pro] | 文生视频 | 顶级质量，电影级视觉效果 |
| `fal-ai/kling-video/v3/pro/image-to-video` | Kling Video v3 Image to Video [Pro] | 图生视频 | 原生音频生成，自定义元素 |
| `fal-ai/kling-video/o3/pro/text-to-video` | Kling O3 Text to Video [Pro] | 文生视频 | 最新 O3 系列，真实感强 |
| `fal-ai/kling-video/o3/pro/image-to-video` | Kling O3 Image to Video [Pro] | 图生视频 | 首尾帧动画，参考视频生成 |
| `fal-ai/kling-video/v2.5-turbo/pro/text-to-video` | Kling v2.5 Text to Video | 文生视频 | 高性能，流畅运动 |
| `fal-ai/kling-video/v2.5-turbo/pro/image-to-video` | Kling Video | 图生视频 | 2.5 Turbo Pro |
| `fal-ai/kling-video/v2.1/master/image-to-video` | Kling 2.1 Master | 图生视频 | 2.1 大师版 |
| `fal-ai/kling-video/v1.6/pro/image-to-video` | Kling 1.6 | 图生视频 | 经典稳定版 |
| `fal-ai/kling-image/v3/text-to-image` | Kling Image | 文生图 | Kling V3 图像模型 |
| `fal-ai/kling-image/o3/text-to-image` | Kling Image | 文生图 | Kling Omni 3，一致性极佳 |

**适用场景**：视频生成、图像生成  
**优势**：质量高、更新快、支持中文提示词  
**建议**：作为视频生成首选

---

### 2. MiniMax (稀宇科技) - Hailuo AI 系列 ⭐⭐⭐⭐

| 端点 | 名称 | 分类 | 特点 |
|------|------|------|------|
| `fal-ai/minimax/hailuo-2.3/pro/image-to-video` | MiniMax Hailuo 2.3 [Pro] | 图生视频 | 1080p，高级图生视频 |
| `fal-ai/minimax/hailuo-02/standard/image-to-video` | MiniMax Hailuo 02 [Standard] | 图生视频 | 768p/512p 标准版 |
| `fal-ai/minimax/hailuo-02/standard/text-to-video` | MiniMax Hailuo 02 [Standard] | 文生视频 | 768p 文生视频 |
| `fal-ai/minimax/video-01/image-to-video` | MiniMax (Hailuo AI) Video 01 | 图生视频 | 早期版本 |
| `fal-ai/minimax/speech-2.8-hd` | MiniMax Speech 2.8 [HD] | 文本转语音 | 高清语音合成 |
| `fal-ai/minimax/speech-2.8-turbo` | MiniMax Speech 2.8 [Turbo] | 文本转语音 | 极速语音合成 |

**适用场景**：视频生成、语音合成  
**优势**：语音质量高（海螺语音），视频效果自然  
**建议**：TTS 首选 MiniMax

---

### 3. 阿里 (Alibaba) - Wan 系列 ⭐⭐⭐⭐

| 端点 | 名称 | 分类 | 特点 |
|------|------|------|------|
| `fal-ai/wan-pro/image-to-video` | Wan-2.1 Pro Image-to-Video | 图生视频 | 1080p 高质量 |
| `fal-ai/wan-i2v` | Wan-2.1 Image-to-Video | 图生视频 | 标准版 |
| `fal-ai/wan-effects` | Wan Effects | 图生视频 | 流行特效 |
| `fal-ai/wan-25-preview/image-to-video` | Wan 2.5 Image to Video | 图生视频 | 2.5 预览版 |
| `wan/v2.6/reference-to-video/flash` | V2.6 | 视频到视频 | Wan 2.6 参考生成 |

**适用场景**：视频生成  
**优势**：阿里出品，中文理解好，运动流畅  
**建议**：作为 Kling 的备选

---

### 4. 腾讯 (Tencent) - Hunyuan 系列 ⭐⭐⭐

| 端点 | 名称 | 分类 | 特点 |
|------|------|------|------|
| `fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d` | Hunyuan 3d | 文生3D | 快速生成 3D 模型 |

**适用场景**：3D 模型生成  
**优势**：腾讯混元大模型，3D 生成能力强  
**建议**：3D 内容生成使用

---

### 5. 其他中国厂商模型

| 端点 | 名称 | 厂商 | 分类 | 特点 |
|------|------|------|------|------|
| `fal-ai/qwen-image-trainer-v2` | Qwen Image Trainer V2 | 阿里 | 训练 | Qwen 图像 LoRA 训练 |
| `fal-ai/hidream-i1-fast` | Hidream I1 Fast | HiDream | 文生图 | 17B 参数开源模型 |
| `fal-ai/firered-image-edit` | Firered Image Edit | FireRed | 图像编辑 | 开源编辑模型 |

---

## 按场景推荐

### 🎬 视频生成（文生视频/图生视频）

| 优先级 | 模型 | 厂商 | 推荐理由 |
|--------|------|------|----------|
| 🥇 | Kling v3 / O3 Pro | 快手 | 质量最高，更新最快 |
| 🥈 | Wan-2.1 Pro | 阿里 | 中文理解好，运动流畅 |
| 🥉 | MiniMax Hailuo 2.3 | MiniMax | 效果自然，成本低 |

### 🎙️ 语音合成（TTS）

| 优先级 | 模型 | 厂商 | 推荐理由 |
|--------|------|------|----------|
| 🥇 | MiniMax Speech 2.8 HD | MiniMax | 中文语音质量顶级 |
| 🥈 | MiniMax Speech 2.8 Turbo | MiniMax | 速度快，成本低 |

### 🖼️ 图像生成

| 优先级 | 模型 | 厂商 | 推荐理由 |
|--------|------|------|----------|
| 🥇 | Kling Image v3 / O3 | 快手 | 一致性好，质量高 |
| 🥈 | HiDream I1 Fast | HiDream | 17B 参数，开源 |

### 🎨 图像编辑

| 优先级 | 模型 | 厂商 | 推荐理由 |
|--------|------|------|----------|
| 🥇 | Firered Image Edit | FireRed | 开源，编辑能力强 |

### 🧊 3D 生成

| 优先级 | 模型 | 厂商 | 推荐理由 |
|--------|------|------|----------|
| 🥇 | Hunyuan 3D | 腾讯 | 混元大模型，3D 效果好 |

---

## 与现有 Skills 的对比

| Skill | 当前模型 | 建议替换为中国厂商 |
|-------|----------|-------------------|
| VisualAnalyzer | `fal-ai/florence-2-large/detailed-caption` (微软) | 保持或换 `qwen-vl` (如有) |
| IdeaVisualizer | `fal-ai/flux-2` (Black Forest) | 可尝试 `kling-image` |
| BackgroundRemover | `fal-ai/bria/background/remove` (Bria) | 保持 |

**结论**：
- 视频/语音类：强烈建议用中国厂商（Kling、MiniMax、Wan）
- 图像分析类：Florence-2 效果已很好，中文场景可找替代
- 文生图：Flux-2 仍是首选，Kling Image 可作备选

---

## 下一步建议

1. **立即测试**：Kling v3 视频生成效果
2. **语音合成**：将 MiniMax Speech 加入技能矩阵
3. **持续关注**：Qwen-VL（阿里多模态）上线 fal.ai
4. **成本对比**：记录各模型 token 消耗和成本

---

*报告生成：Alphana*  
*数据来源：fal.ai API (v1/models)*
