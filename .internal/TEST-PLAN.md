# alpha-senses v1.0 测试手册

> **执行者**：Kimi（按本手册逐步执行，汇报每项结果）
> **监督**：Tizer
> **日期**：2026-02-21
> **Skills 路径**：`~/.openclaw/workspace/projects/alpha-senses/skills/`

---

## 测试素材准备

执行任何测试前，先确认以下素材存在（如不存在，自行从网上找公开 URL 替代）：

| 素材 | 说明 | 建议来源 |
|------|------|---------|
| 图片 | 任意清晰人物或场景图 | 用 `https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800` |
| 音频 | 10 秒以上中文语音 | 先用 TextToSpeech 生成一段，保存为 `test.mp3` |
| 视频 | 短视频 URL | 用 `https://www.w3schools.com/html/mov_bbb.mp4` |

---

## 单项测试（11 个 Skills）

---

### T01：VisualAnalyzer — 图像分析

**目的**：验证图片分析功能正常

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/visual-analyzer
python run.py --image "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"
```

**期望**：
- 输出一段图片的详细中文描述
- 包含场景、颜色、情绪等信息

**通过标准**：输出文字描述，无报错

---

### T02：IdeaVisualizer — 想法生图

**目的**：验证文字生成图片功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/idea-visualizer
python run.py --idea "一只戴着宇航员头盔的熊猫，站在月球上，地球在背景中，科幻风格"
```

**期望**：
- 输出生成图片的 URL
- 图片已下载保存到本地

**通过标准**：本地有图片文件，可以打开查看

---

### T03：ImageStyler — 图像风格化

**目的**：验证图生图功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/image-styler
python run.py \
  --image "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800" \
  --style "赛博朋克风格，霓虹灯，暗黑系"
```

**期望**：
- 输出风格化后的图片 URL 及本地路径
- 图片风格明显不同于原图

**通过标准**：本地有风格化图片，可以打开查看

---

### T04：TweetImageGen — 推文配图

**目的**：验证根据推文内容生成配图

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/tweet-image-gen
python run.py --content "Bitcoin 突破历史新高！牛市来了，所有 altcoin 都在疯涨。是入场的时候了吗？🚀 #BTC #Crypto"
```

**期望**：
- 自动提取推文主题（加密货币/牛市）
- 生成匹配的配图
- 输出图片 URL 和本地路径

**通过标准**：本地有配图，图片主题与推文相关

---

### T05：BackgroundRemover — 背景去除

**目的**：验证背景移除功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/bg-remover
python run.py --image "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=800"
```

**期望**：
- 输出去背景后的图片（透明 PNG）
- 人物主体清晰保留

**通过标准**：本地有透明背景的 PNG 文件

---

### T06：TextToSpeech — 文字转语音

**目的**：验证语音合成功能，同时生成后续测试用的音频素材

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech
python run.py \
  --text "比特币今日突破历史新高，市场情绪极度乐观。分析师认为，本轮牛市将持续至2026年底。" \
  --voice "sweet_lady" \
  --output ./test-audio.mp3
```

**期望**：
- 生成自然流畅的中文语音
- 保存为 `test-audio.mp3`

**通过标准**：本地有 mp3 文件，可以播放

> ⚠️ 保存好 `test-audio.mp3` 路径，T08（AudioAnalyzer）和 T10（VoiceClone）需要用到

---

### T07：VideoAnalyzer — 视频分析

**目的**：验证 Kimi 多模态视频理解功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/video-analyzer
python run.py \
  --video "https://www.w3schools.com/html/mov_bbb.mp4" \
  --lang zh \
  --mode summary
```

**期望**：
- 输出视频内容摘要（中文）
- 包含场景描述、关键信息
- 保存为 `./analysis.md`

**通过标准**：输出有意义的中文摘要，无报错

---

### T08：AudioAnalyzer — 音频分析

**目的**：验证语音转文字 + 情绪分析功能

**前提**：T06 已完成，有 `test-audio.mp3`

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/audio-analyzer
python run.py \
  --audio ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech/test-audio.mp3 \
  --lang zh \
  --emotion
```

**期望**：
- 转录文字基本准确（对比 T06 原文）
- 输出情绪分析结果
- 保存为 `./transcript.md`

**通过标准**：转录文字可辨认，情绪分析有输出

---

### T09：AvatarGen — 动态 Avatar 生成

**目的**：验证人物图转动态视频功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/avatar-gen
python run.py \
  --image "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=800" \
  --duration 5 \
  --output ./avatar-test.mp4
```

**期望**：
- 生成 5 秒左右的动态视频
- 人物形象基于输入图片
- 保存为 `./avatar-test.mp4`

**通过标准**：本地有 mp4 文件，可以播放

> ⚠️ 此任务耗时较长（30-60 秒），耐心等待

---

### T10：VoiceClone — 声音克隆

**目的**：验证声音克隆功能

**前提**：T06 已完成，有 `test-audio.mp3`（作为声音样本）

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/voice-clone
python run.py \
  --sample ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech/test-audio.mp3 \
  --text "这是用克隆声音合成的新内容，今天的加密货币市场非常活跃。" \
  --output ./cloned-test.mp3
```

