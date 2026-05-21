---
title: "Anthropic SDK TypeScript"
aliases: [Anthropic SDK, anthropic-sdk-typescript]
tags:
  - opensource
  - sdk
  - TypeScript
  - Anthropic
github: https://github.com/anthropics/anthropic-sdk-typescript
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Anthropic SDK TypeScript

## 项目简介

**Anthropic SDK TypeScript** 是 Anthropic 官方提供的 TypeScript/JavaScript 客户端库，用于访问 Claude API。该 SDK 提供了对 Anthropic 安全优先的语言模型 API 的完整访问能力，支持服务器端 TypeScript 或 JavaScript 应用程序开发。

- **GitHub**: https://github.com/anthropics/anthropic-sdk-typescript
- **NPM 包**: `@anthropic-ai/sdk`
- ** Stars**: 1,855
- **License**: MIT
- **Node.js 要求**: 18+

---

## 技术栈分析

### 核心依赖
| 依赖 | 版本 | 用途 |
|------|------|------|
| `json-schema-to-ts` | ^3.1.1 | JSON Schema 到 TypeScript 类型转换 |
| `zod` | ^3.25.0 \|\| ^4.0.0 (peer) | 运行时类型验证（可选） |

### 开发工具链
| 工具 | 用途 |
|------|------|
| **TypeScript** | 5.8.3 - 主要开发语言 |
| **Yarn** | 1.22.22 - 包管理器 |
| **Jest** | 29.4.0 - 测试框架 |
| **ESLint** | 9.39.1 - 代码检查 |
| **Prettier** | 3.0.0 - 代码格式化 |
| **SWC** | 1.3.102 - 快速编译 |
| **tsc-multi** | 多目标编译 |

### 架构特点
- **Monorepo 结构**: 使用 Yarn Workspaces 管理多包
- **多平台支持**: 主 SDK + AWS SDK + Bedrock SDK + Vertex SDK + Foundry SDK
- **双模块格式**: 同时支持 CommonJS 和 ESM
- **OpenAPI 生成**: 代码从 OpenAPI 规范自动生成（Stainless 工具）

---

## 核心功能模块

### 1. 核心客户端 (`src/client.ts`)
- **Anthropic 主类**: 49KB 的核心客户端实现
- **请求处理**: HTTP 请求构建、认证、重试逻辑
- **流式支持**: SSE (Server-Sent Events) 流处理
- **错误处理**: 完整的错误类型体系

### 2. API 资源 (`src/resources/`)
| 模块 | 功能 |
|------|------|
| `messages/` | 消息 API（主要接口） |
| `completions/` | 文本补全 API |
| `models/` | 模型信息查询 |
| `beta/` | Beta 功能接口 |

### 3. 辅助工具 (`src/helpers/`)
- **Zod 集成**: 结构化输出验证
- **JSON Schema**: JSON Schema 支持
- **MCP**: Model Context Protocol 支持 (20.7KB)
- **Memory**: 记忆功能支持

### 4. 内部工具 (`src/internal/`)
- **平台检测**: 自动识别运行环境
- **请求选项**: 请求配置管理
- **流工具**: 流数据处理
- **文件上传**: 文件上传支持

### 5. 子包生态 (`packages/`)
| 包名 | 用途 |
|------|------|
| `aws-sdk` | AWS Bedrock 集成 |
| `bedrock-sdk` | Amazon Bedrock 专用 |
| `vertex-sdk` | Google Cloud Vertex AI |
| `foundry-sdk` | Palantir Foundry 集成 |

---

## 代码结构概览

```
anthropic-sdk-typescript/
├── src/
│   ├── client.ts              # 核心客户端 (49KB)
│   ├── index.ts               # 主入口
│   ├── core/                  # 核心功能
│   │   ├── api-promise.ts     # API Promise 封装
│   │   ├── error.ts           # 错误类型
│   │   ├── pagination.ts      # 分页处理
│   │   ├── streaming.ts       # 流处理 (10.7KB)
│   │   └── uploads.ts         # 文件上传
│   ├── resources/             # API 资源
│   │   ├── messages/          # 消息 API
│   │   ├── completions/       # 补全 API
│   │   ├── models/            # 模型 API
│   │   └── beta/              # Beta API
│   ├── helpers/               # 辅助工具
│   │   ├── beta/              # Beta 辅助
│   │   ├── zod.ts             # Zod 集成
│   │   └── json-schema.ts     # JSON Schema
│   ├── internal/              # 内部工具
│   │   ├── decoders/          # 解码器
│   │   ├── detect-platform.ts # 平台检测
│   │   └── utils/             # 工具函数
│   └── tools/                 # 工具函数
├── packages/                  # 子包
│   ├── aws-sdk/
│   ├── bedrock-sdk/
│   ├── vertex-sdk/
│   └── foundry-sdk/
├── examples/                  # 示例代码 (31个)
└── tests/                     # 测试套件
```

---

## 关键实现亮点

### 1. 类型安全架构
```typescript
// 完整的 TypeScript 类型支持
export type MessageCreateParams = {
  model: string;
  max_tokens: number;
  messages: MessageParam[];
  // ... 完整参数类型
};
```

### 2. 流式处理
- **SSE 解析**: 自定义行解码器和 JSONL 解码器
- **实时输出**: 支持思考过程流式展示
- **工具调用流**: 工具调用结果流式返回

### 3. 多平台适配
```typescript
// 自动平台检测
import { getPlatformHeaders } from './internal/detect-platform';
// 支持 Node.js、Deno、Bun、Edge Runtime
```

### 4. 错误处理体系
```typescript
export class APIError extends AnthropicError {
  // 详细的错误分类
  // - AuthenticationError
  // - RateLimitError
  // - BadRequestError
  // - InternalServerError
  // ...
}
```

### 5. 工具使用支持
- **MCP 集成**: Model Context Protocol 完整支持
- **工具调用**: 内置工具调用循环
- **结构化输出**: Zod/JSON Schema 验证

---

## 适用场景建议

### 推荐场景
| 场景 | 说明 |
|------|------|
| **企业级应用** | 需要稳定、安全的 Claude API 访问 |
| **流式对话** | 实时聊天、打字机效果 |
| **工具调用** | 需要与外部工具集成的 Agent |
| **多平台部署** | AWS/GCP/Azure 多云环境 |
| **类型安全** | 大型 TypeScript 项目 |

### 集成示例
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// 基础对话
const message = await client.messages.create({
  model: 'claude-opus-4-6',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello, Claude' }],
});

// 流式输出
const stream = await client.messages.create({
  model: 'claude-sonnet-4-5',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});

for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta') {
    process.stdout.write(chunk.delta.text);
  }
}
```

### 与竞品对比
| 特性 | Anthropic SDK | OpenAI SDK | Google SDK |
|------|---------------|------------|------------|
| 类型安全 | 优秀 | 良好 | 一般 |
| 流式支持 | 完整 | 完整 | 部分 |
| 多平台 | 优秀 | 良好 | 一般 |
| 工具调用 | 原生支持 | 原生支持 | 有限 |
| 文档质量 | 优秀 | 良好 | 良好 |

---

## 总结

Anthropic SDK TypeScript 是一个**生产级、类型安全、功能完整**的 Claude API 客户端。其亮点包括：

1. **官方维护**: 由 Anthropic 团队直接维护
2. **类型优先**: TypeScript 类型定义精确完整
3. **多平台**: 支持各种 JavaScript 运行时
4. **生态丰富**: AWS/GCP/Azure 专用包
5. **流式优化**: 完善的 SSE 流处理

适合需要**稳定、安全、企业级** Claude 集成的项目。
