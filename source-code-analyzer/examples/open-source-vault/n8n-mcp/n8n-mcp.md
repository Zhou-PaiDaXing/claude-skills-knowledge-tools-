---
title: "n8n-MCP"
aliases: [n8n-MCP, n8n MCP]
tags:
  - opensource
  - mcp-server
  - workflow-automation
  - n8n
github: https://github.com/nicepkg/n8n-mcp
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# n8n-MCP 项目分析报告

## 项目概览

**项目名称**: n8n-MCP  
**GitHub Stars**: 18,148  
**主要语言**: TypeScript  
**许可证**: MIT  
**项目描述**: A MCP for Claude Desktop / Claude Code / Windsurf / Cursor to build n8n workflows

> n8n-MCP 是一个 Model Context Protocol (MCP) 服务器，为 AI 助手提供对 n8n 工作流自动化平台的全面访问。支持 1,396 个 n8n 节点（812 核心 + 584 社区），帮助 AI 理解和构建 n8n 工作流。

---

## 技术栈分析

### 核心技术
| 技术 | 用途 | 版本 |
|------|------|------|
| **TypeScript** | 主要开发语言 | 5.8.3 |
| **Node.js** | 运行时环境 | 22+ |
| **MCP SDK** | Model Context Protocol | 1.28.0 |
| **Express.js** | HTTP 服务器 | 5.1.0 |
| **SQLite** | 本地数据存储 | better-sqlite3 |

### n8n 生态集成
| 包 | 用途 |
|----|------|
| **n8n-core** | n8n 核心功能 |
| **n8n-nodes-base** | n8n 基础节点 |
| **n8n-workflow** | n8n 工作流定义 |
| **@n8n/n8n-nodes-langchain** | LangChain 节点 |

### 开发工具
- **Vitest**: 测试框架 (v3.2.4)
- **Husky**: Git hooks
- **Secretlint**: 密钥扫描
- **TypeScript**: 类型检查

---

## 核心功能模块

### 1. 节点发现与管理
| 功能 | 描述 |
|------|------|
| **search_nodes** | 全文搜索所有节点，支持社区节点过滤 |
| **get_node** | 获取节点详细信息，多模式支持 |
| **validate_node** | 节点配置验证，支持多级验证 |

### 2. 模板系统
| 功能 | 描述 |
|------|------|
| **search_templates** | 多模式模板搜索 |
| **get_template** | 获取完整工作流模板 |
| **2,709 模板** | 预提取的工作流配置 |

### 3. 工作流管理 (需 n8n API)
| 功能 | 描述 |
|------|------|
| **n8n_create_workflow** | 创建新工作流 |
| **n8n_get_workflow** | 获取工作流详情 |
| **n8n_update_partial_workflow** | 部分更新工作流 |
| **n8n_delete_workflow** | 删除工作流 |
| **n8n_test_workflow** | 测试工作流执行 |

### 4. 执行管理
| 功能 | 描述 |
|------|------|
| **n8n_executions** | 执行记录管理 |
| **n8n_test_workflow** | 触发工作流测试 |

### 5. 凭证管理
| 功能 | 描述 |
|------|------|
| **n8n_manage_credentials** | 凭证的 CRUD 操作 |

---

## 代码结构概览

