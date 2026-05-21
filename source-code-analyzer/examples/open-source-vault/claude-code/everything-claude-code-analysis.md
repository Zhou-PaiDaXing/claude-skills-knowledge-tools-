---
title: "Everything Claude Code 源码分析"
aliases: [Everything Claude Code]
tags:
  - opensource
  - source-analysis
  - claude-code
  - ai-skill
  - coding-agent
github: https://github.com/affaan-m/everything-claude-code
created: 2026-04-29
updated: 2026-04-29
score: 5.1
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# affaan-m/everything-claude-code 分析报告

## 项目概览

- **类型**：AI Agent Harness 优化系统 / Claude Code 插件生态
- **技术栈**：JavaScript (Node.js) + Bash + Python + Rust (ECC 2.0 TUI) + Markdown-as-Config
- **规模**：183 Skills, 48 Agents, 79 Commands, ~204 JS 文件, ~638 MD 文件, 总代码 v1.10.0
- **核心定位**：为 Claude Code / Cursor / Codex / OpenCode 等 AI 编码助手提供生产级的 agents、skills、hooks、rules 和 MCP 配置
- **Stars**：169,390 | **License**：MIT

---

## X1 快速收集

### 项目定位（1句话）

ECC 是一套"Agent Harness 性能优化系统"，通过预定义的 agents（专家子代理）、skills（领域知识）、hooks（确定性触发器）、rules（强制约束）、commands（用户入口）五层架构，将 AI 编码助手从"裸模型"提升为具有记忆、安全、质量门控和多代理协作能力的工程系统。

### 架构图（文本）

```
                        +-----------------------+
                        |    用户 / CI / REPL    |
                        +----------+------------+
                                   |
                          /commands (79 个)
                          slash 命令入口层
                                   |
                    +--------------+--------------+
                    |                             |
              /skills (183个)              /agents (48个)
              领域知识 & 工作流            专家子代理定义
              (SKILL.md)                  (agent.md + YAML前置)
                    |                             |
                    +----------- 被引用 ----------+
                                   |
              +--------------------+--------------------+
              |                    |                     |
        /hooks (hooks.json)   /rules (16 目录)      /mcp-configs
        确定性触发器            强制约束规则           外部工具集成
        PreToolUse/Post        common/lang-specific   GitHub/Context7/
        SessionStart/End       coding-style/testing   Exa/Playwright...
              |
     scripts/hooks/ (40+ JS)
     实际 hook 执行逻辑
              |
     scripts/lib/ (30+ JS)
     共享工具库层
              |
     manifests/ (profiles/modules/components)
     选择性安装清单系统
              |
     ecc2/ (Rust TUI)          ecc_dashboard.py (Python TUI)
     下一代控制面板              当前版本仪表盘
```

### 巧妙技巧

