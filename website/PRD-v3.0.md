# Alpha Senses Website PRD (v3.0) - [The Notion Soul Edition]
# Target: Cooclo (CTO)

## 1. 核心叙事目标
不要推销功能，要讲一个“Agents 获得感官”的故事。视觉风格强制对标 Notion 3.0。

## 2. 页面架构 (Scroll Flow)
### 2.1 Hero (极致克制)
- **文字**: "Agents Think. Now They Sense." (Inter ExtraBold)
- **副标题**: "Giving AI Agents the eyes and ears they've been missing. Built for the era of multi-modal agency."
- **吉祥物**: 限制在页面右上角或 Logo 旁，高度禁止超过 64px。

### 2.2 The Gap (Bento Grid)
- 用 Shadcn 的 Bento Grid 实现。
- **格 1 (Problem)**: "Blind Agents" - 描述 Agent 无法处理图像的局限。
- **格 2 (Solution)**: "Visual Awareness" - 展示 Visual Analyzer 的实时反馈。
- **格 3 (Scale)**: "Multi-Sense" - 描述 11 个感官的横向覆盖。

### 2.3 Interactive Showcase (模拟 Notion 3.0 侧边标签)
- 实现一个 Tabs 组件。
- 点击 [Vision], [Audio], [Creation], [Processing]。
- 主内容区动态展示对应的代码调用样式和预期结果。

### 2.4 Ecosystem (Trust Layer)
- 品牌墙风格展示: fal.ai, Moonshot, OpenClaw.

## 3. 视觉规范
- **背景**: #FFFFFF (手机端强制白色) / #F7F6F3 (Notion 灰色表面)。
- **字体**: Inter + JetBrains Mono (代码区)。
- **边框**: 0.5px 极细边框，圆角 8px。

## 4. 移动端硬性规范
- **Vertical Stack**: 所有 Bento 格子在手机端自动转化为单列。
- **Logo Only**: 手机端 Navbar 仅保留 Logo 和 Hamburger。
- **No Overlap**: 严禁任何图片层堆叠。
