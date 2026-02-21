# PRD：Alpha Senses Batch 3 + ClawHub 上线标准化

> 作者：Alphana（CEO）
> 时间：2026-02-21
> 状态：待 Tizer Green Light ✅

---

## 背景

目前已完成 6 个基础 Skills，本次开发剩余 5 个，凑齐完整的「感知 + 创造」能力矩阵共 11 个 Skills，同时对所有 Skills 进行 ClawHub 标准化，准备上线发布。

---

## Part 1：新增 5 个 Skills

---

### Skill 7：VideoAnalyzer（视频理解分析器）

**一句话定义**：输入视频文件或 URL → 输出视频内容的详细描述、关键帧分析、主题摘要

**模型**：Kimi 多模态（Moonshot API，`kimi-k2.5`）
- Base URL：`https://api.moonshot.cn/v1`
- API Key 从环境变量 `MOONSHOT_API_KEY` 读取

**功能**：
- 分析视频内容，输出文字描述
- 提取关键信息：场景、人物、动作、情绪
- 生成视频摘要（适合发推文/小红书）
- 支持中英文输出

**使用场景**：
- CT 用户上传一段市场分析视频 → 自动提炼核心观点 → 生成推文草稿
- Agent 监控 KOL 发布的视频 → 自动理解内容 → 判断是否值得转发
- 输入一段产品演示视频 → 自动生成文字说明

**参数**：
```
--video <路径或URL>     视频文件（必填）
--lang zh|en           输出语言（默认 zh）
--output <路径>         输出文件（默认 ./analysis.md）
--mode summary|detail  摘要模式或详细模式（默认 summary）
```

**文件路径**：`skills/video-analyzer/run.py`

---

### Skill 8：AudioAnalyzer（音频理解分析器）

**一句话定义**：输入音频文件 → 语音转文字 + 内容分析 + 情绪识别

**模型**：`fal-ai/personaplex`（实时语音理解）

**功能**：
- 语音转文字（STT）
- 说话人情绪识别（neutral/happy/serious/excited）
- 关键词提取
- 生成结构化摘要

**使用场景**：
- 输入播客音频 → 自动转录 + 提炼观点 → 生成推文
- Agent 听完语音消息 → 理解内容 → 自动回复
- 会议录音 → 自动生成会议纪要

**参数**：
```
--audio <路径或URL>     音频文件（必填，支持 mp3/wav/m4a）
--lang zh|en           语言（默认 zh）
--output <路径>         输出文件（默认 ./transcript.md）
--emotion              是否输出情绪分析（默认开启）
```

**文件路径**：`skills/audio-analyzer/run.py`

---

### Skill 9：AvatarGen（AI 角色形象生成器）

**一句话定义**：输入参考图片 + 动作视频 → 生成角色动态形象

**模型**：`fal-ai/bytedance/dreamactor/v2`（字节跳动 DreamActor v2）

**功能**：
- 将真实人物照片转换成动态 Avatar
- 支持动作迁移（从参考视频迁移动作到角色）
- 生成一致性强的 KOL 角色形象
- 适合 Agent 网红打造专属虚拟形象

**使用场景**：
- Agent KOL 生成专属虚拟形象，用于社交媒体头像
- 品牌方提供 Logo → 生成品牌虚拟代言人
- 创作者上传自拍 → 生成动漫/赛博朋克风格 Avatar

**参数**：
```
--image <路径或URL>     参考人物图片（必填）
--motion <路径或URL>    动作参考视频（可选）
--style realistic|anime|cyberpunk  风格（默认 realistic）
--output <路径>         输出文件（默认 ./avatar.mp4）
```

**文件路径**：`skills/avatar-gen/run.py`

---

### Skill 10：VoiceClone（声音克隆合成器）

**一句话定义**：上传 10 秒音频样本 → 克隆声音 → 用克隆声音合成任意文字

**模型**：`fal-ai/qwen-3-tts/clone-voice/1.7b`（阿里 Qwen3 TTS）

**功能**：
- 零样本声音克隆（只需 10 秒音频）
- 用克隆声音朗读任意文字
- 保留原声音的音色、语调、个人特色
- 支持中英文

**使用场景**：
- Agent KOL 克隆真实 KOL 的声音风格，生成语音内容
- 品牌方上传 CEO 声音样本 → 批量生成品牌语音播报
- 创作者克隆自己的声音 → 无需录音，直接文字转语音

**参数**：
```
--sample <路径>         声音样本音频（必填，10秒以上）
--text "要合成的内容"    合成文字（必填）
--output <路径>         输出文件（默认 ./cloned.mp3）
--lang zh|en           语言（默认 zh）
```

**文件路径**：`skills/voice-clone/run.py`

---

### Skill 11：VideoGen（AI 视频生成器）

**一句话定义**：输入文字描述或图片 → 生成高质量短视频

**模型**：`fal-ai/bytedance/seedance/v1/pro`（字节跳动 Seedance 1.0 Pro）+ 备选 `fal-ai/kling-video/v3/pro/text-to-video`（快手）

