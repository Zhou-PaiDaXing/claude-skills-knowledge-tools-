---
title: "Oh-my-mermaid"
aliases: [Oh-my-mermaid, oh-my-mermaid]
tags:
  - opensource
  - visualization
  - mermaid
  - TypeScript
github: https://github.com/nicepkg/oh-my-mermaid
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Oh-my-mermaid

> **Turn complex codebases into clear, navigable architecture diagrams with Claude Code**

---

## 项目简介

Oh-my-mermaid (omm) 是一个架构镜像工具，专为"vibe coding"时代设计。它能够将复杂的代码库转换为清晰、可导航的架构图，由 AI 生成架构文档，供人类理解。AI 在几秒钟内编写代码，但人类需要数小时才能理解它——如果不理解，代码库就变成了黑盒，甚至对开发者自己也是如此。omm 填补了这一鸿沟。

**核心特点：**
- AI 生成架构文档：代码库分析生成多角度架构视图
- 递归分析：复杂节点自动展开为嵌套子图
- Mermaid 图表：使用 Mermaid 语法生成图表
- 交互式查看器：Web 界面浏览架构层次
- 多平台支持：Claude Code、Codex、Cursor、OpenClaw、Antigravity
- 云端同步：可选的 ohmymermaid.com 云端存储

**项目链接：**
- GitHub: https://github.com/oh-my-mermaid/oh-my-mermaid
- npm: https://www.npmjs.com/package/oh-my-mermaid
- 云端: https://ohmymermaid.com

---

## 技术栈分析

### 核心技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| TypeScript | ^5.9.3 | 类型安全开发 |
| Node.js | >= 18 | 运行时 |
| tsup | ^8.5.1 | 构建工具 |
| YAML | ^2.8.3 | 配置和数据序列化 |
| vitest | ^4.1.0 | 测试框架 |

### 开发工具
| 工具 | 用途 |
|------|------|
| tsup | TypeScript 打包 |
| vitest | 单元测试 |
| @types/node | Node.js 类型定义 |

---

## 核心功能模块

### 1. CLI 模块 (`src/cli.ts`)
**命令系统：**
| 命令 | 功能 |
|------|------|
| `omm init` | 初始化 .omm/ 目录 |
| `omm setup [platform]` | 注册 AI 工具技能 |
| `omm update` | 更新 CLI 和插件 |
| `omm list` | 列出视角 (perspectives) |
| `omm tree <path>` | 显示元素树 |
| `omm read <path> <field>` | 读取字段 |
| `omm write <path> <field>` | 写入字段 |
| `omm show <path>` | 显示元素所有字段 |
| `omm delete <path>` | 删除元素 |
| `omm status` | 显示概览 |
| `omm diff <path>` | 比较图表版本 |
| `omm validate [path]` | 验证图表语法 |
| `omm view [--port]` | 启动 Web 查看器 |

**云端命令：**
| 命令 | 功能 |
|------|------|
| `omm login` | 登录 omm.dev |
| `omm logout` | 登出 |
| `omm link [org/slug]` | 链接云端项目 |
| `omm push` | 推送到云端 |
| `omm pull` | 从云端拉取 |
| `omm share` | 获取分享链接 |
| `omm org list` | 列出组织 |
| `omm org switch` | 切换组织 |

### 2. 平台集成 (`src/lib/platforms/`)
| 平台 | 模块 | 功能 |
|------|------|------|
| Claude Code | `claude.ts` | 插件安装和管理 |
| Codex | `codex.ts` | Codex 集成 |
| Cursor | `cursor.ts` | Cursor 规则安装 |
| OpenClaw | `openclaw.ts` | OpenClaw 集成 |
| Antigravity | `antigravity.ts` | Antigravity 集成 |

**平台工具函数 (`utils.ts`)：**
- `hasCommand()`: 检测命令是否存在
- `getPackageVersion()`: 获取包版本
- `getGlobalOmmPath()`: 获取全局 omm 路径

### 3. 存储系统 (`src/lib/store.ts`)
**本地存储结构：**
```
.omm/
├── overall-architecture/          # 视角目录
│   ├── description.md             # 描述
│   ├── diagram.mmd                # Mermaid 图表
│   ├── context.md                 # 上下文
│   ├── constraint.md              # 约束
│   ├── concern.md                 # 关注点
│   ├── todo.md                    # 待办
│   ├── note.md                    # 备注
│   ├── main-process/              # 嵌套元素
│   │   ├── description.md
│   │   ├── diagram.mmd
│   │   └── auth-service/          # 深层嵌套
│   │       └── ...
│   └── renderer/
│       └── ...
├── data-flow/
└── external-integrations/
```