| 想法 | 位置(file:line) | 如何复用 |
|------|-----------------|----------|
| **GateGuard Fact-Forcing**：不问"你确定吗"（LLM 永远说是），而是要求 Agent 先列出具体事实（importers、public API、data schema）才允许编辑文件。通过"调查行为"本身产生认知，而非依赖自我评估。 | `scripts/hooks/gateguard-fact-force.js:1-415` | 任何 Agent 系统都可以在工具调用前插入 fact-forcing gate，将"确认"替换为"调查" |
| **Hook Profile 三档控制**：minimal/standard/strict 三个运行时配置档位，通过 `ECC_HOOK_PROFILE` 环境变量控制 hook 启用程度，每个 hook 声明自己在哪些档位下运行 | `scripts/lib/hook-flags.js:1-75` | 适用于任何需要分级启用中间件/拦截器的系统 |
| **Plugin Root 自动发现**：hooks.json 中内联了一段 JS 引导代码，自动在多个可能路径（插件目录、marketplace 缓存、版本化目录等）中搜索 ECC 安装根目录 | `hooks/hooks.json:10` | 解决"插件安装位置不确定"的通用问题 |
| **De-Sloppify 模式**：不在实现 prompt 中加否定指令（会导致模型犹豫），而是在实现后单独运行一个清理 Agent 作为独立 pass | `skills/autonomous-loops/SKILL.md:317-376` | 任何 LLM pipeline 都可以用 "先放手做 + 后清理" 替代 "边做边限制" |
| **Instinct 置信度演化**：学习到的行为模式（instinct）有 0.3-0.9 的置信度评分，随时间和用户反馈动态升降，只有 >= 0.7 的才会自动注入 | `skills/continuous-learning-v2/SKILL.md:296-312` | 可用于任何自适应系统的特征/规则置信度管理 |
| **Session Stale-Replay Guard**：恢复上一次会话摘要时，用 "HISTORICAL REFERENCE ONLY" 包装，明确标记为"冻结的过去"，防止 LLM 重新执行过期指令 | `scripts/hooks/session-start.js:409-423` | 任何有会话持久化的 Agent 系统都需要防止"陈旧指令重放" |
| **Atomic Write 防竞态**：状态文件写入使用 temp + rename 模式，防止并发读取到半写状态 | `scripts/hooks/gateguard-fact-force.js:131-161` | 标准的文件系统原子写入模式，适用于任何多进程场景 |
| **runCommand 白名单 + 元字符拦截**：工具函数只允许 git/node/npx/which/where 前缀命令，同时拦截 shell 元字符 | `scripts/lib/utils.js:403-428` | 安全执行外部命令的最小实现 |

### 有用抽象

1. **Agent 定义格式**（`agents/*.md`）：Markdown + YAML frontmatter（name, description, tools, model）——用人类可读的 Markdown 定义 Agent 身份和能力边界，工具列表限制了 Agent 的行动空间。
   - 路径：`agents/planner.md:1-6`, `agents/loop-operator.md:1-7`

2. **Skill 定义格式**（`skills/*/SKILL.md`）：结构化的领域知识文档，包含 "When to Use" / "How It Works" / "Anti-Patterns" 等标准化章节——将最佳实践从代码中抽出，成为 Agent 的可查阅知识库。
   - 路径：`skills/verification-loop/SKILL.md`, `skills/council/SKILL.md`

3. **Hook Dispatcher Pipeline**（`scripts/hooks/bash-hook-dispatcher.js`）：将多个 Pre/Post Bash hooks 串联为一个 pipeline，每个 hook 返回 {output, stderr, exitCode}，非零退出中断后续 hooks。
   - 路径：`scripts/hooks/bash-hook-dispatcher.js:116-140`

4. **Install Manifest 系统**（`manifests/*.json`）：三层选择性安装模型——profiles（预设组合）-> modules（功能模块）-> components（用户可选粒度），支持 `--with` / `--without` 精细控制。
   - 路径：`manifests/install-profiles.json`, `manifests/install-modules.json`, `manifests/install-components.json`

5. **Cross-Platform Utils Layer**（`scripts/lib/utils.js`）：统一的跨平台工具层，封装了文件操作、session ID 管理、git 操作、stdin JSON 读取等，所有 hook 脚本共用。
   - 路径：`scripts/lib/utils.js:1-629`

### 工具/脚本精华

| 工具 | 用途 | 路径 |
|------|------|------|
| `ecc.js` | 统一 CLI 入口，子命令路由（install/plan/catalog/doctor/repair/status/sessions） | `scripts/ecc.js` |
| `claw.js` | NanoClaw REPL：零依赖的 session-aware 交互循环，Markdown-as-database | `scripts/claw.js` |
| `doctor.js` | 诊断 ECC 安装状态：检测缺失或偏移的托管文件 | `scripts/doctor.js` |
| `repair.js` | 修复偏移/缺失的 ECC 托管文件 | `scripts/repair.js` |
| `harness-audit.js` | 审计 agent harness 配置的完整性和质量 | `scripts/harness-audit.js` |
| `session-inspect.js` | 从 dmux 或 Claude 历史目标中提取标准化会话快照 | `scripts/session-inspect.js` |
| `install-plan.js` | 干运行模式查看安装计划，不实际修改文件 | `scripts/install-plan.js` |
| `ecc_dashboard.py` | 913 行的 Python TUI 仪表盘，实时展示 ECC 状态 | `ecc_dashboard.py` |
| `project-detect.js` | 自动检测项目语言和框架（13 语言 + 23 框架） | `scripts/lib/project-detect.js` |
| `plugin-hook-bootstrap.js` | Hook 引导器：解决插件根路径发现 + Node/Shell 双模式执行 | `scripts/hooks/plugin-hook-bootstrap.js` |