```
n8n-mcp/
├── src/
│   ├── mcp/                      # MCP 协议实现
│   │   ├── index.ts              # MCP 服务器入口
│   │   ├── stdio-wrapper.ts      # STDIO 传输包装
│   │   ├── tools/                # MCP 工具定义
│   │   └── prompts/              # MCP 提示模板
│   ├── services/                 # 业务服务
│   │   ├── node-service.ts       # 节点服务
│   │   ├── template-service.ts   # 模板服务
│   │   ├── n8n-api-service.ts    # n8n API 服务
│   │   ├── validation-service.ts # 验证服务
│   │   └── sqlite-storage-service.ts # SQLite 存储
│   ├── database/                 # 数据库相关
│   │   ├── database-adapter.ts
│   │   └── migrations/
│   ├── parsers/                  # 数据解析器
│   ├── types/                    # TypeScript 类型
│   ├── utils/                    # 工具函数
│   └── scripts/                  # 数据获取脚本
│       ├── fetch-templates.js    # 获取模板
│       ├── fetch-community-nodes.js # 获取社区节点
│       └── rebuild-database.js   # 重建数据库
├── data/                         # 数据文件
│   ├── nodes.db                  # SQLite 数据库 (75MB+)
│   └── workflow-patterns.json    # 工作流模式
├── docs/                         # 文档
│   ├── SELF_HOSTING.md
│   ├── N8N_DEPLOYMENT.md
│   └── setup guides/             # 各平台设置指南
├── dist/                         # 编译输出
└── tests/                        # 测试
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## 关键实现亮点

### 1. 大规模节点数据管理
```typescript
// 支持 1,396 个节点
- 812 核心节点 (n8n-nodes-base)
- 584 社区节点 (516 已验证)
- 99% 属性覆盖率
- 63.6% 操作覆盖率
```

### 2. 智能搜索系统
- **FTS5 全文搜索**: 基于 SQLite FTS5 的高性能搜索
- **多模式搜索**: 关键词、任务类型、节点类型、元数据
- **智能过滤**: 复杂度、目标受众、所需服务

### 3. 多级验证系统
```typescript
// 三级验证策略
1. minimal    - 快速必填字段检查 (<100ms)
2. full       - 完整验证，支持修复建议
3. runtime    - 运行时兼容性检查
```

### 4. 模板智能匹配
- **2,709 个模板** 完整元数据
- **2,646 个配置** 从热门模板提取
- **任务导向搜索**: 按常见任务类型筛选

### 5. 工作流差异更新
```typescript
// 支持的操作类型
- updateNode: 更新节点
- addConnection: 添加连接
- removeConnection: 移除连接
- cleanStaleConnections: 清理无效连接
```

### 6. 多平台支持
| 平台 | 支持状态 |
|------|----------|
| Claude Code | 完全支持 |
| Claude Desktop | 完全支持 |
| Cursor | 完全支持 |
| Windsurf | 完全支持 |
| VS Code + Copilot | 完全支持 |
| Codex CLI | 完全支持 |

---

## 适用场景建议

### 最佳使用场景

#### 1. AI 辅助工作流开发
```
场景: 开发者描述需求，AI 自动构建 n8n 工作流
示例: "创建一个 Slack 通知工作流，当收到 webhook 时发送消息"
AI 操作:
1. 搜索相关模板
2. 获取节点信息 (Webhook, Slack)
3. 验证配置
4. 生成工作流 JSON
```

#### 2. 工作流迁移与重构
- 批量更新工作流配置
- 节点版本升级
- 连接优化

#### 3. 学习与探索
- 发现新节点和功能
- 学习最佳实践
- 查看真实配置示例

#### 4. 团队协作
- 标准化工作流开发流程
- 减少配置错误
- 加速新成员上手

### 部署方式

| 方式 | 适用场景 | 复杂度 |
|------|----------|--------|
| **Cloud** | 快速开始，100 次/天免费 | 低 |
| **npx** | 本地快速测试 | 低 |
| **Docker** | 自托管生产环境 | 中 |
| **Railway** | 一键云部署 | 低 |
| **本地源码** | 开发定制 | 高 |

### 使用示例

#### 基础查询
```typescript
// 搜索节点
await search_nodes({ query: "slack", includeExamples: true })

// 获取节点详情
await get_node({ nodeType: "n8n-nodes-base.slack", detail: "full" })

// 验证配置
await validate_node({ nodeType, config, mode: "full" })
```

#### 工作流操作
```typescript
// 创建工作流
await n8n_create_workflow({ workflow })

// 部分更新
await n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [
    { type: "updateNode", nodeId: "node-1", changes: {...} },
    { type: "addConnection", source: "node-1", target: "node-2", ... }
  ]
})
```

---

## 项目链接

- **GitHub**: https://github.com/czlonkowski/n8n-mcp
- **在线服务**: https://dashboard.n8n-mcp.com
- **Docker**: ghcr.io/czlonkowski/n8n-mcp
- **npm**: https://www.npmjs.com/package/n8n-mcp

---

## 安全注意事项

⚠️ **重要警告**: 永远不要直接让 AI 编辑生产环境工作流！

建议流程：
1. 复制生产工作流
2. 在开发环境测试
3. 导出备份
4. 验证后部署

---

*分析时间: 2026-04-15*
