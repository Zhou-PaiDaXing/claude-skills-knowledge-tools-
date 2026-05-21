---
title: "/last30days Skill"
aliases: [last30days, last30days-skill]
tags:
  - opensource
  - ai-skill
  - research
github: ""
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# /last30days Skill

## 项目简介

**/last30days** 是一个 AI Agent Skill，用于跨 Reddit、X (Twitter)、YouTube、Hacker News、Polymarket 等多个平台研究任何主题。它通过聚合社交平台的真实用户互动数据（点赞、投票、评论），提供比传统搜索引擎更真实的社区观点。

- **GitHub Stars**: 21,953
- **开发语言**: Python 3.12+
- **许可证**: MIT
- **作者**: mvanhorn (@slashlast30days)

### 核心功能

- 跨平台并行搜索（Reddit、X、YouTube、TikTok、Instagram、HN、Polymarket、GitHub）
- 基于真实互动的内容评分（upvotes、likes、views）
- AI Agent 法官综合多源信息生成简报
- 智能实体解析（自动发现相关账号、社区、话题标签）
- 支持对比查询（"X vs Y"）
- 预测市场数据整合（Polymarket）

---

## 技术栈分析

### 核心语言与运行时
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 主要开发语言 |
| Node.js | 可选 | X/Twitter 搜索客户端 |
| yt-dlp | 外部依赖 | YouTube 搜索和转录 |

### 主要依赖
| 类别 | 库/工具 | 用途 |
|------|---------|------|
| API 客户端 | 自定义 | ScrapeCreators、Reddit、HN、Polymarket |
| 数据处理 | 标准库 | JSON、正则、日期处理 |
| 搜索 | yt-dlp | YouTube 内容获取 |
| 认证 | 浏览器 Cookie | X/Twitter 认证 |

### 数据源
| 平台 | 数据类型 | 认证方式 |
|------|---------|---------|
| Reddit | 帖子、评论、投票 | 公共 JSON（免费） |
| X/Twitter | 推文、互动 | 浏览器 Cookie 或 xAI API |
| YouTube | 视频、转录 | yt-dlp（免费） |
| TikTok | 视频、标题 | ScrapeCreators API |
| Instagram | Reels、标题 | ScrapeCreators API |
| Hacker News | 故事、评论 | Algolia API（免费） |
| Polymarket | 预测市场 | Gamma API（免费） |
| GitHub | Issues、PRs、用户 | gh CLI 或 API |
| Bluesky | 帖子 | App Password |
| Perplexity | AI 搜索 | OpenRouter API |

---

## 核心功能模块

### 1. 主引擎 (`scripts/last30days.py`)
- **功能**: CLI 入口和命令解析
- **特性**:
  - Python 版本检查（3.12+）
  - 子进程管理
  - 参数解析和验证
  - 输出保存和格式化

### 2. 搜索管道 (`scripts/lib/pipeline.py`)
- **功能**: 多源搜索协调
- **核心流程**:
  1. 查询计划生成（Query Plan）
  2. 并行搜索执行
  3. 结果融合和去重
  4. 聚类（Clustering）
  5. 评分和排序

### 3. 渲染引擎 (`scripts/lib/render.py`)
- **功能**: 结果格式化和输出
- **模式**:
  - `compact` - 紧凑聚类输出
  - `md` - 完整 Markdown 报告
  - `json` - JSON 结构化数据
  - `context` - 上下文模式

### 4. 实体解析 (`scripts/lib/entity_extract.py`)
- **功能**: 智能实体识别
- **解析内容**:
  - X/Twitter 账号
  - GitHub 用户名/仓库
  - Reddit 社区
  - TikTok 话题标签
  - YouTube 频道

### 5. 聚类引擎 (`scripts/lib/cluster.py`)
- **功能**: 跨源内容聚类
- **算法**: 实体感知重叠检测
- **输出**: 故事/主题聚类

### 6. 融合引擎 (`scripts/lib/fusion.py`)
- **功能**: 多源结果融合
- **策略**:
  - 加权评分
  - 去重
  - 跨源验证

### 7. 环境管理 (`scripts/lib/env.py`)
- **功能**: 配置和密钥管理
- **支持**:
  - 多平台 API 密钥
  - 浏览器 Cookie 提取
  - 配置文件管理

---

## 代码结构概览

