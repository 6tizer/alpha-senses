# fal.ai Skills 技术设计文档 (TDD)

> **目标读者**：Tizer 及开发团队  
> **文档版本**：v1.0  
> **日期**：2026-02-20  
> **作者**：酷CO (CTO)

---

## 1. 项目概述

**fal.ai Skills** 是 OpenClaw 的多模态能力扩展模块，通过集成 fal.ai 的 AI 服务，让 AI 代理获得"看到"、"理解"、"画出来"的能力。

### MVP 已完成的 3 个 Skills

| Skill | 中文名 | 功能 | 状态 |
|-------|--------|------|------|
| VisualAnalyzer | 视觉分析器 | 图片 → 详细描述 | ✅ 完成 |
| IdeaVisualizer | 想法可视化 | 文字 → 图片生成 | ✅ 完成 |
| BackgroundRemover | 背景移除器 | 图片 → 透明 PNG | ✅ 完成 |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OpenClaw 主框架                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Skills 注册中心                                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │  Visual     │  │   Idea      │  │ Background  │  ...更多 Skills   │   │
│  │  │  Analyzer   │  │ Visualizer  │  │   Remover   │                  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                  │   │
│  └─────────┼────────────────┼────────────────┼─────────────────────────┘   │
└────────────┼────────────────┼────────────────┼─────────────────────────────┘
             │                │                │
             └────────────────┴────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         fal.ai 客户端层                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     ConcurrentGuard (并发守卫)                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  • 队列管理 (max 40 任务)                                    │   │   │
│  │  │  • 并发控制 (max 2 并发)                                     │   │   │
│  │  │  • 用户隔离 (per-user queuing)                               │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         fal.ai API 层                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  /florence-2     │  │   /flux-2        │  │  /bria/remove    │          │
│  │  (图像理解)       │  │  (图像生成)       │  │  (背景移除)       │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 架构说明（给 Tizer）

fal.ai Skills 像是一家**精品餐厅的外包厨房**：

| 层级 | 类比 | 作用 |
|------|------|------|
| OpenClaw | 主餐厅 | 接待顾客、安排订单 |
| Skills | 菜单上的菜品 | 每种 Skill 是一道菜 |
| ConcurrentGuard | 订单调度员 | 控制出餐速度，避免厨房过载 |
| fal.ai | 外包厨房 | 真正的烹饪大师 |

**为什么需要 ConcurrentGuard？**

fal.ai 有使用限制：
- 最多同时处理 2 个任务
- 超过的自动排队（最多 40 个）
- 如果不管理，用户会卡死或报错

ConcurrentGuard 就是**智能调度系统**，确保：
1. 不会给 fal.ai 太多任务
2. 每个用户公平排队
3. 任务完成及时回调

---

## 3. Skill 详细实现

### 3.1 VisualAnalyzer（视觉分析器）

#### 功能说明
上传任意图片，AI 自动分析并返回详细描述。

#### 技术规格

| 属性 | 值 |
|------|-----|
| fal.ai 端点 | `fal-ai/florence-2-large/detailed-caption` |
| 输入 | 图片 URL 或 Base64 |
| 输出 | 详细文字描述 + 可选标签 |
| 平均耗时 | 3-5 秒 |
| 成本 | ~$0.002/次 |

#### 输入参数
```typescript
interface VisualAnalyzerInput {
  // 图片源（二选一）
  image_url?: string;      // 公开可访问的图片 URL
  image_base64?: string;   // base64 编码的图片数据
  
  // 可选配置
  detail_level?: 'basic' | 'detailed' | 'expert';  // 描述详细程度
  output_language?: 'zh' | 'en' | 'auto';          // 输出语言
}
```

#### 输出结构
```typescript
interface VisualAnalyzerOutput {
  success: boolean;
  data: {
    description: string;       // 详细描述
    tags: string[];            // 标签列表
    objects: Array<{
      name: string;
      confidence: number;      // 0-1
      bbox?: [number, number, number, number];  // 边界框
    }>;
    style?: string;            // 艺术风格
    mood?: string;             // 情绪氛围
    colors?: string[];         // 主色调
  };
  metadata: {
    processing_time_ms: number;
    model_version: string;
    cost_usd: number;
  };
}
```