### 快速收获

- **低投入高价值**：
  - 学习 GateGuard Fact-Forcing 模式（`gateguard-fact-force.js`），在自己的 Agent 系统中实现"先调查后编辑"
  - 复用 Hook Profile 三档控制模式（`hook-flags.js`），为中间件系统添加分级启用能力
  - 采用 De-Sloppify 两阶段模式替代单步约束
  - 复制 Session Stale-Replay Guard 设计到任何有会话恢复功能的 Agent

- **中等投入好价值**：
  - 建立类似的 Agent/Skill/Rule 三层知识管理体系（Markdown-as-Config 范式）
  - 实现选择性安装系统（profiles -> modules -> components）
  - 搭建类似的 Hook Pipeline 架构（PreToolUse/PostToolUse 拦截链）

- **高投入高价值**：
  - 构建完整的 Continuous Learning 系统（instinct 观察 -> 提取 -> 置信度演化 -> 技能进化）
  - 实现多 Agent 编排系统（RFC-DAG / worktree 隔离 / merge queue）
  - 移植整套 cross-harness 适配层（Claude/Cursor/Codex/OpenCode 统一安装面）

---

## T1 架构模式分析

### 架构风格识别

ECC 采用的是**"声明式配置 + 确定性拦截 + 概率性推理"混合架构**：

1. **声明式配置层**：agents/skills/rules/commands 全部是 Markdown 文件，用声明式方式定义"Agent 是什么"、"何时使用"、"如何工作"。这些文件不是代码，而是给 LLM 读的"配置"。
   - 路径：`agents/*.md`, `skills/*/SKILL.md`, `rules/**/*.md`

2. **确定性拦截层**：hooks 系统是纯 JavaScript，通过 PreToolUse/PostToolUse/SessionStart/SessionEnd 等事件确定性触发（100% 可靠），实现质量门控、安全检查、会话管理等功能。
   - 路径：`hooks/hooks.json`, `scripts/hooks/*.js`

3. **概率性推理层**：实际的编码、规划、审查工作由 LLM（Claude Opus/Sonnet）完成，Agent 定义只是引导 LLM 的 prompt。

**核心设计哲学**：将"确定性必须做对的事情"（安全检查、状态管理、文件操作）放在 hooks（Node.js 代码）中；将"需要智能判断的事情"（代码审查、规划、重构）放在 agents/skills（Markdown prompt）中。

### 模块边界

| 模块 | 职责 | 边界定义 | 依赖方向 |
|------|------|----------|----------|
| `agents/` | 48 个专家子代理的身份定义 | 每个 `.md` 文件定义一个 Agent 的角色、工具、模型 | 被 commands 和 AGENTS.md 引用 |
| `skills/` | 183 个领域知识与工作流 | 每个目录下 `SKILL.md` 定义一个技能 | 被 agents 和 commands 引用 |
| `commands/` | 79 个用户入口命令 | 每个 `.md` 定义一个 slash command | 委托给 agents + skills |
| `hooks/` | 确定性事件拦截 | `hooks.json` 声明 matcher + 命令 | 调用 scripts/hooks/ |
| `scripts/hooks/` | Hook 执行逻辑 | 每个 `.js` 实现一个具体检查 | 依赖 scripts/lib/ |
| `scripts/lib/` | 共享工具库 | 平台抽象、文件操作、安装逻辑 | 无外部依赖（仅 Node.js stdlib） |
| `manifests/` | 安装元数据 | profiles/modules/components JSON | 被 install-plan/install-apply 读取 |
| `rules/` | 强制约束 | 按 common + 语言分目录 | 被 Agent 运行时隐式加载 |
| `mcp-configs/` | MCP 服务配置 | 外部工具集成声明 | 被安装器复制到目标 |
| `ecc2/` | Rust TUI 控制面板（alpha） | 独立 Cargo 项目 | 读取 SQLite 状态存储 |