```
last30days-skill/
├── scripts/
│   ├── last30days.py           # 主 CLI（15.8 KB）
│   ├── briefing.py             # 简报生成（8.1 KB）
│   ├── evaluate_search_quality.py  # 搜索质量评估（19.1 KB）
│   └── lib/                    # 核心库
│       ├── __init__.py
│       ├── bird_x.py           # X/Twitter 客户端（16.1 KB）
│       ├── bluesky.py          # Bluesky 集成（8.5 KB）
│       ├── chrome_cookies.py   # Chrome Cookie 提取（8.5 KB）
│       ├── cluster.py          # 聚类引擎（10.8 KB）
│       ├── cookie_extract.py   # Cookie 提取工具（13.2 KB）
│       ├── dates.py            # 日期处理（3.1 KB）
│       ├── dedupe.py           # 去重（3.2 KB）
│       ├── entity_extract.py   # 实体提取（4.1 KB）
│       ├── env.py              # 环境配置（20.4 KB）
│       ├── fusion.py           # 融合引擎（8.1 KB）
│       ├── github.py           # GitHub 集成（34.1 KB）
│       ├── hackernews.py       # HN 集成
│       ├── pipeline.py         # 搜索管道
│       ├── polymarket.py       # Polymarket 集成
│       ├── reddit.py           # Reddit 集成
│       ├── render.py           # 渲染引擎
│       ├── schema.py           # 数据模型
│       ├── search.py           # 搜索接口
│       ├── ui.py               # UI 组件
│       └── youtube.py          # YouTube 集成
├── .agents/skills/last30days/
│   └── SKILL.md                # Agent Skill 定义（78.2 KB）
├── .claude-plugin/
│   ├── marketplace.json        # Claude 插件市场配置
│   └── plugin.json             # 插件配置
├── .hermes-plugin/
│   └── SKILL.md                # Hermes 插件配置
├── docs/
│   ├── how-search-works.md     # 搜索原理文档
│   └── test-results/           # 测试结果
├── fixtures/                   # 测试数据
├── hooks/                      # Git hooks
├── assets/                     # 示例资源
├── SKILL.md                    # 主 Skill 文档（78.2 KB）
├── README.md                   # 项目说明
├── CHANGELOG.md                # 变更日志
└── pyproject.toml              # Python 项目配置
```

---

## 关键实现亮点

### 1. v3 智能搜索架构
```python
# 查询计划示例
{
  "intent": "breaking_news",
  "freshness_mode": "strict_recent",
  "cluster_mode": "story",
  "subqueries": [
    {
      "label": "primary",
      "search_query": "kanye west",
      "ranking_query": "What notable events...",
      "sources": ["reddit", "x", "youtube", "tiktok"],
      "weight": 1.0
    }
  ]
}
```

### 2. 实体解析系统
- **X Handle 解析**: WebSearch + 验证
- **GitHub 用户解析**: 人员模式 vs 项目模式
- **社区发现**: Reddit 子版块、TikTok 话题标签
- **双向关联**: 人员 <-> 公司、产品 <-> 创始人

### 3. 聚类优先输出
- 按故事/主题聚类，而非按来源
- 多源聚类 = 高置信度
- 不确定性标记（single-source、thin-evidence）

### 4. 评分算法
```python
# 多维度评分
score = f(engagement, relevance, freshness, source_weight)
# engagement: upvotes, likes, views
# relevance: 与主题匹配度
# freshness: 时间衰减
# source_weight: 平台权重
```

### 5. 跨平台对比模式
- 单遍并行查询（替代串行 3 遍）
- 实体感知子查询
- 合并结果聚类

### 6. 零配置启动
- Reddit、HN、Polymarket、GitHub 开箱即用
- X/Twitter 通过浏览器 Cookie 自动认证
- YouTube 通过 yt-dlp 免费获取

---

## 适用场景建议

### 适合的场景
1. **竞品调研** - 对比工具/产品的社区反馈
2. **人物研究** - 了解某人最近 30 天的动态
3. **趋势追踪** - 发现新兴话题和社区讨论
4. **投资研究** - 结合 Polymarket 预测市场数据
5. **内容创作** - 获取社区真实观点和引用
6. **会议准备** - 快速了解与会者背景

### 使用示例
```bash
# 基本研究
/last30days "OpenAI Codex"

# 对比查询
/last30days "Claude Code vs GitHub Copilot"

# 人物研究
/last30days "Sam Altman"

# 调整时间范围
/last30days "AI video tools" --days=7

# 深度研究
/last30days "quantum computing" --deep
```

### 安装方式
| 平台 | 命令 |
|------|------|
| Claude Code | `/plugin marketplace add mvanhorn/last30days-skill` |
| OpenClaw | `clawhub install last30days-official` |
| Manual | `git clone` to `~/.claude/skills/last30days` |

---

## 隐私与安全

### 数据访问
- 只读取公开数据
- 不发布、点赞或修改内容
- 不访问用户账号
- API 密钥不共享给第三方

### 本地存储
- 研究结果保存到 `~/Documents/Last30Days/`
- 配置文件在 `~/.config/last30days/.env`
- Cookie 实时读取，不落盘

---

## 相关链接

- **GitHub**: https://github.com/mvanhorn/last30days-skill
- **Twitter**: @slashlast30days
- **ScrapeCreators**: https://scrapecreators.com
- **Skill 文档**: `SKILL.md`（78.2 KB，详细使用指南）