**期望**：
- 合成语音音色接近样本
- 内容为新文字
- 保存为 `./cloned-test.mp3`

**通过标准**：本地有 mp3 文件，音色与样本相似

---

### T11：VideoGen — AI 视频生成

**目的**：验证文字生成视频功能

**执行**：
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/video-gen
python run.py \
  --prompt "一只熊猫坐在竹林里，用笔记本电脑查看加密货币行情，科技感十足" \
  --duration 5 \
  --style realistic \
  --output ./video-test.mp4
```

**期望**：
- 生成 5 秒视频
- 内容与描述相关
- 保存为 `./video-test.mp4`

**通过标准**：本地有 mp4 文件，可以播放

> ⚠️ 此任务耗时最长（30-120 秒），耐心等待

---

## 组合测试

---

### C01：场景 A — CT KOL 自动内容生产

**描述**：模拟 CT KOL Agent 从一张截图出发，自动生成推文配图 + 语音播报

**步骤**：

**Step 1** — 分析热点截图
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/visual-analyzer
python run.py --image "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
# 把输出的描述文字复制，用于下一步
```

**Step 2** — 生成推文配图
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/tweet-image-gen
python run.py --content "[把 Step 1 的输出摘要粘贴到这里]" --output ./ct-image.png
```

**Step 3** — 把分析结果转成语音播报
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech
python run.py \
  --text "[把 Step 1 的输出摘要粘贴到这里]" \
  --voice "male_1" \
  --output ./ct-audio.mp3
```

**通过标准**：
- ✅ Step 1：输出图片的中文分析
- ✅ Step 2：生成与 CT 相关的配图
- ✅ Step 3：生成对应的语音播报

---

### C02：场景 B — 虚拟 KOL 打造（简化版）

**描述**：生成一个虚拟 KOL 的形象图 + 克隆声音 + 配套视频

**前提**：T06 已完成，有 `test-audio.mp3`

**步骤**：

**Step 1** — 生成 KOL 形象概念图
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/idea-visualizer
python run.py \
  --idea "一位专业的加密货币分析师，亚洲面孔，穿着西装，背景是交易大厅，写实风格" \
  --output ./kol-avatar.png
```

**Step 2** — 去除背景，提取干净素材
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/bg-remover
python run.py --image ./idea-visualizer/kol-avatar.png --output ./kol-nobg.png
```

**Step 3** — 克隆声音，合成 KOL 播报内容
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/voice-clone
python run.py \
  --sample ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech/test-audio.mp3 \
  --text "大家好，我是阿尔法，今天为大家带来最新的加密货币市场分析。" \
  --output ./kol-voice.mp3
```

**Step 4** — 生成 KOL 视频内容
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/video-gen
python run.py \
  --prompt "专业加密货币分析师在演播室里分析市场行情，镜头感十足，科技感背景" \
  --duration 5 \
  --output ./kol-video.mp4
```

**通过标准**：
- ✅ Step 1：生成 KOL 形象图
- ✅ Step 2：生成透明背景版本
- ✅ Step 3：合成 KOL 播报语音
- ✅ Step 4：生成 KOL 视频

---

### C03：场景 D — 音视频内容二创

**描述**：分析一段视频 + 音频 → 理解内容 → 生成配图

**步骤**：

**Step 1** — 分析视频内容
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/video-analyzer
python run.py --video "https://www.w3schools.com/html/mov_bbb.mp4" --mode summary
# 记录输出的摘要
```

**Step 2** — 根据视频主题生成配图
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/idea-visualizer
python run.py --idea "[Step 1 输出的主题描述]，数字艺术风格" --output ./recreate-image.png
```

**Step 3** — 把内容转成语音
```bash
cd ~/.openclaw/workspace/projects/alpha-senses/skills/text-to-speech
python run.py --text "[Step 1 输出的摘要]" --output ./recreate-audio.mp3
```

**通过标准**：
- ✅ Step 1：输出视频摘要
- ✅ Step 2：生成相关配图
- ✅ Step 3：生成对应语音

---

## 测试汇报模板

每项测试完成后，按以下格式汇报：

```
T01 VisualAnalyzer：✅ 通过 / ❌ 失败
- 耗时：x 秒
- 输出：[一句话描述输出内容]
- 备注：[如有问题，说明错误信息]
```

---

## 注意事项

1. **API Key**：确保环境变量已设置
   ```bash
   echo $FAL_KEY       # 应该有值
   echo $MOONSHOT_API_KEY  # 应该有值
   ```

2. **耗时较长的 Skill**：AvatarGen（T09）和 VideoGen（T11）可能需要 1-2 分钟，正常等待

3. **测试顺序**：建议按 T01→T11 顺序，T06 先执行（生成 test-audio.mp3 供后续使用）

4. **失败处理**：某项失败不影响其他项，记录错误继续执行

5. **结果保存**：所有输出文件保存在各 Skill 目录下，方便对比

---

*测试手册 v1.0 | 作者：Alphana | 2026-02-21*