### 架构图

```
User Layer (Commands)
  |
  |  /tdd  /plan  /code-review  /verify  /learn  ...
  |
  v
Agent Orchestration Layer
  |
  |  planner -> architect -> tdd-guide -> code-reviewer
  |  security-reviewer -> build-error-resolver -> loop-operator
  |
  v                                v
Skill Knowledge Layer          Hook Interception Layer
  |                                |
  | tdd-workflow                   | PreToolUse: gateguard, config-protection,
  | verification-loop              |   block-no-verify, bash-quality
  | continuous-learning-v2         | PostToolUse: format, typecheck,
  | autonomous-loops               |   console-warn, edit-accumulator
  | council                        | SessionStart: context-load, instinct-inject
  | agent-harness-construction     | SessionEnd: session-save, observer-stop
  |                                | PreCompact: session-snapshot
  v                                v
Rules Layer                    Scripts/Lib Layer
  |                                |
  | common/coding-style.md         | utils.js (cross-platform)
  | common/testing.md              | hook-flags.js (profile control)
  | typescript/patterns.md         | project-detect.js (auto-detect)
  | python/style.md                | install-manifests.js (install logic)
  | ...                            | session-manager.js
  v                                v
MCP Layer                      Install/State Layer
  |                                |
  | GitHub, Context7, Exa,         | manifests/ (profiles/modules/components)
  | Playwright, Memory,            | install-state.json (tracking)
  | Sequential Thinking            | SQLite state store
```

### 扩展点

1. **新增 Agent**：添加 `agents/<name>.md`，YAML frontmatter 定义工具和模型，无需修改任何代码
   - 路径模式：`agents/*.md`

2. **新增 Skill**：添加 `skills/<name>/SKILL.md`，自动被 catalog 发现
   - 路径模式：`skills/*/SKILL.md`

3. **新增 Hook**：在 `scripts/hooks/` 添加 JS 文件，在 `hooks/hooks.json` 注册 matcher
   - 注册点：`hooks/hooks.json`

4. **新增安装目标**：在 `scripts/lib/install-targets/` 添加 adapter
   - 路径：`scripts/lib/install-targets/registry.js`

5. **新增语言支持**：在 `rules/<language>/` 添加规则，在 `scripts/lib/project-detect.js` 添加检测规则
   - 路径：`scripts/lib/project-detect.js:17-83`

6. **新增安装模块**：在 `manifests/install-modules.json` 添加模块定义
   - 路径：`manifests/install-modules.json`

7. **新增 MCP 服务**：在 `mcp-configs/mcp-servers.json` 添加配置
   - 路径：`mcp-configs/mcp-servers.json`

### 权衡分析

| 决策 | 收益 | 代价 |
|------|------|------|
| **Markdown-as-Config 范式**（Agent/Skill/Rule 全部用 Markdown 定义） | 极低学习门槛、人类可读可编辑、LLM 原生理解、社区贡献友好 | 缺乏类型安全、无法做编译时校验、运行时行为完全依赖 LLM 对 prompt 的理解 |
| **Hook 系统用 Node.js 实现**（非 shell 脚本） | 跨平台（Windows/macOS/Linux）、可测试、可组合、有丰富的标准库 | 需要 Node.js >= 18 运行时、每次 hook 调用有进程启动开销（通过 `run-with-flags.js` 的 require() 优化缓解） |
| **Skills-first 迁移**（从 commands 迁向 skills） | 更丰富的上下文（When to Use/Anti-Patterns 等）、不受 slash command 格式限制 | 需要维护旧 command shims 的向后兼容、迁移期间有两套入口 |
| **选择性安装**（profiles + modules + components） | 用户可精确控制安装内容、减少不需要的上下文噪声 | 安装系统复杂度高（三层元数据 + adapter 适配层 + 状态跟踪） |
| **极少的运行时依赖**（仅 3 个：@iarna/toml, ajv, sql.js） | 供应链攻击面极小、安装快、无版本冲突 | 所有工具函数需手写（utils.js 629 行） |
| **多 Harness 适配**（Claude/Cursor/Codex/OpenCode/Gemini/CodeBuddy/Antigravity） | 一套配置适配多个 AI 编码工具 | 适配层维护成本高、每个目标的行为差异需要持续跟踪 |
| **Continuous Learning 使用 Hooks 而非 Skills**（v2 vs v1） | 100% 确定性触发 vs 50-80% 概率触发 | 更复杂的 hook 管理、需要后台 observer 进程 |

