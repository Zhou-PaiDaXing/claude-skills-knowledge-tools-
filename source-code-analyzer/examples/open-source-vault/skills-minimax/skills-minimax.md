---
title: "MiniMax Skills"
aliases: [MiniMax Skills]
tags:
  - opensource
  - ai-skill
  - Python
github: https://github.com/nicepkg/minimax-skills
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# MiniMax Skills

## 项目简介

**MiniMax Skills** 是 MiniMax AI 官方提供的开发技能集合，专为 AI 编码代理设计，提供结构化、生产级的开发指导。这些技能涵盖前端、全栈、Android、iOS、Flutter、React Native 和着色器开发，并深度集成 MiniMax 的多模态 AI 能力（图像、视频、音频、音乐、TTS）。

- **GitHub**: https://github.com/MiniMax-AI/skills
- **Stars**: 10,548
- **License**: MIT
- **状态**: Beta（活跃开发中）
- **技能数量**: 18 个技能

---

## 技术栈分析

### 核心技术
| 技术 | 用途 |
|------|------|
| **Markdown** | 技能文档格式 |
| **YAML Frontmatter** | 技能元数据 |
| **React / Next.js** | 前端开发 |
| **Tailwind CSS** | 样式系统 |
| **Kotlin / Jetpack Compose** | Android 开发 |
| **Swift / SwiftUI / UIKit** | iOS 开发 |
| **Flutter** | 跨平台开发 |
| **GLSL** | 着色器开发 |
| **C# / .NET** | DOCX 处理 |
| **MiniMax API** | 多模态 AI 能力 |

### MiniMax API 集成
| API | 功能 |
|-----|------|
| **Image Generation** | 文生图、图生图、角色参考 |
| **Video Generation** | 文生视频、图生视频、首尾帧 |
| **Audio/TTS** | 文本转语音、声音克隆、声音设计 |
| **Music Generation** | 歌曲生成、乐器生成、翻唱 |
| **Vision** | 图像分析、OCR、UI 评审 |

---

## 核心功能模块

### 1. 开发技能 (Development Skills)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| **frontend-dev** | 全栈前端开发 | React/Next.js, Tailwind, Framer Motion, GSAP, p5.js, Three.js |
| **fullstack-dev** | 全栈后端架构 | REST API, JWT/OAuth, SSE/WebSocket, SQL/NoSQL |
| **android-native-dev** | Android 原生开发 | Kotlin, Jetpack Compose, Material Design 3 |
| **ios-application-dev** | iOS 应用开发 | UIKit, SnapKit, SwiftUI, Apple HIG |
| **flutter-dev** | Flutter 跨平台 | Widgets, Riverpod/Bloc, GoRouter |
| **react-native-dev** | React Native 开发 | Expo, 组件、导航、状态管理 |
| **shader-dev** | GLSL 着色器 | Ray marching, SDF, 粒子系统, ShaderToy |

### 2. 文档处理技能

| 技能 | 描述 | 技术 |
|------|------|------|
| **minimax-docx** | DOCX 创建/编辑/格式化 | OpenXML SDK (.NET), C# |
| **minimax-pdf** | PDF 生成/填充/重排 | 令牌设计系统 |
| **minimax-xlsx** | Excel 处理 | pandas, XML 模板 |
| **pptx-generator** | PowerPoint 生成 | PptxGenJS, XML 工作流 |

### 3. 多模态 AI 技能

| 技能 | 描述 | API |
|------|------|-----|
| **minimax-multimodal-toolkit** | 统一多模态入口 | TTS, 音乐, 视频, 图像 |
| **minimax-music-gen** | 音乐生成 | MiniMax Music API |
| **vision-analysis** | 视觉分析 | MiniMax VL API, GPT-4V 回退 |
| **gif-sticker-maker** | GIF 贴纸制作 | 图像+视频生成 |

### 4. 创意/娱乐技能

| 技能 | 描述 | 特点 |
|------|------|------|
| **buddy-sings** | Claude Code 宠物唱歌 | 个性化歌曲生成 |
| **minimax-music-playlist** | 个性化播放列表 | 音乐品味分析 |

---

## 代码结构概览

```
skills-minimax/
├── README.md                  # 英文文档
├── README_zh.md               # 中文文档
├── CONTRIBUTING.md            # 贡献指南
├── LICENSE                    # MIT 许可证
├── .claude/                   # Claude 配置
│   └── skills/
│       └── pr-review/         # PR 审查技能
├── .claude-plugin/            # Claude 插件配置
├── .codex/                    # Codex 配置
├── .cursor-plugin/            # Cursor 插件配置
├── .opencode/                 # OpenCode 配置
├── plugins/                   # 插件目录
└── skills/                    # 技能目录
    ├── frontend-dev/          # 前端开发
    │   └── SKILL.md
    ├── fullstack-dev/         # 全栈开发
    │   └── SKILL.md
    ├── android-native-dev/    # Android 开发
    │   └── SKILL.md
    ├── ios-application-dev/   # iOS 开发
    │   └── SKILL.md
    ├── flutter-dev/           # Flutter 开发
    │   └── SKILL.md
    ├── react-native-dev/      # React Native
    │   └── SKILL.md
    ├── shader-dev/            # 着色器开发
    │   └── SKILL.md
    ├── minimax-docx/          # DOCX 处理
    │   ├── SKILL.md
    │   └── scripts/
    │       └── dotnet/        # C# 实现
    │           ├── MiniMaxAIDocx.Core/
    │           └── MiniMaxAIDocx.Cli/
    ├── minimax-pdf/           # PDF 处理
    │   └── SKILL.md
    ├── minimax-xlsx/          # Excel 处理
    │   └── SKILL.md
    ├── pptx-generator/        # PPT 生成
    │   └── SKILL.md
    ├── minimax-multimodal-toolkit/  # 多模态工具
    │   └── SKILL.md
    ├── minimax-music-gen/     # 音乐生成
    │   └── SKILL.md
    ├── minimax-music-playlist/ # 播放列表
    │   └── SKILL.md
    ├── vision-analysis/       # 视觉分析
    │   └── SKILL.md
    ├── gif-sticker-maker/     # GIF 贴纸
    │   └── SKILL.md
    └── buddy-sings/           # 宠物唱歌
        └── SKILL.md
```

