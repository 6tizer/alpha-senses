# Alpha Senses Website PRD (v1.0)
# Created by: Alphana (CEO)
# Target: Cooclo (CTO)

## 1. 产品背景
Alpha Senses 是基于 fal.ai 的 11 个 AI 感官技能包。本官网旨在提供专业、极简的品牌展示，并将流量引回 GitHub 和 ClawHub。

## 2. 核心审美 (Atomic Design)
- **风格**: 完全对标 Notion 极简美学。
- **基因**: 遵循 `projects/shared/design-system/WHITEPAPER-V1.md`。
- **背景**: 深空黑 (#000000)。
- **强调色**: 龙虾红 (#DC2626)。

## 3. 功能需求
### 3.1 导航系统 (Navigation)
- **Desktop**: 固定左侧边栏 (280px)，包含技能分类列表。
- **Mobile**: **必须具备全适配支持**。侧边栏折叠至左上角图标，通过 Shadcn `Sheet` (Drawer) 组件唤起。

### 3.2 内容展示 (The Stage)
- **Hero Section**: 品牌 Logo + Mascot (龙虾) + Slogan。
- **Skill Detail View**: 
    - 技能名称 + 标签。
    - 功能描述。
    - 代码示例 (Code Block，必须支持手机端横滚)。
    - Mock 展示图 (使用已处理的资产)。

### 3.3 全球化
- **Bilingual**: 默认中文，支持一键切换英文。

## 4. 技术栈要求
- **Framework**: Vite + React 19 + TypeScript.
- **Styling**: Tailwind CSS 4.0.
- **UI Components**: Shadcn UI (Radix UI).
- **Icons**: Lucide React.

## 5. 验收标准
1. Chrome 开发者工具模拟 iPhone 15 Pro 无布局错位。
2. 符合白皮书定义的 4px 间距系统。
3. 部署至 Vercel 速度秒开。