---

## A1 Agent 架构分析

### Agent 核心架构

ECC 的 Agent 系统是一种**"声明式 Agent 配置 + 宿主 LLM 执行"架构**。Agent 本身不包含可执行代码，而是定义了 LLM 应该扮演的角色、可使用的工具、应遵循的流程。

**Agent 定义结构**（`agents/*.md`）：
```yaml
---
name: agent-name
description: 何时应该调用此 Agent（一句话）
tools: ["Read", "Grep", "Glob", "Bash", "Edit"]  # 工具白名单
model: opus|sonnet  # 模型路由
color: teal  # 可选的 UI 颜色
---
（Markdown 格式的角色定义 + 工作流 + 约束）
```

关键设计：
- **工具白名单**限制了 Agent 的行动空间（例如 planner 只有 Read/Grep/Glob，不能 Edit/Write）
  - 路径：`agents/planner.md:5` -> `tools: ["Read", "Grep", "Glob"]`
- **模型路由**根据任务复杂度选择模型（Opus 做深度推理，Sonnet 做快速执行）
  - 路径：`agents/planner.md:6` -> `model: opus`; `agents/loop-operator.md:6` -> `model: sonnet`
- **角色提示**定义了详细的工作流程（如 code-reviewer 的分级检查清单：CRITICAL -> HIGH -> MEDIUM -> LOW）
  - 路径：`agents/code-reviewer.md:32-174`

### 决策机制

ECC 的决策在三个层面发生：

**1. Agent 路由决策**（AGENTS.md 中声明）：
```
复杂功能请求 -> planner
代码刚写完 -> code-reviewer
Bug 修复/新功能 -> tdd-guide
架构决策 -> architect
安全敏感代码 -> security-reviewer
自主循环 -> loop-operator
```
- 路径：`AGENTS.md:48-56`

**2. Hook 拦截决策**（确定性规则）：
- GateGuard：首次编辑文件 -> 强制调查 -> 重试后放行
  - 路径：`scripts/hooks/gateguard-fact-force.js:346-413`
- Config Protection：尝试修改 linter/formatter 配置 -> 阻止并引导修复代码
  - 路径：`scripts/hooks/config-protection.js`
- Block No-Verify：尝试 `git commit --no-verify` -> 拦截
  - 路径：`scripts/hooks/block-no-verify.js`
- MCP Health Check：MCP 工具调用前检查服务健康状态
  - 路径：`scripts/hooks/mcp-health-check.js`

**3. Council 多声部决策**（处理歧义场景）：
- 4 个独立声音：Architect（正确性）+ Skeptic（前提挑战）+ Pragmatist（实用性）+ Critic（风险）
- 三个外部声音作为独立子代理启动，不共享对话历史（反锚定机制）
- 路径：`skills/council/SKILL.md:1-204`

### 工具系统

**内置工具**（Claude Code 原生）：Read, Write, Edit, MultiEdit, Grep, Glob, Bash

**MCP 外部工具**（`.mcp.json`）：
| 工具 | 用途 |
|------|------|
| GitHub MCP | 仓库操作、PR、Issues |
| Context7 | 文档查询（最新 API 文档） |
| Exa | 网页搜索 |
| Memory MCP | 持久化记忆 |
| Playwright | 浏览器自动化测试 |
| Sequential Thinking | 结构化推理 |

- 路径：`.mcp.json:1-28`

