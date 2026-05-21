---
title: "Claude Code Usage Dashboard"
aliases: [Claude Usage, claude-usage]
tags:
  - opensource
  - claude-code
  - monitoring
  - Python
github: https://github.com/nicepkg/claude-usage
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Claude Code Usage Dashboard

## 项目简介

**Claude Code Usage Dashboard** 是一个本地仪表盘工具，用于追踪 Claude Code 的 Token 使用量、成本和会话历史。它读取 Claude Code 本地写入的详细使用日志，将其转换为图表和成本估算。

- **GitHub Stars**: 931
- **开发语言**: Python 3.8+
- **许可证**: MIT
- **创建者**: The Product Compass Newsletter

### 核心功能

- 扫描 Claude Code 的 JSONL 日志文件
- 计算 Token 使用量和估算成本
- 提供本地 Web 仪表盘（Chart.js 可视化）
- 支持按模型、项目、日期筛选
- 完全本地运行，无需第三方依赖

---

## 技术栈分析

### 核心语言与运行时
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 唯一开发语言 |
| SQLite | 内置 | 数据持久化 |
| http.server | 标准库 | Web 服务器 |

### 技术特点
- **零依赖**: 仅使用 Python 标准库
- **无需 pip install**: 直接运行 Python 脚本
- **无虚拟环境**: 开箱即用
- **本地 SQLite**: 数据库存储在 `~/.claude/usage.db`

### 数据来源
| 来源 | 路径 | 说明 |
|------|------|------|
| Claude Code 项目 | `~/.claude/projects/` | 主要日志位置 |
| Xcode 集成 | `~/Library/Developer/Xcode/CodingAssistant/ClaudeAgentConfig/projects/` | Xcode 用户 |

---

## 核心功能模块

### 1. 扫描器 (`scanner.py`)
- **功能**: 解析 JSONL 转录文件并写入 SQLite
- **核心特性**:
  - 增量扫描（基于文件修改时间）
  - 消息去重（基于 message.id）
  - 流式事件处理
  - 会话级统计聚合

#### 数据库 Schema
```sql
-- 会话表
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    project_name TEXT,
    first_timestamp TEXT,
    last_timestamp TEXT,
    git_branch TEXT,
    total_input_tokens INTEGER,
    total_output_tokens INTEGER,
    total_cache_read INTEGER,
    total_cache_creation INTEGER,
    model TEXT,
    turn_count INTEGER
);

-- 轮次表
CREATE TABLE turns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TEXT,
    model TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_read_tokens INTEGER,
    cache_creation_tokens INTEGER,
    tool_name TEXT,
    cwd TEXT,
    message_id TEXT
);

-- 已处理文件追踪
CREATE TABLE processed_files (
    path TEXT PRIMARY KEY,
    mtime REAL,
    lines INTEGER
);
```

### 2. 仪表盘 (`dashboard.py`)
- **功能**: HTTP 服务器 + 单页 HTML/JS 仪表盘
- **技术**: 使用 `http.server` + Chart.js（CDN）
- **特性**:
  - 自动刷新（30 秒间隔）
  - 模型筛选（URL 书签支持）
  - 时间范围筛选（7天/30天/90天/全部）
  - CSV 导出功能
  - 暗黑主题 UI

### 3. CLI (`cli.py`)
- **命令**:
  - `scan` - 扫描 JSONL 文件并更新数据库
  - `today` - 显示今日使用摘要
  - `stats` - 显示所有时间统计
  - `dashboard` - 扫描 + 启动浏览器仪表盘

---

## 代码结构概览

```
claude-usage/
├── cli.py              # 命令行入口（10.1 KB）
├── scanner.py          # JSONL 扫描器（19.4 KB）
├── dashboard.py        # Web 仪表盘（41.0 KB）
├── tests/
│   ├── test_cli.py     # CLI 测试
│   ├── test_scanner.py # 扫描器测试（26.9 KB）
│   └── test_dashboard.py # 仪表盘测试
├── docs/
│   └── screenshot.png  # 文档截图
├── .github/workflows/
│   └── tests.yml       # CI 配置
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## 关键实现亮点

### 1. 零依赖设计
```python
# 仅使用标准库
import sqlite3
import http.server
import json
import pathlib
# 无需 pip install
```

### 2. 增量扫描算法
```python
def scan():
    # 1. 检查文件修改时间
    # 2. 只处理新增或修改的文件
    # 3. 对于更新文件，只读取新增行
    # 4. 基于 message_id 去重流式事件
```

### 3. 成本计算（2026年4月 Anthropic API 定价）
| 模型 | 输入 | 输出 | Cache 写入 | Cache 读取 |
|------|------|------|-----------|-----------|
| claude-opus-4-6 | $5.00/MTok | $25.00/MTok | $6.25/MTok | $0.50/MTok |
| claude-sonnet-4-6 | $3.00/MTok | $15.00/MTok | $3.75/MTok | $0.30/MTok |
| claude-haiku-4-5 | $1.00/MTok | $5.00/MTok | $1.25/MTok | $0.10/MTok |

### 4. 前端架构
- **单文件 HTML**: 所有 CSS/JS 内嵌在 Python 字符串中
- **Chart.js**: 从 CDN 加载
- **响应式设计**: 支持移动端
- **URL 状态**: 筛选条件保存在 URL 参数中

### 5. 数据可视化
- 每日 Token 使用柱状图
- 模型分布饼图
- 项目排行横向柱状图
- 会话列表表格
- 成本统计表格

---

## 适用场景建议

### 适合的场景
1. **成本监控** - 需要了解 Claude Code 使用成本的用户
2. **使用分析** - 想分析自己在不同项目上的 AI 使用情况
3. **预算管理** - 需要控制 API 开销的开发者
4. **隐私优先** - 不想将使用数据发送到第三方服务
5. **团队报告** - 需要生成使用报告的团队

### 使用建议
```bash
# 快速开始
git clone https://github.com/phuryn/claude-usage
cd claude-usage
python3 cli.py dashboard

# 每日检查
python3 cli.py today

# 完整统计
python3 cli.py stats

# 自定义端口
HOST=0.0.0.0 PORT=9000 python3 cli.py dashboard
```

### 注意事项
- 仅统计包含 `opus`、`sonnet` 或 `haiku` 的模型
- Max/Pro 订阅用户的实际成本结构与 API 定价不同
- 不捕获 Cowork 会话（服务器端运行，无本地日志）

---

## 相关链接

- **GitHub**: https://github.com/phuryn/claude-usage
- **创建者**: https://www.productcompass.pm
- **Claude Code**: https://claude.ai/code
