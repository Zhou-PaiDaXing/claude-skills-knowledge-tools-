---
title: "MiroFish"
aliases: [MiroFish, mirofish]
tags:
  - opensource
  - ai-infrastructure
  - prediction
  - swarm-intelligence
github: https://github.com/nicepkg/mirofish
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# MiroFish 项目分析报告

## 项目概述

**MiroFish**（米洛鱼）是由盛大集团（Shanda）战略支持和孵化的开源项目，定位为"简洁通用的群体智能引擎，预测万物"。

- **GitHub Stars**: 55,163
- **主要语言**: Python (后端), JavaScript/Vue (前端)
- **许可证**: AGPL-3.0
- **愿景**: 创建映射现实的群体智能镜像，通过捕捉个体交互触发的集体涌现，突破传统预测局限

### 核心定位

MiroFish 是一个基于多智能体技术的下一代 AI 预测引擎。通过从现实世界提取种子信息（如突发新闻、政策草案或金融信号），自动构建高保真平行数字世界，让数千个具有独立人格、长期记忆和行为逻辑的智能体自由交互并经历社会演化。

---

## 技术栈分析

### 编程语言

| 语言 | 用途 | 框架/工具 |
|------|------|-----------|
| **Python** | 后端服务 | Flask, FastAPI |
| **JavaScript** | 前端交互 | Vue 3, Vite |
| **Node.js** | 构建工具 | npm, concurrently |

### 核心技术依赖

#### 后端依赖 (Python)
```python
# 来自 backend/app/__init__.py 分析
Flask                    # Web框架
Flask-CORS              # 跨域支持
Zep Cloud               # 长期记忆服务
OASIS                   # 社交模拟引擎 (CAMEL-AI)
```

#### 前端依赖 (JavaScript)
```json
{
  "vue": "^3.5.24",           // 前端框架
  "vue-router": "^4.6.3",     // 路由管理
  "vue-i18n": "^11.3.0",      // 国际化
  "axios": "^1.14.0",         // HTTP客户端
  "d3": "^7.9.0"              // 数据可视化
}
```

### 系统要求

| 组件 | 版本要求 |
|------|----------|
| Node.js | 18+ |
| Python | 3.11 - 3.12 |
| 包管理器 | uv (Python), npm (Node) |

---

## 核心功能模块

### 1. 系统架构

```
MiroFish/
├── frontend/           # Vue 3 前端
│   ├── src/
│   └── package.json
├── backend/            # Flask 后端
│   ├── app/
│   │   ├── api/       # API路由
│   │   ├── models/    # 数据模型
│   │   ├── services/  # 业务逻辑
│   │   └── utils/     # 工具函数
│   └── scripts/       # 脚本工具
└── static/            # 静态资源
```

### 2. 五大工作流程

```
┌─────────────────────────────────────────────────────────┐
│  1. Graph Building    种子提取 & 记忆注入 & GraphRAG构建  │
├─────────────────────────────────────────────────────────┤
│  2. Environment Setup 实体关系提取 & 人格生成 & Agent配置  │
├─────────────────────────────────────────────────────────┤
│  3. Simulation        双平台并行模拟 & 动态时序记忆更新     │
├─────────────────────────────────────────────────────────┤
│  4. Report Generation ReportAgent深度交互与报告生成       │
├─────────────────────────────────────────────────────────┤
│  5. Deep Interaction  与模拟世界中的Agent对话交互         │
└─────────────────────────────────────────────────────────┘
```

### 3. 核心服务模块

| 模块 | 文件路径 | 功能描述 |
|------|----------|----------|
| **模拟管理** | `services/simulation_manager.py` | 模拟生命周期管理 |
| **模拟运行器** | `services/simulation_runner.py` | 执行社交模拟 |
| **图谱构建** | `services/graph_builder.py` | 构建知识图谱 |
| **本体生成** | `services/ontology_generator.py` | 生成领域本体 |
| **报告Agent** | `services/report_agent.py` | 生成预测报告 |
| **配置生成** | `services/simulation_config_generator.py` | 模拟配置 |
| **Zep工具** | `services/zep_tools.py` | 记忆管理工具 |

### 4. API 路由

