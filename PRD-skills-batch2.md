# PRD：fal.ai Skills 第二批（Batch 2）

> 作者：Alphana（CEO）  
> 时间：2026-02-21  
> 状态：待 Tizer Green Light

---

## 背景

第一批 3 个基础 Skills（VisualAnalyzer、IdeaVisualizer、BackgroundRemover）已全部验证完毕。

第二批聚焦 **AlphaPanda 内容生产闭环**，目标是让用户从"生成文字内容"直接延伸到"配图 + 配音"，形成完整的发布素材。

---

## Skill 1：TweetImageGen（推文配图生成器）

### 一句话定义
输入推文文字内容 → 自动生成匹配的配图

### 使用场景
AlphaPanda 用户在 Create 页面生成推文后，点击"生成配图"，自动产出一张风格匹配的图片用于发布。

### 输入
- `tweet`：推文正文（中/英文均支持）
- `style`：图片风格，可选值：
  - `crypto`（默认）：加密货币/科技感
  - `minimal`：极简白底
  - `news`：新闻感/信息图

### 输出
- 生成图片 URL
- 本地保存路径（可选）

### 技术实现
- **主模型**：`fal-ai/kling-image/v3/text-to-image`（快手）
- **对比测试**：`fal-ai/glm-image`（智谱）、`xai/grok-imagine-image`（Grok，待确认）
- **逻辑**：将 tweet 内容 + style 组合成优化 prompt，调用各模型生成并对比效果

### 文件路径
`projects/fal-skills/skills/tweet-image-gen/run.py`

---

## Skill 2：ImageStyler（图片风格转换器）

### 一句话定义
输入一张图片 → 转换成指定艺术风格

### 使用场景
- 把普通截图转成赛博朋克风格用于发布
- 把 KOL 头像转成统一视觉风格
- AlphaPanda 配图的二次加工

### 输入
- `image_path` 或 `image_url`：原始图片
- `style`：目标风格，可选值：
  - `cyberpunk`：赛博朋克，霓虹+暗调
  - `minimal`：极简，清爽白底
  - `anime`：动漫插画风
  - `cinematic`：电影感，高对比度
- `strength`：风格强度 0.1~1.0（默认 0.7）

### 输出
- 风格转换后的图片 URL
- 本地保存路径（可选）

### 技术实现
- **主模型**：`fal-ai/kling-image/v3/image-to-image`（快手）
- **对比测试**：`fal-ai/glm-image/image-to-image`（智谱）、Grok 图生图（待确认）
- **逻辑**：根据 style 参数生成对应的 prompt，结合原图调用图生图接口

### 文件路径
`projects/fal-skills/skills/image-styler/run.py`

---

## Skill 3：TextToSpeech（文字转语音）

### 一句话定义
输入文字 → 生成自然语音音频文件

### 使用场景
- AlphaPanda 内容转语音播报
- 推文/文章的有声版本
- 中英文均支持

### 输入
- `text`：要转换的文字内容
- `voice`：音色，可选值（MiniMax 内置音色）：
  - `female_zh`：中文女声（默认）
  - `male_zh`：中文男声
  - `female_en`：英文女声
  - `male_en`：英文男声
- `output`：输出文件路径（默认 `./output.mp3`）

### 输出
- 音频文件（mp3）
- 音频时长（秒）

### 技术实现
- **模型**：`fal-ai/minimax/speech-2.8-hd`
- **逻辑**：直接调用 MiniMax Speech 2.8 HD，中英文自动识别

### 文件路径
`projects/fal-skills/skills/text-to-speech/run.py`

---

## 附加任务：Grok 图像 API 调研 + 全量接入

### 背景
Grok（xAI）在 fal.ai 上已有图像端点，需确认可用性后统一接入。

### 调研内容
1. 确认 `xai/grok-imagine-image` 文生图、图生图端点是否可用
2. 如可用，在以下 **所有现有 Skills** 中补充 Grok 作为对比模型：
   - VisualAnalyzer（看 Grok 是否有图像理解能力）
   - IdeaVisualizer（文生图对比）
   - TweetImageGen（文生图对比）
   - ImageStyler（图生图对比）
3. 输出各模型对比报告（效果 + 速度 + 稳定性）

---

## 验收标准（3 个 Skills 通用）

- [ ] CLI 可直接运行（`python run.py --help` 有清晰说明）
- [ ] 支持必填参数校验，缺参数有友好提示
- [ ] 成功时输出 URL + 本地路径
- [ ] 失败时输出清晰错误信息
- [ ] 代码有中文注释

## 预估工时
- 每个 Skill：15-20 分钟
- 总计：约 1 小时

---

*PRD by Alphana | 待 Tizer Green Light 后派给 Cooclo 执行*