**Hook 系统作为"隐式工具"**：
- Pre-Bash Dispatcher 串联了 6 个前置检查（block-no-verify, auto-tmux, tmux-reminder, git-push-reminder, commit-quality, gateguard）
  - 路径：`scripts/hooks/bash-hook-dispatcher.js:18-48`
- Post-Bash Dispatcher 串联了 4 个后置动作（command-log-audit, command-log-cost, pr-created, build-complete）
  - 路径：`scripts/hooks/bash-hook-dispatcher.js:50-69`

### 记忆系统

ECC 的记忆系统是三层的：

**1. Session Memory**（短期）：
- SessionStart hook 自动加载最近 7 天的会话摘要
- 匹配策略：精确 worktree 匹配 > 项目名匹配 > 最新可用
- 路径：`scripts/hooks/session-start.js:155-208`
- SessionEnd hook 保存当前会话摘要
- PreCompact hook 在上下文压缩前捕获快照
- 过期清理：默认保留 30 天，自动裁剪

**2. Instinct Memory**（中期/持久）：
- 通过 PreToolUse/PostToolUse hooks 观察每次工具使用
- 后台 observer agent（Haiku 模型）分析观察数据，提取模式
- 项目作用域隔离：基于 git remote URL hash 分隔不同项目的 instinct
- 置信度演化：0.3（试探性）-> 0.5（中等）-> 0.7（强，自动应用）-> 0.9（核心行为）
- 路径：`skills/continuous-learning-v2/SKILL.md:46-127`
- 存储结构：`~/.claude/homunculus/projects/<hash>/instincts/`

**3. Knowledge/Skill Memory**（长期）：
- 通过 `/evolve` 命令将相关 instincts 聚类成 skills/commands/agents
- 通过 `/promote` 将项目级 instinct 提升为全局级（需在 2+ 项目中出现且平均置信度 >= 0.8）
- 存储结构：`~/.claude/homunculus/evolved/` 和 `~/.claude/skills/learned/`
- 路径：`skills/continuous-learning-v2/SKILL.md:268-288`

### 多 Agent 协作

ECC 支持多种多 Agent 协作模式：

**1. 顺序委托**（最常见）：
```
用户请求 -> planner（规划）-> tdd-guide（实现）-> code-reviewer（审查）
```

**2. 并行独立执行**：
- AGENTS.md 明确指出"Use parallel execution for independent operations"
- 路径：`AGENTS.md:57`

**3. RFC-DAG 编排**（Ralphinho 模式）：
- 将规格说明分解为工作单元依赖图
- 每层并行执行，层间串行
- 每个单元经过 Research -> Plan -> Implement -> Test -> Review 流水线
- 独立 worktree 隔离 + merge queue（带驱逐和冲突恢复）
- 路径：`skills/autonomous-loops/SKILL.md:379-531`

**4. 四声部 Council**（决策场景）：
- 4 个独立声音并行执行，最后综合
- 路径：`skills/council/SKILL.md:84-110`

**5. Infinite Agentic Loop**（批量生成）：
- 编排器分析规格 + 分配创意方向 -> 并行部署 N 个子 Agent
- 路径：`skills/autonomous-loops/SKILL.md:142-208`

**6. Continuous PR Loop**（持续集成）：
- 循环：创建分支 -> claude -p 实现 -> 可选 reviewer pass -> 提交 -> PR -> 等 CI -> 自动修复 -> 合并
- 路径：`skills/autonomous-loops/SKILL.md:211-314`

### 执行循环

ECC 的核心执行循环：