**存储操作：**
- `readField()`: 读取字段内容
- `writeField()`: 写入字段内容
- `listPerspectives()`: 列出所有视角
- `getElementTree()`: 获取元素树结构
- `deleteElement()`: 删除元素

### 4. 云端同步 (`src/lib/cloud.ts`, `src/commands/`)
**API 接口：**
- 用户认证 (login/logout)
- 项目链接 (link)
- 数据推送 (push)
- 数据拉取 (pull)
- 分享链接生成 (share)
- 组织管理 (org)

### 5. Web 查看器 (`src/server/`)
- **HTTP 服务器**: 提供 Web 界面
- **文件监听**: 自动刷新
- **嵌套渲染**: 自动检测文件系统嵌套

### 6. 验证系统 (`src/lib/validate.ts`)
- Mermaid 语法验证
- 项目结构验证
- 字段完整性检查

### 7. 差异比较 (`src/lib/diff.ts`)
- 图表版本比较
- 变更检测

---

## 代码结构概览

```
oh-my-mermaid/
├── src/
│   ├── index.ts                    # 库入口
│   ├── cli.ts                      # CLI 入口 (7KB)
│   ├── types.ts                    # 类型定义
│   ├── commands/                   # 命令实现
│   │   ├── init.ts                 # 初始化
│   │   ├── setup.ts                # 平台设置
│   │   ├── update.ts               # 更新
│   │   ├── list.ts                 # 列出视角
│   │   ├── tree.ts                 # 显示树
│   │   ├── read-write.ts           # 读写操作
│   │   ├── show.ts                 # 显示元素
│   │   ├── delete.ts               # 删除
│   │   ├── status.ts               # 状态
│   │   ├── diff.ts                 # 差异
│   │   ├── refs.ts                 # 引用
│   │   ├── validate.ts             # 验证
│   │   ├── view.ts                 # 启动查看器
│   │   ├── login.ts                # 登录
│   │   ├── logout.ts               # 登出
│   │   ├── push.ts                 # 推送
│   │   ├── pull.ts                 # 拉取
│   │   ├── link.ts                 # 链接
│   │   ├── share.ts                # 分享
│   │   ├── org.ts                  # 组织管理
│   │   ├── config.ts               # 配置
│   │   └── class-field.ts          # 类字段
│   ├── lib/                        # 库模块
│   │   ├── store.ts                # 存储系统 (10KB)
│   │   ├── validate.ts             # 验证 (5KB)
│   │   ├── diff.ts                 # 差异 (3KB)
│   │   ├── refs.ts                 # 引用 (2KB)
│   │   ├── cloud.ts                # 云端 API (3KB)
│   │   ├── cloud-paths.ts          # 云端路径 (1KB)
│   │   ├── meta.ts                 # 元数据 (1KB)
│   │   └── platforms/              # 平台集成
│   │       ├── index.ts
│   │       ├── types.ts
│   │       ├── utils.ts            # 平台工具 (3KB)
│   │       ├── claude.ts           # Claude Code (2KB)
│   │       ├── codex.ts            # Codex (1KB)
│   │       ├── cursor.ts           # Cursor (3KB)
│   │       ├── openclaw.ts         # OpenClaw (1KB)
│   │       └── antigravity.ts      # Antigravity (1KB)
│   ├── server/                     # Web 服务器
│   │   ├── index.ts                # 服务器入口 (2KB)
│   │   ├── api.ts                  # API 路由 (3KB)
│   │   └── watcher.ts              # 文件监听 (1KB)
│   └── __tests__/                  # 测试套件
│       ├── store.test.ts
│       ├── validate.test.ts
│       ├── cursor.test.ts
│       └── ...
├── skills/                         # AI 技能定义
├── .claude-plugin/                 # Claude 插件
├── package.json                    # npm 配置
├── tsup.config.ts                  # 构建配置
└── README.md                       # 项目文档
```

---

## 关键实现亮点

