---
title: "Graphify"
aliases: [Graphify, graphify]
tags:
  - opensource
  - ai-skill
  - visualization
  - knowledge-graph
github: https://github.com/nicepkg/graphify
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Graphify

> **AI coding assistant skill — Turn any folder of code, docs, papers, images into knowledge graphs**

---

## 项目简介

Graphify 是一个 AI 编码助手技能，支持在 Claude Code、Codex、OpenCode、Cursor、Gemini CLI、Aider、OpenClaw、Factory Droid、Trae、Hermes、Kiro、Google Antigravity 等平台上运行。它能够将任何文件夹的代码、文档、论文、图片或视频转换为可查询的知识图谱，帮助开发者更快地理解代码库，发现架构决策背后的"为什么"。

**核心特点：**
- 完全多模态：支持代码、PDF、Markdown、截图、图表、白板照片、多语言图片、视频和音频
- 三阶段处理：AST 结构提取 + 音视频转录 + LLM 语义提取
- 无需嵌入：基于图拓扑的 Leiden 社区检测，无需向量数据库
- 置信度标记：每条关系标记为 EXTRACTED/INFERRED/AMBIGUOUS
- 71.5x Token 压缩：相比直接读取原始文件，查询时 Token 消耗降低 71.5 倍

**项目链接：**
- GitHub: https://github.com/safishamsi/graphify
- PyPI: https://pypi.org/project/graphifyy/
- 文档: 见 README 和 ARCHITECTURE.md

---

## 技术栈分析

### 核心技术栈
| 技术 | 用途 |
|------|------|
| Python | >= 3.10 核心运行时 |
| NetworkX | 图数据结构和算法 |
| tree-sitter | 多语言 AST 解析 |
| graspologic | Leiden 社区检测 |
| vis.js | 交互式图可视化 |

### 支持的语言 (tree-sitter)
| 语言 | 用途 |
|------|------|
| Python | 数据科学、AI |
| JavaScript/TypeScript | Web 开发 |
| Go | 云原生、后端 |
| Rust | 系统编程 |
| Java | 企业应用 |
| C/C++ | 系统编程 |
| Ruby | Web 开发 |
| C# | .NET 生态 |
| Kotlin | Android、后端 |
| Scala | 大数据 |
| PHP | Web 开发 |
| Swift | iOS/macOS |
| Lua | 游戏脚本 |
| Zig | 系统编程 |
| PowerShell | Windows 自动化 |
| Elixir | 并发应用 |
| Objective-C | iOS/macOS 传统 |
| Julia | 科学计算 |
| Verilog/SystemVerilog | 硬件设计 |
| Vue/Svelte | 前端框架 |
| Dart | Flutter |

### 可选依赖
| 功能 | 依赖 |
|------|------|
| MCP 服务器 | mcp |
| Neo4j 导出 | neo4j |
| PDF 解析 | pypdf, html2text |
| 文件监控 | watchdog |
| SVG 导出 | matplotlib |
| Office 文档 | python-docx, openpyxl |
| 视频/音频 | faster-whisper, yt-dlp |

---

## 核心功能模块

### 1. 代码提取 (`graphify/extract.py`)
- **LanguageConfig**: 语言配置数据类
- **AST 遍历**: tree-sitter 解析代码结构
- **节点提取**: 类、函数、导入、调用图
- **跨文件分析**: 跨文件的调用关系追踪
- **文档字符串提取**: 提取设计原理注释

### 2. 图构建 (`graphify/build.py`)
- **NetworkX 图**: 有向/无向图支持
- **节点合并**: 跨文件同一实体的合并
- **边类型**: 调用、导入、继承、语义相似
- **超边**: 3+ 节点的组关系

### 3. 社区检测 (`graphify/cluster.py`)
- **Leiden 算法**: 基于图拓扑的社区检测
- **无嵌入**: 直接利用图结构作为相似信号
- **层次聚类**: 多粒度社区结构

