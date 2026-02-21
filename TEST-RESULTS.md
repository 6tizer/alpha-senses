# fal.ai Skills 测试结果

> 测试时间：2026-02-20

---

## ✅ Skill 1: VisualAnalyzer（视觉分析）

- **端点**：`fal-ai/florence-2-large/detailed-caption`
- **状态**：✅ 通过
- **测试输入**：猫咪图片（Unsplash）
- **输出**：`The image shows a black and white cat laying on top of a wooden table, with a green wall in the background.`
- **延迟**：约 3-5 秒
- **用法**：`python3 run.py --image <图片URL>`

---

## ✅ Skill 2: IdeaVisualizer（想法视觉化）

- **端点**：`fal-ai/flux/schnell`
- **状态**：✅ 通过
- **测试输入**：`"a cute panda mascot for a crypto app, dark background, neon green accent, minimal design"`
- **输出**：生成图片 URL + 本地保存
- **生成图**：https://v3b.fal.media/files/b/0a8f2382/uQ1ih3c2W58sG21J4b9sK.jpg
- **延迟**：约 3-5 秒
- **用法**：`python3 run.py --idea "描述" --output ./output.png`

---

## ✅ Skill 3: BackgroundRemover（去背景）

- **端点**：`fal-ai/bria/background/remove`
- **状态**：✅ 通过
- **测试输入**：猫咪图片（Unsplash）
- **输出**：透明背景 PNG，URL + 本地保存
- **输出图**：https://v3b.fal.media/files/b/0a8f2389/xLpbEBi959450XLCtPPAK.png
- **延迟**：约 3-5 秒
- **用法**：`python3 run.py --image <图片URL> --output ./no-bg.png`

---

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| `fal-ai/llava-next` 超时 | 端点已废弃 | 改用 `florence-2-large/detailed-caption` |
| `fal-ai/bria/rmbg` 404 | 端点路径变了 | 改用 `fal-ai/bria/background/remove` |
| `florence-2-large` 422 | Wikipedia 图片有防盗链 | 改用 Unsplash URL |
| `results` 字段是字符串非字典 | API 返回格式与文档不符 | 做类型判断兼容 |