---

## 关键实现亮点

### 1. 标准化技能格式
```yaml
---
name: skill-name
description: Brief description
metadata:
  author: MiniMax AI
---

# Skill Title

## Overview
...

## When to Use
...

## Workflow
1. Step one
2. Step two

## Examples
...
```

### 2. 前端开发技能亮点
- **AI 生成媒体**: 集成 MiniMax API 生成图像、视频、音频
- **电影级动画**: Framer Motion、GSAP 高级动画
- **生成艺术**: p5.js、Three.js、Canvas
- **说服性文案**: AIDA 框架
- **技术栈**: React / Next.js + Tailwind CSS

### 3. DOCX 处理 (C#/.NET)
```csharp
// 三管道架构
// 1. 创建新文档
// 2. 填充/编辑现有文档
// 3. 应用模板格式

// XSD 验证门控
// OpenXML SDK 精确控制
// 零格式丢失编辑
```

### 4. 多模态工具包
```markdown
## MiniMax 多模态能力

### TTS
- 文本转语音
- 声音克隆
- 声音设计
- 多段落合成

### 音乐
- 歌曲生成
- 乐器生成
- 风格词汇表

### 视频
- 文生视频
- 图生视频
- 首尾帧
- 主体参考
- 多场景长视频

### 图像
- 文生图
- 图生图
- 角色参考
```

### 5. 着色器开发
- **Ray Marching**: 光线步进技术
- **SDF Modeling**: 有向距离场建模
- **流体模拟**: 实时流体效果
- **粒子系统**: 复杂粒子效果
- **程序化生成**: 噪声和纹理
- **ShaderToy 兼容**: 直接移植

---

## 适用场景建议

### 推荐场景
| 场景 | 推荐技能 | 说明 |
|------|----------|------|
| **现代 Web 开发** | frontend-dev | React/Next.js + AI 生成媒体 |
| **后端架构** | fullstack-dev | API 设计、认证、数据库 |
| **移动应用** | android-native-dev, ios-application-dev, flutter-dev, react-native-dev | 原生和跨平台 |
| **文档自动化** | minimax-docx, minimax-pdf, minimax-xlsx, pptx-generator | 办公文档处理 |
| **创意内容** | minimax-music-gen, minimax-multimodal-toolkit | AI 生成音乐/视频/图像 |
| **视觉特效** | shader-dev | GLSL 着色器、视觉效果 |
| **图像分析** | vision-analysis | OCR、UI 评审、图表提取 |

### 安装示例

#### Claude Code
```bash
claude plugin marketplace add https://github.com/MiniMax-AI/skills
claude plugin install minimax-skills
```

#### Cursor
```bash
git clone https://github.com/MiniMax-AI/skills.git ~/.cursor/minimax-skills
```

#### Codex
```bash
git clone https://github.com/MiniMax-AI/skills.git ~/.codex/minimax-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/minimax-skills/skills ~/.agents/skills/minimax-skills
```

### 使用示例

#### 前端开发
```markdown
使用 frontend-dev 技能创建一个着陆页：
- 使用 Next.js + Tailwind CSS
- 集成 Framer Motion 动画
- 使用 MiniMax API 生成英雄区背景视频
- 应用 AIDA 框架编写文案
```

#### 音乐生成
```markdown
使用 minimax-music-gen 技能：
- 生成一首关于 AI 未来的流行歌曲
- 使用高级控制模式编辑歌词
- 规划歌曲结构：主歌-副歌-桥段
```

#### DOCX 处理
```markdown
使用 minimax-docx 技能：
- 创建一份商业计划书
- 使用专业封面样式
- 应用企业品牌色彩
```

### 与竞品对比
| 特性 | MiniMax Skills | OpenAI Skills | Claude Skills |
|------|----------------|---------------|---------------|
| 多模态集成 | 深度集成 | 有限 | 有限 |
| 开发技能 | 全面 | 一般 | 一般 |
| 文档处理 | 专业级 | 基础 | 基础 |
| 创意 AI | 强 | 中等 | 中等 |
| 平台支持 | 多平台 | 多平台 | Claude 为主 |

---

## 总结

MiniMax Skills 是一套**多模态 AI 驱动、开发导向、生产级**的技能集合。其亮点包括：

1. **多模态深度集成**: MiniMax API 原生支持图像/视频/音频/音乐
2. **全栈开发覆盖**: 前端、后端、移动端、跨平台
3. **专业文档处理**: DOCX/PDF/XLSX/PPTX 完整支持
4. **创意 AI 能力**: 音乐生成、着色器开发、视觉分析
5. **多平台兼容**: Claude Code、Cursor、Codex、OpenCode

适合需要**AI 增强开发、多模态内容生成、专业文档处理**的开发者。