```
SessionStart Hook
  -> 加载最近会话摘要
  -> 注入高置信度 instincts
  -> 检测项目类型
  -> 注册 observer lease
  |
  v
PreToolUse Hooks (每次工具调用前)
  -> GateGuard: 首次编辑? -> 强制调查
  -> Config Protection: 修改配置? -> 阻止
  -> MCP Health Check: MCP 调用? -> 检查健康
  -> Observe: 记录工具使用(async, 10ms timeout)
  -> Governance Capture: 记录治理事件
  |
  v
Agent 执行 (LLM 推理 + 工具调用)
  -> 根据任务类型路由到专家 Agent
  -> Agent 使用白名单内的工具执行任务
  -> Skills 提供领域知识引导
  -> Rules 强制编码风格和安全约束
  |
  v
PostToolUse Hooks (每次工具调用后)
  -> Format: 自动格式化修改的文件
  -> TypeCheck: 增量类型检查
  -> Console Warn: 检测 console.log
  -> Edit Accumulator: 累计编辑统计
  -> Build Complete: 检测构建完成通知
  |
  v
PreCompact Hook (上下文压缩前)
  -> 捕获会话快照
  -> 保存到 session-data 目录
  |
  v
SessionEnd Hook
  -> 保存会话摘要
  -> 移除 observer lease
  -> 停止 observer(当无 lease 时)
```

---

## 综合评分

| 维度 | 评分(1-10) | 亮点 | 可改进 |
|------|------------|------|--------|
| **架构设计** | 9 | 声明式配置 + 确定性拦截的混合架构非常精巧，将"该用代码做的"和"该用 prompt 做的"分得很清 | ecc2 (Rust TUI) 仍是 alpha，与主系统的集成尚不完整 |
| **代码质量** | 8 | 跨平台工具库实现扎实、错误处理全面、安全意识强（命令白名单、路径遍历防护） | hooks.json 中的内联 JS 引导代码可读性很差（单行压缩的路径发现逻辑） |
| **扩展性** | 10 | 新增 Agent/Skill/Rule/Command 几乎零摩擦（只需添加 Markdown 文件），选择性安装系统支持精细控制 | 安装适配层复杂度随目标增加而线性增长 |
| **Agent 设计** | 9 | 工具白名单限制行动空间、模型路由分级、fact-forcing 替代确认、author-bias 消除（审查者非作者）| 48 个 Agent 之间的路由完全依赖 LLM 判断，无确定性路由层 |
| **记忆系统** | 9 | 三层记忆（session/instinct/skill）设计完整，项目作用域隔离，置信度演化机制精巧 | observer agent 需要后台进程，增加运维复杂度 |
| **安全性** | 9 | runCommand 白名单+元字符拦截、config-protection、block-no-verify、path-traversal 防护、secrets-check | 部分安全检查依赖正则匹配（如破坏性命令检测），可能被绕过 |
| **文档** | 9 | 70KB README + 多语言翻译 + 专门的安全指南/长文指南/短文指南 + 每个 skill 有标准化文档 | WORKING-CONTEXT.md 过于面向维护者，新用户难以快速上手 |
| **可维护性** | 7 | 测试覆盖 80%+、CI 验证全面（unicode 安全、agent 验证、hook 验证、skill 验证） | 183 个 skills 的质量参差不齐，部分仍需审计；command/skill 双入口的迁移中状态增加认知负担 |

---

## 核心收获

### 最值得借鉴的 3 个设计决策

1. **"确定性拦截 + 概率推理"分离**：将安全检查、状态管理等"必须做对"的事情放在 hooks（Node.js 代码，100% 触发），将代码审查、规划等"需要智能"的事情放在 agents/skills（Markdown prompt，由 LLM 执行）。这避免了要么全靠代码（无法处理模糊场景）要么全靠 LLM（安全不可靠）的两难困境。
   - 关键文件：`hooks/hooks.json`, `scripts/hooks/bash-hook-dispatcher.js`, `agents/code-reviewer.md`

2. **Fact-Forcing 替代 Confirmation**：GateGuard 不问"你确定吗"（LLM 永远说是），而是要求 Agent 列出具体事实。这一设计认识到 LLM 的核心弱点——自我评估不可靠，但信息搜集能力强——并巧妙地将"确认"转化为"调查"。
   - 关键文件：`scripts/hooks/gateguard-fact-force.js`

3. **Instinct 置信度演化模型**：将学习到的模式赋予量化置信度（0.3-0.9），随观察累积和用户反馈动态调整，结合项目作用域隔离和跨项目提升机制。这比简单的"全学/全不学"或"一次学习永远有效"都更精细。
   - 关键文件：`skills/continuous-learning-v2/SKILL.md`

### 最值得学习的 3 个代码模式