#### 示例输出
```json
{
  "success": true,
  "data": {
    "description": "一只成年大熊猫坐在竹林中，黑白相间的毛发清晰可见。它正用前爪抓着一根竹子，嘴里咀嚼着竹叶。",
    "tags": ["熊猫", "竹林", "野生动物", "中国"],
    "objects": [
      { "name": "大熊猫", "confidence": 0.99 },
      { "name": "竹子", "confidence": 0.95 }
    ],
    "style": "摄影/写实",
    "mood": "宁静、自然",
    "colors": ["黑白", "绿色", "棕色"]
  },
  "metadata": {
    "processing_time_ms": 4200,
    "model_version": "florence-2-large-1.0",
    "cost_usd": 0.002
  }
}
```

---

### 3.2 IdeaVisualizer（想法可视化）

#### 功能说明
将文字描述转换为视觉图片，让抽象想法具象化。

#### 技术规格

| 属性 | 值 |
|------|-----|
| fal.ai 端点 | `fal-ai/flux-2` |
| 输入 | 文字描述 + 风格参数 |
| 输出 | 生成图片 URL |
| 平均耗时 | 5-10 秒 |
| 成本 | ~$0.03-0.05/次 |

#### 输入参数
```typescript
interface IdeaVisualizerInput {
  prompt: string;            // 图片描述（支持中文）
  negative_prompt?: string;  // 不想出现的元素
  style?: 'auto' | 'photorealistic' | 'anime' | 'digital-art' | 'cinematic';
  aspect_ratio?: '1:1' | '16:9' | '9:16' | '4:3' | '3:4';
  seed?: number;             // 随机种子
}
```

#### Prompt 工程（关键）

用户输入："一只可爱的熊猫"  
AI 实际需要的是："A cute panda bear sitting in a bamboo forest, soft lighting, digital art style, highly detailed, 8k resolution"

**Prompt 优化流程**：
1. 语言检测 - 如果是中文，先翻译
2. 内容分析 - 提取主题、风格、场景、情绪
3. Prompt 构建 - 按模板组装
4. 质量增强 - 添加通用质量标签

**模板**：
```
{主题}, {场景}, {风格}, {光线}, {质量标签}
```

#### 示例调用
```typescript
const result = await ideaVisualizer.run({
  prompt: "一只穿着西装的熊猫在交易所看股票行情",
  style: 'digital-art',
  aspect_ratio: '16:9'
});

// 输出
{
  success: true,
  data: {
    image_url: "https://fal.media/files/.../panda-trader.png",
    width: 1024,
    height: 576,
    prompt_enhanced: "A panda wearing a business suit analyzing stock charts in a modern trading office, digital art style, neon lighting, highly detailed, 8k"
  },
  metadata: {
    processing_time_ms: 8543,
    cost_usd: 0.035
  }
}
```

---

### 3.3 BackgroundRemover（背景移除器）

#### 功能说明
自动识别图片主体，移除背景，输出透明背景 PNG。

#### 技术规格

| 属性 | 值 |
|------|-----|
| fal.ai 端点 | `fal-ai/bria/background/remove` |
| 输入 | 图片 URL 或 Base64 |
| 输出 | 透明背景 PNG |
| 平均耗时 | 3-5 秒 |
| 成本 | ~$0.01/次 |

---

## 4. fal.ai API 调用规范

### 4.1 认证方式

```typescript
// 环境变量方式
process.env.FAL_KEY = 'your-fal-api-key';
```

### 4.2 调用模式

| 方式 | 适用场景 | 特点 |
|------|----------|------|
| `fal.subscribe()` | 大多数情况 | 自动轮询直到完成 |
| `fal.queue()` | 高并发场景 | 手动控制，更灵活 |

### 4.3 常用端点

| 功能 | 端点 | 成本 | 耗时 |
|------|------|------|------|
| 图像生成 (Flux-2) | `fal-ai/flux-2` | ~$0.035 | 5-10s |
| 视觉分析 | `fal-ai/florence-2-large/detailed-caption` | ~$0.002 | 3-5s |
| 背景移除 | `fal-ai/bria/background/remove` | ~$0.01 | 3-5s |

---

## 5. 并发管理策略

### 5.1 fal.ai 限制