### 4. 报告生成 (`graphify/report.py`)
- **God Nodes**: 高度中心性概念识别
- **意外连接**: 跨领域关系发现
- **建议问题**: 基于图结构的问题推荐
- **置信度评分**: INFERRED 边的置信度

### 5. 导出模块 (`graphify/export.py`)
- **HTML 可视化**: vis.js 交互式图
- **JSON 格式**: 持久化图数据
- **Obsidian**: 生成 Obsidian 知识库
- **SVG/GraphML**: 矢量图和标准格式
- **Neo4j**: Cypher 导入语句

### 6. 缓存系统 (`graphify/cache.py`)
- **SHA256 缓存**: 基于文件内容的缓存
- **增量更新**: 仅处理变更文件
- **转录缓存**: 音视频转录结果缓存

### 7. 音视频处理 (`graphify/transcribe.py`)
- **faster-whisper**: 本地语音转录
- **yt-dlp**: YouTube 视频下载
- **领域感知提示**: 基于语料库生成转录提示

### 8. MCP 服务器 (`graphify/serve.py`)
- **stdio 服务器**: MCP 协议支持
- **查询接口**: query_graph, get_node, get_neighbors
- **路径查找**: shortest_path 功能

---

## 代码结构概览

```
graphify/
├── graphify/                     # 主包
│   ├── __init__.py               # 包初始化
│   ├── __main__.py               # CLI 入口 (52KB)
│   ├── extract.py                # AST 提取 (137KB)
│   ├── build.py                  # 图构建 (4KB)
│   ├── cluster.py                # 社区检测 (5KB)
│   ├── analyze.py                # 图分析 (20KB)
│   ├── report.py                 # 报告生成 (8KB)
│   ├── export.py                 # 导出功能 (39KB)
│   ├── cache.py                  # 缓存系统 (5KB)
│   ├── detect.py                 # 语言检测 (19KB)
│   ├── ingest.py                 # 内容摄取 (10KB)
│   ├── transcribe.py             # 音视频转录 (6KB)
│   ├── validate.py               # 验证 (3KB)
│   ├── watch.py                  # 文件监控 (7KB)
│   ├── wiki.py                   # Wiki 生成 (7KB)
│   ├── hooks.py                  # Git 钩子 (7KB)
│   ├── security.py               # 安全检查 (7KB)
│   ├── serve.py                  # MCP 服务器 (16KB)
│   ├── benchmark.py              # 基准测试 (5KB)
│   ├── manifest.py               # 清单 (214B)
│   └── skill.md                  # Claude 技能定义
├── tests/                        # 测试套件
│   ├── test_extract.py
│   ├── test_cluster.py
│   ├── test_export.py
│   ├── test_languages.py
│   └── ...
├── worked/                       # 示例输出
│   ├── example/                  # 示例项目
│   ├── httpx/                    # httpx 库分析
│   ├── karpathy-repos/           # Karpathy 仓库分析
│   └── mixed-corpus/             # 混合语料分析
├── pyproject.toml                # 项目配置
└── README.md                     # 项目文档
```

---

## 关键实现亮点

### 1. 三阶段处理管道
```python
# 阶段 1: AST 提取（确定性，无 LLM）
code_nodes = extract_from_ast(file_path)  # tree-sitter

# 阶段 2: 音视频转录（本地 Whisper）
transcript = transcribe_video(video_path)  # faster-whisper

# 阶段 3: LLM 语义提取（并行子代理）
concepts = extract_concepts(doc_path)  # Claude/GPT
```

### 2. 无嵌入的社区检测
```python
# graphify/cluster.py
import graspologic

# Leiden 算法直接作用于图结构
communities = graspologic.network.leiden(graph)

# 语义相似边已存在于图中
# 无需单独的向量数据库
```