### 1. 平台检测和设置
```typescript
// src/lib/platforms/claude.ts
export const claude: Platform = {
  name: 'Claude Code',
  id: 'claude',

  detect(): boolean {
    return hasCommand('claude');
  },

  isSetup(): boolean {
    const installed = getInstalledVersion();
    const current = getPackageVersion();
    return installed === current;
  },

  async setup(): Promise<void> {
    // 卸载旧版本
    // 添加 marketplace
    // 安装插件
  },
};
```

### 2. 文件系统存储
```typescript
// src/lib/store.ts
export interface ElementPath {
  perspective: string;    // e.g., "overall-architecture"
  elementPath: string[];  // e.g., ["main-process", "auth-service"]
}

export function readField(perspective: string, elementPath: string[], field: Field): string {
  const filePath = getFieldFilePath(perspective, elementPath, field);
  return fs.readFileSync(filePath, 'utf-8');
}
```

### 3. 嵌套元素检测
```typescript
// 自动从文件系统检测嵌套
// 有子目录的元素显示为可展开组
// 无子目录的元素显示为叶节点
export function getElementTree(perspective: string): ElementNode {
  const root = { name: perspective, children: [] };
  // 递归遍历目录构建树
}
```

### 4. 7 个标准字段
```typescript
// src/types.ts
export type Field = 
  | 'description'   // 描述
  | 'diagram'       // Mermaid 图表
  | 'context'       // 上下文
  | 'constraint'    // 约束
  | 'concern'       // 关注点
  | 'todo'          // 待办
  | 'note';         // 备注
```

### 5. 技能定义格式
```markdown
<!-- skills/skill.md -->
# /omm-scan

Analyze the codebase and generate architecture documentation.

## Steps
1. Identify major components and their relationships
2. Create perspectives (structure, data flow, integrations)
3. Generate Mermaid diagrams for each perspective
4. Recursively analyze complex nodes
5. Write to .omm/ directory
```

---

## 适用场景建议

### 1. 新项目入职
- **场景**: 新开发者加入项目，需要快速理解架构
- **优势**: 自动生成架构文档，多角度视图
- **使用**: `/omm-scan` 然后 `omm view`

### 2. 代码审查准备
- **场景**: 审查大型 PR 前理解影响范围
- **优势**: 可视化依赖关系，识别关键路径
- **使用**: 审查前运行 `omm-scan` 更新架构图

### 3. 架构决策记录
- **场景**: 记录和沟通架构决策
- **优势**: 7 个字段完整记录上下文、约束、关注点
- **使用**: 在 `constraint.md` 和 `concern.md` 中记录决策依据

### 4. 技术债务管理
- **场景**: 跟踪和规划重构
- **优势**: `todo.md` 字段记录待办，与架构图关联
- **使用**: 在相关元素的 todo 字段中添加重构任务

### 5. 团队协作
- **场景**: 分布式团队共享架构理解
- **优势**: 云端同步，分享链接
- **使用**: `omm push` 后 `omm share` 获取分享链接

### 6. 文档自动化
- **场景**: 保持架构文档与代码同步
- **优势**: AI 自动分析，增量更新
- **使用**: Git 钩子触发 `omm-scan`

---

## 快速开始

### 安装
```bash
npm install -g oh-my-mermaid && omm setup
```

### 使用技能
```
/omm-scan
```

### 查看结果
```bash
omm view
```

### 云端同步
```bash
omm login && omm link && omm push
```

---

## 支持的平台

| 平台 | 安装命令 |
|------|----------|
| Claude Code | `omm setup claude` |
| Codex | `omm setup codex` |
| Cursor | `omm setup cursor` |
| OpenClaw | `omm setup openclaw` |
| Antigravity | `omm setup antigravity` |

---

## 输出结构示例

```
.omm/
├── overall-architecture/
│   ├── description.md
│   ├── diagram.mmd
│   ├── context.md
│   ├── main-process/
│   │   ├── description.md
│   │   ├── diagram.mmd
│   │   └── auth-service/
│   │       ├── description.md
│   │       └── diagram.mmd
│   └── renderer/
│       └── ...
├── data-flow/
│   └── ...
└── external-integrations/
    └── ...
```

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)

---

## 开发贡献

```bash
git clone https://github.com/oh-my-mermaid/oh-my-mermaid.git
cd oh-my-mermaid
npm install && npm run build
npm test
```

使用 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范。

---

## 路线图

详见 [docs/ROADMAP.md](./docs/ROADMAP.md)