| 限制项 | 值 | 说明 |
|--------|-----|------|
| 最大并发 | 2 | 同时只能跑 2 个任务 |
| 队列长度 | 40 | 超过 40 个排队会报错 |
| 超时时间 | 5 分钟 | 单个任务最长执行时间 |

### 5.2 ConcurrentGuard 核心设计

```
用户请求 ──▶ [队列系统] ──▶ [调度器] ──▶ fal.ai
                 │              │
            用户隔离队列      全局并发槽 (max 2)
```

**关键机制**：
- **用户隔离**：每个用户有自己的队列（max 10 任务）
- **公平调度**：先进先出，防止某个用户独占资源
- **超时清理**：5 分钟自动取消卡住的任务
- **统计监控**：实时追踪队列状态

### 5.3 代码结构

```typescript
class ConcurrentGuard {
  maxGlobalConcurrent = 2;
  maxQueuePerUser = 10;
  maxGlobalQueue = 40;
  
  // 提交任务
  async submit(userId, skillName, input): Promise<result>
  
  // 处理队列
  private async processQueue()
  
  // 取消任务
  cancelTask(taskId, reason)
  
  // 获取统计
  getStats()
}
```

---

## 6. 错误处理机制

### 6.1 错误分类

| 类别 | 示例 | 处理策略 |
|------|------|----------|
| **用户错误** | 无效图片、参数错误 | 立即返回，提示修正 |
| **网络错误** | 超时、连接失败 | 自动重试 3 次 |
| **fal.ai 错误** | 队列满、内部错误 | 降级/排队，通知等待 |
| **系统错误** | 代码异常 | 记录日志，人工介入 |

### 6.2 重试策略

```typescript
const retryConfig = {
  maxAttempts: 3,
  backoffMs: 1000,      // 第一次等 1s
  maxBackoffMs: 10000,  // 最长等 10s
};

// 指数退避: 1s → 2s → 4s
```

### 6.3 降级策略

当 fal.ai 不可用时：

| Skill | 降级方案 |
|-------|----------|
| VisualAnalyzer | 返回简单描述 "图片上传成功" |
| IdeaVisualizer | 提示用户稍后重试，或提供素材库 |
| BackgroundRemover | 使用备用服务或提示手动处理 |

---

## 7. 与 AlphaPanda 集成

### 7.1 配图生成流程

```
用户选择趋势/输入内容
       │
       ▼
┌─────────────┐
│ 内容分析    │── 提取关键词、情绪、主题
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Prompt 构建 │── 生成 fal.ai 提示词
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Concurrent  │── 排队等待执行
│   Guard     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ fal.ai 生成 │── Flux-2 生成图片
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 上传 CDN    │── 存储到 Supabase
└──────┬──────┘
       │
       ▼
    返回给用户
```

### 7.2 调用示例

```typescript
// AlphaPanda 配图服务
async function generateTweetImage(content: string, persona: Persona) {
  // 1. 分析内容
  const keywords = extractKeywords(content);
  
  // 2. 构建 prompt
  const prompt = buildImagePrompt(keywords, persona.style);
  
  // 3. 调用 fal.ai Skill
  const result = await skills.ideaVisualizer.run({
    prompt,
    style: persona.imageStyle || 'digital-art',
    aspect_ratio: '16:9'
  });
  
  // 4. 存储结果
  await saveImageToDraft(draftId, result.data.image_url);
  
  return result;
}
```

---

## 附录

### A. 成本速查

| Skill | 单次成本 | 1000 次/月 |
|-------|----------|------------|
| VisualAnalyzer | $0.002 | $2 |
| IdeaVisualizer | $0.035 | $35 |
| BackgroundRemover | $0.01 | $10 |

### B. 响应时间速查

| Skill | 平均耗时 | P95 耗时 |
|-------|----------|----------|
| VisualAnalyzer | 3-5s | 8s |
| IdeaVisualizer | 5-10s | 15s |
| BackgroundRemover | 3-5s | 8s |

### C. 参考资料
- [fal.ai 文档](https://fal.ai/docs)
- [Flux-2 模型](https://fal.ai/models/fal-ai/flux-2)
- [Florence-2 模型](https://fal.ai/models/fal-ai/florence-2-large)

---

*文档结束*