1. **Hook Pipeline 串联模式**：`bash-hook-dispatcher.js` 将多个独立检查函数串联为 pipeline，每个返回标准化结果 `{output, stderr, exitCode}`，非零退出中断后续 hooks。支持 `run()` 函数导出（同进程 require，省 ~50-100ms）和 legacy spawnSync 两种执行路径。
   - 路径：`scripts/hooks/bash-hook-dispatcher.js:116-140`, `scripts/hooks/run-with-flags.js:119-147`

2. **跨平台安全命令执行**：`utils.js` 的 `runCommand()` 实现了命令前缀白名单 + shell 元字符拦截 + 引号内容豁免的三层安全策略，既保证了安全性又不过度限制功能。
   - 路径：`scripts/lib/utils.js:403-428`

3. **Session 匹配策略**：`session-start.js` 的 `selectMatchingSession()` 实现了三级降级匹配（精确 worktree -> 项目名 -> 最新可用），单次遍历中同时缓存文件内容避免重复 IO，并用 `realpathSync` 处理符号链接和大小写不敏感文件系统。
   - 路径：`scripts/hooks/session-start.js:155-208`

### 最值得复用的 3 个工具/脚本

1. **`scripts/lib/project-detect.js`**：自动检测 13 种语言 + 23 种框架的项目类型检测器，通过 marker 文件 + 依赖包名两路检测，支持 npm/pip/go.mod/Cargo.toml/composer/mix.exs 六种包管理器解析。可以直接复用到任何需要项目类型识别的工具中。
   - 路径：`scripts/lib/project-detect.js`（434 行）

2. **`scripts/hooks/gateguard-fact-force.js`**：完整的 "fact-forcing gate" 实现，包含 session 状态管理、原子写入、路径注入防护、分级门控（Edit/Write/Bash-destructive/Bash-routine）。可以直接移植到任何 Agent 系统的工具调用前拦截层。
   - 路径：`scripts/hooks/gateguard-fact-force.js`（416 行）

3. **`scripts/lib/utils.js`**：零外部依赖的跨平台工具库，包含文件操作、session 管理、git 操作、stdin JSON 读取、ANSI 转义清理等。任何 Node.js CLI 工具都可以复用其中的函数。
   - 路径：`scripts/lib/utils.js`（629 行）

---

## 推荐学习路径

1. **先读** -> `CLAUDE.md`（项目架构概览）+ `AGENTS.md`（Agent 清单和编排规则）+ `SOUL.md`（核心原则）+ `RULES.md`（格式约束）。这四个文件在 30 分钟内可以建立对项目的全局理解。
   - 路径：`/CLAUDE.md`, `/AGENTS.md`, `/SOUL.md`, `/RULES.md`

2. **再看** -> Hook 系统（确定性拦截层），按以下顺序：
   - `hooks/hooks.json`（所有 hook 注册声明，理解"拦截了什么"）
   - `scripts/hooks/plugin-hook-bootstrap.js`（引导器，理解"如何执行"）
   - `scripts/hooks/run-with-flags.js`（flag 控制器，理解"条件执行"）
   - `scripts/hooks/bash-hook-dispatcher.js`（pipeline 模式，理解"如何串联"）
   - `scripts/hooks/gateguard-fact-force.js`（fact-forcing 核心，理解"最精巧的设计"）
   - `scripts/hooks/session-start.js`（会话恢复，理解"记忆加载"）

3. **最后研究** -> 高级 Agent 协作模式和记忆系统：
   - `skills/autonomous-loops/SKILL.md`（6 种循环模式的完整图谱，从简单到复杂）
   - `skills/continuous-learning-v2/SKILL.md`（instinct 记忆系统的完整设计）
   - `skills/council/SKILL.md`（多声部决策模式）
   - `skills/agent-harness-construction/SKILL.md`（Agent 系统设计的元技能）
   - `manifests/install-profiles.json` + `manifests/install-modules.json`（选择性安装的设计模式）
   - `ecc2/Cargo.toml`（Rust TUI 控制面板，了解 ECC 2.0 的方向）