### 3. 置信度标记系统
```python
# 每条边都有类型和置信度
edge = {
    "source": "node_a",
    "target": "node_b",
    "type": "semantically_similar_to",
    "confidence_tag": "INFERRED",  # EXTRACTED / INFERRED / AMBIGUOUS
    "confidence_score": 0.85
}
```

### 4. 多平台技能集成
```python
# graphify/__main__.py
_PLATFORM_CONFIG = {
    "claude": {
        "skill_file": "skill.md",
        "skill_dst": Path(".claude") / "skills" / "graphify" / "SKILL.md",
    },
    "codex": {
        "skill_file": "skill-codex.md",
        "skill_dst": Path(".agents") / "skills" / "graphify" / "SKILL.md",
    },
    # ... 支持 12+ 平台
}
```

### 5. PreToolUse 钩子（Claude/Codex）
```json
// 自动提示 AI 先读取图报告
{
  "matcher": "Glob|Grep",
  "hooks": [{
    "type": "command",
    "command": "[ -f graphify-out/graph.json ] && echo '{...graph reminder...}' || true"
  }]
}
```

### 6. SHA256 缓存机制
```python
# graphify/cache.py
def get_cache_key(file_path):
    content = file_path.read_bytes()
    return hashlib.sha256(content).hexdigest()

def load_cached(file_path):
    key = get_cache_key(file_path)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
```

---

## 适用场景建议

### 1. 新团队入职
- **场景**: 新成员快速理解大型代码库
- **优势**: 71.5x Token 压缩，结构化概览
- **使用**: `/graphify .` 生成项目图

### 2. 代码审查
- **场景**: 审查前理解代码结构和依赖
- **优势**: 可视化依赖关系，发现意外连接
- **使用**: `graphify query "show the auth flow"`

### 3. 架构决策
- **场景**: 评估重构影响，理解设计原理
- **优势**: 提取 rationale_for 节点，显示设计原因
- **使用**: 查看 GRAPH_REPORT.md 中的 "Surprising connections"

### 4. 研究文献管理
- **场景**: 整理论文、笔记、截图
- **优势**: 多模态支持，跨文档概念链接
- **使用**: `/graphify ./papers --obsidian`

### 5. 遗留代码现代化
- **场景**: 理解无文档的老代码
- **优势**: AST 提取无需文档，自动生成结构图
- **使用**: `/graphify ./legacy-code`

### 6. 会议和讲座记录
- **场景**: 录制技术讲座，提取知识
- **优势**: 本地转录，自动提取概念
- **使用**: `/graphify add <video-url>`

---

## 性能基准

| 语料库 | 文件数 | Token 压缩比 |
|--------|--------|--------------|
| Karpathy repos + 5 papers + 4 images | 52 | **71.5x** |
| graphify source + Transformer paper | 4 | **5.4x** |
| httpx (synthetic Python) | 6 | ~1x |

> 注：Token 压缩比随语料库大小增加而提升。小项目结构清晰即可，大项目节省显著。

---

## 输出示例

```
graphify-out/
├── graph.html              # 交互式可视化
├── GRAPH_REPORT.md         # 概览报告
│   ├── God nodes           # 核心概念
│   ├── Surprising connections  # 意外发现
│   └── Suggested questions # 推荐问题
├── graph.json              # 持久化图数据
└── cache/                  # SHA256 缓存
    └── <hash>.json
```

---

## 隐私说明

- **代码文件**: tree-sitter 本地处理，内容不上传
- **文档/图片**: 发送至 AI 模型 API 进行语义提取
- **视频/音频**: faster-whisper 本地转录，音频不出本机
- **无遥测**: 无使用统计、无分析追踪

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)

---

## 相关项目

- **Penpax**: graphify 的企业级扩展，持续监控整个工作生命
  - 网站: https://safishamsi.github.io/penpax.ai
  - 功能: 浏览器历史、会议、邮件、文件、代码的连续知识图谱