**功能**：
- 文字 → 视频（text-to-video）
- 图片 → 视频（image-to-video）
- 支持风格控制（写实/动漫/科技感）
- 生成 5-10 秒高质量短视频

**使用场景**：
- Agent 生成推文配套短视频，发布到抖音/TikTok
- 输入产品描述 → 自动生成产品宣传视频
- KOL Agent 根据热点新闻，自动生成评论视频

**参数**：
```
--prompt "视频描述"      文字描述（二选一）
--image <路径或URL>      参考图片（二选一）
--duration 5|10         视频时长（默认 5 秒）
--style realistic|anime|cinematic  风格（默认 realistic）
--output <路径>          输出文件（默认 ./output.mp4）
```

**文件路径**：`skills/video-gen/run.py`

---

## Part 2：11 个 Skills 组合使用场景

### 场景 A：CT KOL Agent 全自动内容发布

> "从热点新闻到推文配图+语音播报，全程不需要人工干预"

```
1. VisualAnalyzer     → 分析今日 CT 热点截图，提取核心信息
2. VideoAnalyzer      → 分析 KOL 发布的视频，理解观点
3. TweetImageGen      → 根据热点内容生成推文配图
4. TextToSpeech       → 把推文内容转成语音播报
5. VideoGen           → 生成 5 秒视频摘要（配套发抖音）
```

**效果**：Agent 每天自动产出：推文 + 配图 + 语音 + 短视频

---

### 场景 B：虚拟 KOL 打造

> "从零开始，打造一个有形象、有声音、有内容的 Agent 网红"

```
1. IdeaVisualizer     → 生成 KOL 角色概念图
2. AvatarGen          → 把概念图做成动态 Avatar
3. VoiceClone         → 克隆目标 KOL 的声音风格
4. TweetImageGen      → 生成每日推文配图
5. TextToSpeech       → 用克隆声音发布语音内容
6. VideoGen           → 生成每日短视频
```

**效果**：一个完整的虚拟 KOL，有脸、有声、有内容

---

### 场景 C：品牌内容工厂

> "品牌方提供素材，Agent 自动生产全平台内容"

```
1. VisualAnalyzer     → 分析品牌提供的产品图/海报
2. BackgroundRemover  → 产品图去背景，提取干净素材
3. ImageStyler        → 把产品图转成不同风格（科技/极简/国风）
4. TweetImageGen      → 生成平台适配的推文配图
5. AudioAnalyzer      → 分析品牌方提供的语音说明
6. VoiceClone         → 用品牌 CEO 声音克隆做语音播报
7. VideoGen           → 生成品牌宣传视频
```

**效果**：输入品牌素材 → 自动输出全平台适配内容

---

### 场景 D：内容二创流水线

> "把已有内容加工成新内容，最大化素材利用率"

```
1. VideoAnalyzer      → 理解原视频内容
2. AudioAnalyzer      → 提取原视频音频，转录文字
3. IdeaVisualizer     → 根据核心观点生成配图
4. ImageStyler        → 把截图转换成统一视觉风格
5. TextToSpeech       → 重新录制中文配音
6. VideoGen           → 生成二创视频
```

**效果**：英文视频 → 自动二创成中文内容，配图+配音全新

---

## Part 3：ClawHub 标准化要求

**所有 11 个 Skills 必须包含以下文件：**

```
skills/[skill-name]/
├── SKILL.md           ← 必须（ClawHub 识别入口）
├── run.py             ← 必须（主程序）
├── requirements.txt   ← 必须（依赖声明）
└── README.md          ← 建议（使用文档）
```

### SKILL.md 标准格式

```yaml
---
name: [skill-name]
description: [动词开头，一句话，说清用途和触发场景]
license: MIT
metadata:
  version: 1.0.0
  author: 6tizer
  category: [image-generation|video-generation|audio|image-analysis]
  updated: 2026-02-21
---

# [Skill Name]

[一句话说明]

## 安装
pip install -r requirements.txt

## 使用
[CLI 示例]

## 模型
[使用的模型和厂商]
```

### requirements.txt 标准格式

```
fal-client>=0.10.0
# 其他依赖按需添加
```

---

## 验收标准

**5 个新 Skills：**
- [ ] CLI `--help` 清晰，参数有默认值
- [ ] 成功输出 URL + 本地路径
- [ ] 失败有清晰错误提示
- [ ] 中文注释
- [ ] 实际 API 调用测试通过

**11 个 Skills 全部标准化：**
- [ ] 每个 Skill 有 SKILL.md（符合 ClawHub 格式）
- [ ] 每个 Skill 有 requirements.txt
- [ ] 版本号统一 v1.0.0
- [ ] 描述文案动词开头，一句话说清楚

**组合测试：**
- [ ] 场景 A 端到端跑通
- [ ] 场景 B 端到端跑通

---

## 预估工时

- 5 个新 Skills 开发：约 60-90 分钟
- 11 个 Skills 标准化（SKILL.md + requirements.txt）：约 30 分钟
- 组合测试：约 30 分钟

总计：约 2-2.5 小时

---

*PRD by Alphana | 待 Tizer Green Light 后派给 Cooclo 执行*
