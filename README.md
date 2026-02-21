# OpenClaw x fal.ai 增强计划

> 让 OpenClaw 获得多模态能力（图/音/视频/3D）

---

## 项目背景

**发起人**：Tizer（通过 Grok/Gemini 头脑风暴）  
**目标**：全球 OpenClaw 用户零成本入门，自带 Key 模式  
**核心理念**："看到" + "理解" + "画出来"

---

## 账户信息

- **平台**：fal.ai
- **账号**：6tizer@gmail.com
- **API Key**：已配置到系统环境变量
- **用途**：视觉分析、图像生成、背景移除

---

## MVP 进展（已完成）

### 决策过程
原始构想有 **21 个 Skills**，5 大维度。经过讨论，**语音/视频类优先级降低**，专注核心需求。

**MVP 三原则**：看到 + 理解 + 画出来

| 优先级 | Skill | 端点/模型 | 功能 | 状态 |
|--------|-------|-----------|------|------|
| 🥇 | **VisualAnalyzer** | `fal-ai/florence-2-large/detailed-caption` | 图像描述、内容理解 | ✅ 完成 |
| 🥈 | **IdeaVisualizer** | `fal-ai/flux-2` | 文字→图像生成 | ✅ 完成 |
| 🥉 | **BackgroundRemover** | `fal-ai/bria/background/remove` | 背景移除、透明 PNG | ✅ 完成 |

---

## Skills 详情

### 1. VisualAnalyzer（视觉分析）

**功能**：上传图片 → 获得详细描述和分析  
**适用场景**：
- 用户发送图片，AI 理解内容
- 产品图分析
- 视觉内容审查

**性能**：3-5 秒出结果  
**成本**： fal.ai 按调用计费

**示例输出**：
```
输入：一张熊猫图片
输出："一只可爱的熊猫坐在竹林中，黑白相间的毛发，正在吃竹子..."
```

---

### 2. IdeaVisualizer（想法可视化）

**功能**：文字描述 → 生成视觉参考图  
**适用场景**：
- 快速原型可视化
- 创意概念图
- 推文配图生成

**示例**：AlphaPanda 熊猫 Logo 生成

**集成到 AlphaPanda**：根据推文内容自动生成配图

---

### 3. BackgroundRemover（背景移除）

**功能**：上传图片 → 输出透明背景 PNG  
**适用场景**：
- 产品图处理
- 头像制作
- 素材准备

**输出格式**：PNG（透明通道）

---

## 原始构想（21 Skills）

### 五大维度

#### 1. 视觉感知维度
- VisualAnalyzer ✅
- ObjectRecognizer
- StyleAdapter
- ImageEditorPro

#### 2. 音频表达维度（暂缓）
- VoicePersona
- SoundScaper
- AudioEditor
- VoiceDialog

#### 3. 视频动态维度（暂缓）
- VideoStoryteller
- AvatarAnimator
- MotionTransformer
- VideoRemixer

#### 4. 多模态交互维度
- MultimodalChat
- 3DVisualizer
- 3DAnimator

#### 5. 创意自主维度
- IdeaVisualizer ✅
- PersonalCreator
- ContentFactory
- RealtimeCreator

#### 基础能力
- BackgroundRemover ✅
- ConcurrentGuard（并发管理）

---

## 技术架构

### 并发管理
- **限制**：2 个 concurrent tasks
- **队列**：40 个自动 queuing
- **模式**：per-user queuing

### Key 管理
- 用户自带 fal.ai Key
- OpenClaw 管理并发与 quota
- 可选 fallback 共享 Key

---

## 与 AlphaPanda 的集成

| AlphaPanda 功能 | fal.ai Skill | 用途 |
|----------------|--------------|------|
| 推文配图生成 | IdeaVisualizer | 根据内容生成图片 |
| 产品图处理 | BackgroundRemover | 快速处理素材 |
| 用户上传分析 | VisualAnalyzer | 理解图片内容 |

---

## 文件位置

```
projects/fal-skills/
├── README.md           # 本文件
├── BRIEF-v1.md        # 原始完整计划（来自 Grok/Gemini）
└── [skills]/          # Skill 实现代码
    ├── visual_analyzer/
    ├── idea_visualizer/
    └── background_remover/
```

---

## 后续规划

### 短期（MVP 扩展）
- [ ] ObjectRecognizer（物体识别）
- [ ] ImageEditorPro（图像编辑）

### 中期
- [ ] 语音类 Skills（如 VoicePersona）
- [ ] 3D 可视化 Skills

### 长期
- [ ] 视频生成 Skills
- [ ] 多模态融合

---

## 参考资源

- **fal.ai 文档**：https://fal.ai/docs
- **原始头脑风暴**：
  - Grok：https://grok.com/share/bGVnYWN5LWNvcHk_7231cc3b-6486-4d15-b2b0-ba1dcf553323
  - Gemini：https://g.co/gemini/share/8d23f48f7186

---

*最后更新：2026-02-20*