```python
# backend/app/__init__.py
app.register_blueprint(graph_bp, url_prefix='/api/graph')        # 图谱API
app.register_blueprint(simulation_bp, url_prefix='/api/simulation')  # 模拟API
app.register_blueprint(report_bp, url_prefix='/api/report')      # 报告API
```

---

## 代码结构概览

### 后端核心结构

```
backend/
├── app/
│   ├── __init__.py              # Flask应用工厂
│   ├── config.py                # 配置管理
│   ├── api/
│   │   ├── graph.py            # 图谱API (20KB)
│   │   ├── simulation.py       # 模拟API (92KB)
│   │   └── report.py           # 报告API (30KB)
│   ├── models/
│   │   ├── project.py          # 项目模型
│   │   └── task.py             # 任务模型
│   ├── services/
│   │   ├── graph_builder.py    # 图谱构建 (18KB)
│   │   ├── simulation_runner.py # 模拟运行 (68KB)
│   │   ├── simulation_manager.py # 模拟管理 (20KB)
│   │   ├── report_agent.py     # 报告生成 (97KB)
│   │   ├── ontology_generator.py # 本体生成 (19KB)
│   │   ├── zep_tools.py        # Zep工具 (65KB)
│   │   └── ...
│   └── utils/
│       ├── llm_client.py       # LLM客户端
│       ├── logger.py           # 日志工具
│       └── file_parser.py      # 文件解析
├── run.py                      # 启动入口
└── scripts/                    # 工具脚本
```

### 前端核心结构

```
frontend/
├── src/
│   ├── components/            # Vue组件
│   ├── views/                 # 页面视图
│   ├── router/                # 路由配置
│   ├── store/                 # 状态管理
│   └── api/                   # API调用
├── package.json
└── vite.config.js
```

---

## 关键实现亮点

### 1. OASIS 社交模拟引擎

基于 CAMEL-AI 的 OASIS (Open Agent Social Interaction Simulations) 项目：
- 数千个独立智能体并行交互
- 真实社交网络行为模拟
- 支持 Twitter/X、Reddit 等平台模拟

### 2. Zep Cloud 长期记忆

集成 Zep Cloud 提供：
- 实体记忆持久化
- 时序记忆更新
- 记忆检索与关联

### 3. 双平台并行模拟

```python
# 来自 simulation_runner.py 概念
class SimulationRunner:
    def run_parallel_simulation():
        # 同时在多个社交平台模拟
        twitter_sim = TwitterSimulation()
        reddit_sim = RedditSimulation()
        # 交叉影响和演化
```

### 4. GraphRAG 知识图谱

结合图数据库与RAG技术：
- 实体关系自动提取
- 本体驱动生成
- 结构化知识推理

### 5. ReportAgent 深度分析

专门设计的报告生成Agent：
- 丰富的工具集
- 与模拟后环境深度交互
- 多维度预测报告生成

---

## 适用场景建议

### 推荐场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| **舆情预测** | ★★★★★ | 公共事件发展趋势预测 |
| **政策推演** | ★★★★★ | 政策效果零风险测试 |
| **金融预测** | ★★★★☆ | 市场反应和趋势预测 |
| **创意写作** | ★★★★☆ | 小说情节推演（如红楼梦续写） |
| **公关策略** | ★★★★☆ | 危机公关预案测试 |

### 使用模式

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API keys

# 2. 一键安装
npm run setup:all

# 3. 启动服务
npm run dev
# 前端: http://localhost:3000
# 后端: http://localhost:5001
```

### Docker 部署

```bash
cp .env.example .env
docker compose up -d
```

---

## 总结

MiroFish 是一个创新的群体智能预测平台，通过构建高保真的数字孪生世界来进行"未来预演"。其核心优势在于：

**核心优势**:
- 创新的群体智能模拟方法
- 基于 OASIS 的高保真社交模拟
- 长期记忆和人格化Agent
- 可视化交互界面
- 盛大集团战略支持

**适用用户**:
- 政策制定者和公共事务决策者
- 金融分析师和风险管理者
- 内容创作者和创意工作者
- 学术研究人员

**注意事项**:
- LLM API 消耗较高，建议先进行小规模测试
- 需要配置 Zep Cloud 和 LLM API
- 大规模模拟需要充足的计算资源
