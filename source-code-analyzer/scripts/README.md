---
title: README
created: 2026-05-20
tags: [scripts]
---

# source-code-analyzer / scripts

## detect_stack.sh

检测项目栈,输出标准 JSON 给步骤 2 的维度推荐消费。

### 用法

```bash
./scripts/detect_stack.sh /path/to/project
# 或在项目根目录直接
cd /path/to/project && /path/to/skill/scripts/detect_stack.sh
```

### 输出示例

```json
{
  "languages": ["typescript", "python"],
  "frameworks": ["nextjs", "react", "ai-stack"],
  "type": "ai",
  "scale": "large",
  "file_count": 1234
}
```

### 探测范围

| 维度 | 检测依据 |
|---|---|
| 语言 | package.json/tsconfig/go.mod/Cargo.toml/requirements.txt/pom.xml/build.gradle/Package.swift/build.sbt/Gemfile/composer.json/*.csproj |
| 构建系统 | WORKSPACE/Makefile/CMakeLists/.bazelrc |
| Monorepo | pnpm-workspace/nx.json/turbo.json/lerna.json/Cargo workspace/Maven multi-module/Gradle multi-project |
| 移动端 | android+ios 目录/AndroidManifest/Podfile |
| AI | openai/anthropic/langchain/llamaindex/chromadb/pinecone/weaviate 关键词 |
| 规模 | 文件总数 (排除 node_modules/.git/target/build) |
