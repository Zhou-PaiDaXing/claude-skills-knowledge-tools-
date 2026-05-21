---
title: "Obsidian Clipper"
aliases: [Obsidian Clipper, obsidian-clipper]
tags:
  - opensource
  - obsidian
  - productivity
  - browser-extension
github: https://github.com/obsidianmd/obsidian-clipper
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Obsidian Clipper

> **GitHub**: [jgchristopher/obsidian-clipper](https://github.com/jgchristopher/obsidian-clipper)  
> **Stars**: 281  
> **Language**: TypeScript  
> **License**: MIT  
> **Type**: Obsidian Plugin

---

## 项目简介

Obsidian Clipper 是一个 Obsidian 插件，允许用户将网页内容捕获为 Markdown 条目，保存到 Obsidian 的日记或指定笔记中。它通过生成 Bookmarklet（书签小工具）或 Chrome 扩展的方式，实现从浏览器一键剪辑内容到 Obsidian。

**核心功能**：将网页高亮内容转换为 Markdown 并保存到 Obsidian

---

## 技术栈分析

### 核心技术
| 组件 | 版本/说明 | 用途 |
|------|-----------|------|
| TypeScript | 4.7.4 | 主要开发语言 |
| Obsidian API | latest | 插件开发框架 |
| Svelte | 3.55.1 | UI 组件框架 |
| esbuild | 0.14.47 | 构建工具 |
| Webpack | ^5.75.0 | Bookmarklet 打包 |
| TailwindCSS | ^3.2.7 | 样式框架 |

### 关键依赖
| 包 | 用途 |
|----|------|
| `turndown` | HTML 转 Markdown |
| `obsidian-daily-notes-interface` | 日记笔记接口 |
| `parse-domain` | 域名解析 |
| `deepmerge-ts` | 配置合并 |
| `@dagrejs/dagre` | 图形布局 (Canvas 支持) |

### 开发工具
- ESLint: 代码检查
- Vitest: 单元测试
- bookmarklet: 书签工具生成

---

## 核心功能模块

### 1. Bookmarklet 生成器
```typescript
// 生成浏览器书签工具
class BookmarketlGenerator {
    generateBookmarklet(): string {
        // 压缩并打包剪辑代码为可书签化 JavaScript
    }
}
```

**工作流程**：
1. 用户在 Obsidian 中生成 Bookmarklet
2. 将 Bookmarklet 拖到浏览器书签栏
3. 在网页上选中文本后点击 Bookmarklet
4. 内容通过 Obsidian URI 协议发送到 Obsidian

### 2. 内容处理器
```typescript
// HTML 转 Markdown
import Turndown from 'turndown';

// 表格支持
import { tables } from './build/bookmarkletcode/markdown/tables';

// 转换流程：选中 HTML → Turndown → Markdown → Obsidian URI
```

### 3. 笔记条目类型

| 条目类型 | 说明 |
|----------|------|
| **DailyPeriodicNoteEntry** | 保存到日记笔记 |
| **WeeklyPeriodicNoteEntry** | 保存到周记笔记 |
| **TopicNoteEntry** | 保存到指定主题笔记 |
| **AdvancedNoteEntry** | 高级存储 (按域名组织) |
| **CanvasEntry** | 保存到 Canvas 画布 |

### 4. 设置系统
```typescript
interface ObsidianClipperSettings {
    useDailyNote: boolean;           // 使用日记
    useWeeklyNote: boolean;          // 使用周记
    dailyNoteHeading: string;        // 日记标题
    weeklyNoteHeading: string;       // 周记标题
    dailyEntryTemplateLocation: string;   // 日记模板
    weeklyEntryTemplateLocation: string;  // 周记模板
    topicEntryTemplateLocation: string;   // 主题模板
    advanced: boolean;               // 高级模式
    advancedStorageFolder: string;   // 高级存储文件夹
    captureComments: boolean;        // 捕获评论
    markdownSettings: MarkdownSettings;  // Markdown 设置
    experimentalCanvas: boolean;     // Canvas 实验功能
}
```

### 5. Obsidian 协议处理
```typescript
// 注册协议处理器
this.registerObsidianProtocolHandler('obsidian-clipper', async (e) => {
    const { url, title, highlightData, comments, notePath } = e;
    // 根据配置写入对应笔记
});
```

---

## 代码结构概览

```
obsidian-clipper/
├── src/
│   ├── main.ts                     # 插件主入口
│   ├── clippeddata.ts              # 剪辑数据结构
│   ├── types.ts                    # 类型定义
│   │
│   ├── settings/                   # 设置系统
│   │   ├── types.ts                # 设置类型
│   │   ├── settingsstore.ts        # 设置存储
│   │   └── sveltesettingtypes.ts   # Svelte 设置类型
│   │
│   ├── periodicnotes/              # 周期性笔记
│   │   ├── dailyperiodicnoteentry.ts   # 日记条目
│   │   ├── weeklyperiodicnoteentry.ts  # 周记条目
│   │   ├── periodicnoteentry.ts        # 基类
│   │   ├── filewriter.ts               # 文件写入
│   │   ├── appendwriter.ts             # 追加写入
│   │   └── prependwriter.ts            # 前置写入
│   │
│   ├── advancednotes/              # 高级笔记
│   │   └── advancednoteentry.ts
│   │
│   ├── bookmarkletlink/            # Bookmarklet 生成
│   │   └── build-bookmarkletgenerator.js
│   │
│   ├── build/                      # 构建相关
│   │   ├── bookmarkletcode/
│   │   │   ├── index.ts            # Bookmarklet 主代码
│   │   │   └── markdown/
│   │   │       └── tables.ts       # 表格转换
│   │   └── version-bump.mjs        # 版本更新
│   │
│   ├── abstracts/                  # 抽象类
│   │   └── noteentry.ts
│   │
│   ├── modals/                     # 模态框组件
│   │   └── BookmarkletModalComponent.svelte
│   │
│   ├── settings/                   # 设置组件
│   │   └── SettingsComponent.svelte
│   │
│   ├── canvasentry.ts              # Canvas 支持
│   ├── topicnoteentry.ts           # 主题笔记条目
│   └── utils/                      # 工具函数
│       ├── fileutils.ts
│       ├── templateutils.ts
│       └── utility.ts
│
├── package.json
├── esbuild.config.mjs              # esbuild 配置
├── webpack.config.js               # Webpack 配置
├── tailwind.config.js              # Tailwind 配置
├── vitest.config.ts                # 测试配置
└── manifest.json                   # 插件清单
```

---

## 关键实现亮点

### 1. 多目标写入策略
```typescript
// 根据用户配置选择写入目标
if (notePath && notePath !== '') {
    // 写入指定主题笔记
    new TopicNoteEntry(...).writeToNote(file, noteEntry);
} else {
    if (this.settings.useDailyNote) {
        // 写入日记
        new DailyPeriodicNoteEntry(...).writeToPeriodicNote(...);
    }
    if (this.settings.useWeeklyNote) {
        // 写入周记
        new WeeklyPeriodicNoteEntry(...).writeToPeriodicNote(...);
    }
}
```

### 2. 模板系统
```typescript
// 支持自定义模板
export interface MarkdownSettings {
    clipLinkTemplate: string;    // 链接模板
    clipSelectionTemplate: string;  // 选中文本模板
    clipCommentTemplate: string;    // 评论模板
}

// 默认模板示例
clipLinkTemplate: "[{title}]({url})"
clipSelectionTemplate: "> {selection}"
```

### 3. Chrome 扩展支持
- 生成可下载的 Chrome 扩展 ZIP 包
- 适用于不支持 Bookmarklet 的浏览器 (如 Arc)
- 通过外部服务 `obsidianclipper.com` 生成扩展包装器

### 4. 表格转换增强
```typescript
// 集成 Advanced Tables 插件支持
// 使用 turndown 插件将 HTML 表格转为 Markdown 表格
```

---

## 适用场景建议

### 适合场景
| 场景 | 说明 |
|------|------|
| **网页剪藏** | 将网页内容保存到 Obsidian 笔记 |
| **研究收集** | 收集参考资料到日记或主题笔记 |
| **阅读笔记** | 边阅读边记录高亮和评论 |
| **知识管理** | 构建个人知识库 |

### 使用方式

**安装**
1. 在 Obsidian 社区插件市场搜索 "Obsidian Clipper"
2. 安装并启用插件

**配置**
1. 打开设置，配置日记/周记选项
2. 选择存储位置 (日记、周记或主题笔记)
3. 自定义模板 (可选)

**使用 Bookmarklet**
1. 运行命令 "Vault Bookmarklet"
2. 将生成的链接拖到浏览器书签栏
3. 在网页上选中文本，点击书签

**使用 Chrome 扩展**
1. 运行命令生成扩展 ZIP
2. 解压并加载到 Chrome (开发者模式)

### 命令列表
| 命令 | 功能 |
|------|------|
| Vault Bookmarklet | 生成 Vault 级别的 Bookmarklet |
| Vault Bookmarklet to Clipboard | 复制 Bookmarklet 到剪贴板 |
| Topic Bookmarklet | 为当前笔记生成 Bookmarklet |
| Topic Bookmarklet to Clipboard | 复制主题 Bookmarklet |
| Canvas Bookmarklet | 为 Canvas 生成 Bookmarklet |

---

## 依赖的外部服务

**Obsidian Clipper Extension Maker**
- 服务地址: https://obsidianclipper.com
- 用途: 为 Chrome 浏览器生成扩展包装器
- 代码开源: [jgchristopher/obsidian_clipper_extension_maker](https://github.com/jgchristopher/obsidian_clipper_extension_maker)

---

## 相关资源

- **文档**: https://docs.obsidianclipper.com
- **入门视频**: [YouTube](https://youtu.be/kINRwNG2LCQ)
- **依赖插件**:
  - [Obsidian Advanced URI](https://github.com/Vinzent03/obsidian-advanced-uri)
  - [Obsidian Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes)
  - [Advanced Tables](https://github.com/tgrosinger/advanced-tables-obsidian)
- **核心库**: [Turndown](https://github.com/mixmark-io/turndown)
