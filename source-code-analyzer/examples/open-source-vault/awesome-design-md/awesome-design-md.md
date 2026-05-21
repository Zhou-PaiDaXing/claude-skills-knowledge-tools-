---
title: "Awesome Design.md"
aliases: [Awesome Design]
tags:
  - opensource
  - curated-list
  - visualization
  - design
github: ""
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Awesome Design.md 项目分析报告

## 项目概览

**项目名称**: Awesome Design.md  
**GitHub Stars**: 51,612  
**主要语言**: Markdown  
**许可证**: MIT  
**项目描述**: A collection of DESIGN.md files inspired by popular brand design systems

> 这是一个精心策划的 DESIGN.md 文件集合，灵感来自流行的品牌设计系统。每个文件都是从真实网站提取的设计系统文档，帮助 AI 代理生成一致的 UI。

---

## 技术栈分析

### 核心技术
| 技术 | 用途 |
|------|------|
| **Markdown** | 设计系统文档格式 |
| **HTML** | 预览文件格式 |
| **YAML** | 技能元数据格式 |

### 设计系统来源
项目包含 66+ 个来自知名网站的设计系统：

#### AI & LLM 平台
- Claude, Cohere, ElevenLabs, Mistral AI, Ollama, xAI 等

#### 开发者工具
- Cursor, Vercel, Raycast, Warp, Expo 等

#### 后端与数据库
- Supabase, MongoDB, ClickHouse, PostHog, Sentry 等

#### 生产力工具
- Notion, Linear, Figma, Framer, Airtable 等

#### 金融科技
- Stripe, Coinbase, Revolut, Binance, Wise 等

#### 电商与零售
- Airbnb, Shopify, Nike, Meta 等

#### 汽车
- Tesla, BMW, Ferrari, Lamborghini, Bugatti 等

---

## 核心功能模块

### 1. 设计系统文档 (DESIGN.md)
每个设计系统包含以下部分：

| 章节 | 内容 |
|------|------|
| **Visual Theme & Atmosphere** | 视觉主题和氛围 |
| **Color Palette & Roles** | 色彩调色板和语义角色 |
| **Typography Rules** | 排版规则和层级 |
| **Component Stylings** | 组件样式 (按钮、卡片、输入框等) |
| **Layout Principles** | 布局原则和间距系统 |
| **Depth & Elevation** | 深度和阴影系统 |
| **Do's and Don'ts** | 设计规范和禁忌 |
| **Responsive Behavior** | 响应式行为 |
| **Agent Prompt Guide** | AI 代理提示指南 |

### 2. 预览文件
- **preview.html**: 视觉目录，展示色彩、排版、按钮、卡片
- **preview-dark.html**: 深色模式预览

### 3. 在线服务
- **getdesign.md**: 托管的设计系统查看服务
- 支持设计系统请求和定制

---

## 代码结构概览

```
awesome-design-md/
├── design-md/                    # 设计系统集合
│   ├── claude/                   # Anthropic Claude 设计系统
│   │   ├── README.md
│   │   ├── DESIGN.md
│   │   ├── preview.html
│   │   └── preview-dark.html
│   ├── vercel/                   # Vercel 设计系统
│   ├── stripe/                   # Stripe 设计系统
│   ├── notion/                   # Notion 设计系统
│   ├── linear.app/               # Linear 设计系统
│   └── ... (66+ 个设计系统)
├── .github/                      # GitHub 配置
│   ├── FUNDING.yml
│   └── ISSUE_TEMPLATE/
├── README.md                     # 项目说明
├── CONTRIBUTING.md               # 贡献指南
└── LICENSE                       # MIT 许可证
```

---

## 关键实现亮点

### 1. 标准化格式
基于 Google Stitch 的 DESIGN.md 格式规范：
```markdown
---
name: site-name
description: Brief description
---

# Visual Theme & Atmosphere
...

# Color Palette & Roles
| Token | Hex | Role |
|-------|-----|------|
| primary | #FF4D00 | CTA buttons |
```

### 2. 完整的设计令牌
每个设计系统包含：
- **色彩系统**: 主色、辅助色、语义色、功能色
- **排版系统**: 字体家族、字重、行高、层级
- **间距系统**: 基础单位、间距比例
- **阴影系统**: 层级阴影、发光效果
- **圆角系统**: 组件圆角规范

### 3. AI 友好的结构
- 纯文本格式，LLM 易于解析
- 表格化的设计令牌
- 明确的 Do's and Don'ts
- 可直接使用的提示模板

### 4. 分类组织
按行业和用途分类：
- AI & LLM 平台
- 开发者工具
- 生产力 SaaS
- 金融科技
- 电商零售
- 汽车

---

## 适用场景建议

### 最佳使用场景

#### 1. AI 辅助 UI 开发
```
使用场景: 告诉 AI "按照 Stripe 的设计风格构建支付页面"
操作: 复制 stripe/DESIGN.md 到项目根目录
结果: AI 生成符合 Stripe 设计语言的 UI
```

#### 2. 品牌一致性维护
- 确保多个页面/产品保持一致的视觉风格
- 新团队成员快速理解设计规范

#### 3. 设计系统学习
- 研究知名产品的设计决策
- 理解不同行业的设计模式

#### 4. 快速原型开发
- 基于成熟设计系统快速搭建原型
- 减少设计探索时间

### 使用方式

#### 方式一: 直接复制
```bash
cp design-md/stripe/DESIGN.md ./DESIGN.md
```

#### 方式二: 在线查看
访问 https://getdesign.md/stripe/design-md

#### 方式三: AI Agent 集成
```
"使用 DESIGN.md 中的设计规范构建登录页面"
```

---

## 项目链接

- **GitHub**: https://github.com/VoltAgent/awesome-design-md
- **在线服务**: https://getdesign.md
- **Discord**: https://s.voltagent.dev/discord

---

## 与其他工具的对比

| 工具 | 格式 | AI 友好 | 实时预览 | 适用场景 |
|------|------|---------|----------|----------|
| **Design.md** | Markdown | 优秀 | 支持 | AI 代码生成 |
| Figma | 二进制 | 差 | 优秀 | 设计师协作 |
| Storybook | JS/TS | 中等 | 优秀 | 组件开发 |
| Tailwind Config | JS | 中等 | 无 | 开发配置 |

---

*分析时间: 2026-04-15*
