---
title: "OpenCode 源码分析"
aliases: [OpenCode, opencode]
tags:
  - opensource
  - source-analysis
  - coding-agent
  - TypeScript
  - terminal-ui
github: https://github.com/anomalyco/opencode
created: 2026-04-27
updated: 2026-04-27
score: 5.5
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# anomalyco/opencode 分析报告

## 项目概览
- 类型：开源 AI 编程助手（Coding Agent），终端优先，支持桌面和 Web
- 技术栈：TypeScript + Bun Runtime + Effect-TS (函数式effect系统) + Vercel AI SDK + Hono (HTTP) + SolidJS (UI) + Drizzle ORM (SQLite) + tree-sitter
- 规模：核心包 `packages/opencode` 约 360 个 TypeScript 文件、68,000+ 行代码；整个 monorepo 约 1,111 个 TypeScript 文件
- 架构：Client/Server 分离、Monorepo (Bun workspaces + Turbo)、Event-Sourced 状态管理
- Stars: 151,415 | License: MIT | 版本: v1.14.29

---

## X1 快速收集

### 项目定位（1句话）
OpenCode 是一个 provider-agnostic、终端优先的开源 AI 编程 Agent，采用 client/server 架构，支持 TUI/桌面/Web/移动端多前端驱动同一 Agent 后端。

### 架构图（文本）
```
                        +-----------+     +-----------+     +---------+
                        |  TUI CLI  |     | Desktop   |     |  Web    |
                        |  (SolidJS)|     | (Electron)|     | (Solid) |
                        +-----+-----+     +-----+-----+     +----+----+
                              |                 |                  |
                              +--------+--------+---------+--------+
                                       |  WebSocket / HTTP (Hono)  |
                                       |     Server (server.ts)    |
                                       +-----------+---------------+
                                                   |
                          +------------------------+---------------------------+
                          |                        |                           |
                 +--------v--------+     +---------v---------+     +-----------v-----------+
                 |  Session Layer  |     |   Agent Layer      |     |  Provider Layer       |
                 |  (processor.ts  |     |   (agent.ts)       |     |  (provider.ts)        |
                 |   llm.ts        |     |   build/plan/      |     |  20+ AI SDK providers |
                 |   compaction.ts)|     |   general/explore  |     |  models.dev database  |
                 +--------+--------+     +---------+----------+     +-----------+-----------+
                          |                        |                            |
                 +--------v--------+     +---------v----------+     +-----------v-----------+
                 |  Tool Registry  |     |  Permission System |     |  Plugin System         |
                 |  (registry.ts)  |     |  (permission/)     |     |  (plugin/)             |
                 |  15+ builtin    |     |  wildcard rules    |     |  hooks + auth + tools  |
                 |  + MCP + custom |     |  ask/allow/deny    |     |  npm packages          |
                 +-----------------+     +--------------------+     +-----------------------+
                          |
            +-------------+------------------+------------------+
            |             |                  |                  |
     +------v---+  +------v------+  +--------v-----+  +--------v-------+
     | Bash/PTY |  | Edit/Write  |  | Grep/Glob/   |  | Task (subagent)|
     | (pty.ts) |  | (edit.ts)   |  | Read/Search  |  | Skill/MCP      |
     +----------+  +-------------+  +--------------+  +----------------+
                          |
                 +--------v--------+     +-------------------+
                 |  Snapshot (git) |     |  Bus (Event)      |
                 |  track/patch/   |     |  PubSub + Global  |
                 |  restore/revert |     |  sync events      |
                 +-----------------+     +-------------------+
                          |
                 +--------v--------+
                 |  Storage (SQLite)|
                 |  Drizzle ORM    |
                 |  SyncEvent      |
                 +-----------------+
```

### 巧妙技巧
| 想法 | 位置(file:line) | 如何复用 |
|------|-----------------|----------|
| **Provider-specific 系统提示**: 根据 model API ID 自动选择不同系统提示（anthropic/gpt/gemini/kimi/trinity），最大化各模型能力 | `packages/opencode/src/session/system.ts:19-33` | 在任何多 LLM 项目中使用 model-aware prompt routing |
| **InstanceState 缓存模式**: 用 Effect `ScopedCache` 实现按 working directory 隔离的状态缓存，每个实例独立生命周期，自动失效 | `packages/opencode/src/effect/instance-state.ts:38-59` | 任何需要多项目/多租户隔离状态的 CLI 工具 |
| **Doom Loop 检测**: 连续 3 次相同 tool 调用+相同参数自动触发 permission 询问，防止 agent 陷入死循环 | `packages/opencode/src/session/processor.ts:305-330` | 任何 agent 框架的安全护栏 |
| **Tool call 自动修复**: LLM 返回大小写不匹配的 tool name 时自动 lowercase 修复，失败则路由到 `invalid` 工具返回结构化错误 | `packages/opencode/src/session/llm.ts:339-358` | 提升所有 LLM tool calling 的鲁棒性 |
| **SSE chunk timeout**: 自定义 fetch wrapper 为 SSE 流中每个 chunk 设置独立超时，防止连接卡死 | `packages/opencode/src/provider/provider.ts:40-86` | 任何流式 API 客户端 |
| **Git-based Snapshot**: 用 shadow git repo 跟踪 Agent 对文件系统的每个修改步骤，支持 track/patch/restore/revert | `packages/opencode/src/snapshot/index.ts:1-58` | 可逆的文件变更管理 |
| **SyncEvent 事件溯源**: 状态变更通过 event 驱动写入 SQLite 并投影到表，提供 event/projector 分离 | `packages/opencode/src/sync/index.ts:1-60` | Event Sourcing 轻量实现 |
| **LiteLLM 兼容**: 检测 proxy 场景自动注入 noop tool 避免 API 校验失败 | `packages/opencode/src/session/llm.ts:200-228` | 适配各种 LLM proxy 网关 |
| **智能 Compaction**: token overflow 时自动生成 anchored summary、保留最近 N 轮对话的 tail、可增量更新 | `packages/opencode/src/session/compaction.ts:40-75` | 长对话 context 管理 |
| **Tool output truncation + 落盘**: 过长工具输出截断并写入临时文件，agent 可通过 read 工具按需获取完整内容 | `packages/opencode/src/tool/tool.ts:110-127` | 大输出的优雅处理 |

### 有用抽象
1. **Tool.define()** (`packages/opencode/src/tool/tool.ts:130-148`): 统一的工具定义 DSL，自动处理 schema validation、output truncation、span tracing。通过 Effect 管道组合，工具只需关注业务逻辑。
2. **Permission.Ruleset** (`packages/opencode/src/permission/index.ts:26-37`): 基于 wildcard pattern 的分层权限模型 (allow/deny/ask)，支持 tool 级、path 级、agent 级细粒度配置。
3. **BusEvent.define()** (`packages/opencode/src/bus/bus-event.ts:12-19`): 类型安全的事件定义系统，自动注册到全局 registry，配合 zod schema 自动生成 OpenAPI payload。
4. **SyncEvent** (`packages/opencode/src/sync/index.ts`): Event Sourcing 抽象，定义 event type + projector 函数，自动持久化到 SQLite 并投影到对应表。
5. **InstanceState.make()** (`packages/opencode/src/effect/instance-state.ts:38`): 基于 working directory 的 scoped 状态缓存，在多项目场景中自动隔离和生命周期管理。

### 工具/脚本精华
1. **install script** (`/install`, 13,690 行): 完整的跨平台安装脚本，支持 `$OPENCODE_INSTALL_DIR` / `$XDG_BIN_DIR` / `$HOME/bin` / `$HOME/.opencode/bin` 优先级
2. **fix-node-pty** (`packages/opencode/script/fix-node-pty.ts`): 自动修复 node-pty 跨平台兼容问题
3. **build.ts** (`packages/opencode/script/build.ts`): Bun 打包脚本
4. **Nix flake** (`flake.nix`): 完整的 Nix 构建支持
5. **JSON->SQLite Migration** (`packages/opencode/src/storage/json-migration.ts`): 带进度条的一次性数据迁移

### 快速收获
- :green_circle: 低投入高价值：借鉴 Doom Loop 检测模式（3 次相同调用触发中断）—— 10 行代码即可实现的 agent 安全护栏
- :green_circle: 低投入高价值：Tool call 自动修复策略（lowercase + invalid fallback）—— 显著降低 tool calling 错误率
- :green_circle: 低投入高价值：Provider-specific 系统提示路由 —— 每个模型用最适合的 prompt 格式
- :yellow_circle: 中等投入好价值：Permission wildcard ruleset 系统 —— 通用的 agent 权限控制框架
- :yellow_circle: 中等投入好价值：Compaction 机制（anchored summary + tail preservation）—— 长对话 context 管理的工业级方案
- :red_circle: 高投入高价值：Event Sourcing (SyncEvent) + Instance State 架构 —— 适合需要多租户、事件驱动的 agent 系统

---

## T1 架构模式分析

### 架构风格识别
**分层式 + 事件驱动 + 依赖注入 (Effect-TS Layers)**

核心架构特征：
1. **Effect-TS 作为 DI 骨架**: 所有核心服务（Agent, Session, Provider, Tool, Permission, Bus, MCP 等）都定义为 `Context.Service`，通过 `Layer.effect` 构建，形成显式的依赖图。这替代了传统的 DI 容器或 service locator。
2. **Event Sourcing 数据层**: 状态变更通过 `SyncEvent.run()` 写入 event log，projector 函数将事件投影到 Drizzle ORM 表。Bus 系统实时分发事件给订阅者。
3. **Client/Server 分离**: 后端是 Hono HTTP/WebSocket 服务器，前端（TUI/Desktop/Web）通过统一 SDK 交互。一个后端可服务多个前端。
4. **Stream-based LLM 处理**: AI SDK 的 `streamText` 结果通过 Effect `Stream` 处理，实现取消、重试、错误处理的统一管道。

### 模块边界
| 模块 | 路径 | 职责 | 对外接口 |
|------|------|------|----------|
| **Agent** | `src/agent/` | 定义 agent 类型及配置（build/plan/general/explore/compaction/title/summary） | `Agent.Service.get/list/defaultAgent/generate` |
| **Session** | `src/session/` | 会话生命周期、消息存储、LLM 交互、compaction | `Session.Service` (CRUD) + `SessionProcessor.Service` (streaming) |
| **Provider** | `src/provider/` | 20+ LLM provider 接入、模型发现、SDK 加载 | `Provider.Service.list/getModel/getLanguage/defaultModel` |
| **Tool** | `src/tool/` | 15+ 内置工具 + 自定义工具 + MCP 工具 + Plugin 工具 | `ToolRegistry.Service.tools/all/ids` |
| **Permission** | `src/permission/` | 权限评估、ask/allow/deny 决策、Deferred 异步等待 | `Permission.Service.ask/reply/list` |
| **Plugin** | `src/plugin/` | 插件加载（npm/本地/内置）、hooks 触发 | `Plugin.Service.trigger/list/init` |
| **MCP** | `src/mcp/` | MCP 协议客户端，stdio/HTTP/SSE 传输，OAuth | `MCP.Service.tools/prompts/resources/connect` |
| **Bus** | `src/bus/` | 进程内 PubSub 事件系统 | `Bus.Service.publish/subscribe` |
| **Sync** | `src/sync/` | Event Sourcing 持久化、projector 注册 | `SyncEvent.run/define/project` |
| **Snapshot** | `src/snapshot/` | Git-based 文件系统快照 | `Snapshot.Service.track/patch/restore/revert` |
| **Server** | `src/server/` | Hono HTTP 服务、WebSocket、路由 | 控制面 + 实例路由 |
| **Skill** | `src/skill/` | SKILL.md 发现与加载 | `Skill.Service.get/all/available` |
| **Config** | `src/config/` | 多层配置合并（全局/项目/.opencode/plugin） | `Config.Service.get/directories` |
| **Storage** | `src/storage/` | SQLite 数据库（Bun/Node 双适配） | `Database.use/Client` |

### 架构图
见上方 X1 架构图。补充关键数据流：

**用户消息处理流**:
```
User Input -> CLI/SDK -> Server Route -> SessionPrompt.prompt()
  -> Session.create() (if new)
  -> MessageV2.toModelMessages() (序列化历史)
  -> LLM.stream() (调 AI SDK streamText)
  -> SessionProcessor.handleEvent() (处理每个 stream event)
    -> tool-call: Permission.ask() -> Tool.execute() -> updatePart()
    -> text-delta: updatePartDelta() (增量推送)
    -> finish-step: Snapshot.patch() + usage计算
  -> Compaction (if overflow)
  -> Summary (async fork)
```

### 扩展点
1. **Plugin Hooks** (`@opencode-ai/plugin` 类型定义): `chat.params`, `chat.headers`, `tool.definition`, `experimental.chat.system.transform`, `experimental.chat.messages.transform`, `experimental.text.complete`, `experimental.session.compacting`, `experimental.compaction.autocontinue` 等 10+ 钩子
2. **Custom Tools**: 在 `.opencode/tool/` 或 `.opencode/tools/` 目录放 JS/TS 文件自动加载
3. **Custom Agents**: 在 `opencode.json` 的 `agent` 字段配置自定义 agent，支持自定义 prompt/model/permission/temperature
4. **MCP Servers**: 标准 MCP 协议（stdio/HTTP），支持 OAuth
5. **Skills (SKILL.md)**: 在 `.opencode/skills/`、`.claude/skills/`、`.agents/skills/` 放 SKILL.md 文件
6. **Provider SDK**: 通过 `@ai-sdk/openai-compatible` 或 npm 包名自动加载任何 Vercel AI SDK 兼容 provider
7. **SyncEvent Projectors**: 自定义事件类型和投影函数

### 权衡分析
| 决策 | 收益 | 代价 |
|------|------|------|
| **Effect-TS 作为核心 DI/并发框架** | 类型安全的依赖注入；结构化并发（Fiber/Scope/Deferred）；强大的错误处理管道；自动 tracing/observability | 极高学习曲线；IDE 支持有限；堆栈追踪可读性下降；社区生态小 |
| **Bun 作为运行时** | 更快的启动和运行速度；内置 SQLite；更好的 TS 支持 | 生态兼容性问题（node-pty 需要 fix 脚本）；部分 Node API 差异 |
| **Event Sourcing (SyncEvent)** | 完整的事件历史；支持 replay/undo；解耦读写 | 复杂度增加；需要维护 projector；写入性能（每次 event 都要持久化） |
| **Vercel AI SDK 作为 LLM 抽象层** | 20+ provider 开箱即用；统一 streaming 接口；tool calling 标准化 | 受限于 AI SDK 的设计决策（如 token 计算方式）；需要跟随其 breaking changes |
| **SQLite (本地) 而非远程数据库** | 零配置；极快的本地读写；离线工作 | 不支持多进程并发写入；不适合云部署 |
| **Provider-specific Prompt** | 每个模型都能获得最优提示 | 需要维护多份 prompt（当前 8 种）；新模型需要适配 |
| **Client/Server 分离** | 支持远程驱动（如手机操控电脑上的 agent）；多前端共享同一 session | 增加了网络层复杂度；本地使用时的额外开销 |

---

## A1 Agent架构分析

### Agent核心架构
OpenCode 的 Agent 系统设计为**声明式 Agent 配置 + 统一执行引擎**模式：

- **Agent 定义** (`src/agent/agent.ts`): Agent 本身是一个配置对象（`Agent.Info`），包含 name、mode、permission ruleset、prompt、model、temperature 等属性。不包含执行逻辑。
- **执行引擎** (`src/session/processor.ts` + `src/session/llm.ts`): 所有 agent 共享同一个执行引擎。`LLM.stream()` 发起 AI 调用，`SessionProcessor.handleEvent()` 处理流式事件。
- **差异化通过配置实现**: build agent 有完整工具权限；plan agent 禁止编辑工具；explore agent 只有搜索工具。这完全通过 Permission ruleset 配置实现。

**内置 Agent 类型**（`src/agent/agent.ts:107-233`）:
| Agent | Mode | 用途 | 权限特点 |
|-------|------|------|----------|
| `build` | primary | 默认开发 agent | 完整权限（question + plan_enter） |
| `plan` | primary | 只读分析 agent | 禁止编辑；可写 .opencode/plans/*.md |
| `general` | subagent | 通用并行任务 agent | 禁止 todowrite |
| `explore` | subagent | 快速代码搜索 agent | 仅 grep/glob/list/bash/read/webfetch/websearch/codesearch |
| `compaction` | primary/hidden | 上下文压缩 | 禁止所有工具 |
| `title` | primary/hidden | 自动生成标题 | 禁止所有工具 |
| `summary` | primary/hidden | 生成会话摘要 | 禁止所有工具 |

### 决策机制
Agent 的决策完全委托给 LLM。OpenCode 不实现任何显式的规划算法或状态机，而是通过以下机制引导 LLM 行为：

1. **System Prompt 路由** (`src/session/system.ts:19-33`): 根据 model API ID 选择最匹配的 system prompt（8 种变体：anthropic/gpt/beast/gemini/codex/trinity/kimi/default）
2. **Tool Description 动态构建** (`src/tool/registry.ts:245-277`): `task` 工具的 description 会动态列出所有可用 subagent 及其描述；`skill` 工具的 description 会列出所有可用 skill
3. **Permission 作为硬约束**: LLM 不能绕过权限系统。`Permission.ask()` 使用 `Deferred` 阻塞执行直到用户回复
4. **Doom Loop 检测** (`src/session/processor.ts:305-330`): 连续 3 次相同 tool+input 自动触发 permission ask，打断死循环
5. **Compaction 触发**: 当 token 使用量超过 model context 的阈值时自动触发 compaction agent 生成 summary

### 工具系统
**内置工具** (15+):

| 工具 | 文件 | 功能 |
|------|------|------|
| `bash` | `src/tool/bash.ts` | PTY 命令执行 |
| `read` | `src/tool/read.ts` | 读取文件内容 |
| `edit` | `src/tool/edit.ts` | 精确字符串替换编辑 |
| `write` | `src/tool/write.ts` | 写入/创建文件 |
| `apply_patch` | `src/tool/apply_patch.ts` | 应用 patch（GPT 模型专用） |
| `glob` | `src/tool/glob.ts` | 文件模式匹配搜索 |
| `grep` | `src/tool/grep.ts` | 内容搜索 (ripgrep) |
| `task` | `src/tool/task.ts` | 启动 subagent 子会话 |
| `todowrite` | `src/tool/todo.ts` | 任务列表管理 |
| `webfetch` | `src/tool/webfetch.ts` | 获取网页内容 |
| `websearch` | `src/tool/websearch.ts` | Web 搜索 |
| `codesearch` | `src/tool/codesearch.ts` | 代码搜索 |
| `skill` | `src/tool/skill.ts` | 加载 SKILL.md 指令 |
| `question` | `src/tool/question.ts` | 向用户提问 |
| `lsp` | `src/tool/lsp.ts` | LSP 语言服务查询（实验性） |
| `plan` | `src/tool/plan.ts` | 进入/退出 plan 模式 |
| `invalid` | `src/tool/invalid.ts` | 兜底工具，处理无效 tool call |

**工具生命周期**:
1. `Tool.define(id, init)` 注册工具，返回 `Effect<Info<P, M>>`
2. `Tool.init(info)` 初始化工具，调用 init 闭包获取 `Def`
3. `ToolRegistry.state()` 在 InstanceState 中缓存所有初始化好的工具
4. `ToolRegistry.tools(model)` 根据 model/provider 动态筛选工具（如 GPT 用 apply_patch 替代 edit+write）
5. 执行时 `Tool.wrap()` 自动添加 schema 校验、output truncation、span tracing

**工具扩展机制**:
- `.opencode/tool/*.ts` 文件自动发现并加载
- Plugin 通过 `hook.tool` 注册
- MCP 工具通过 `MCP.tools()` 动态加载
- Permission 系统控制每个 agent 可用哪些工具

### 记忆系统
OpenCode 采用**多层记忆架构**:

1. **Session (长期记忆)**: SQLite 持久化。每个 session 保存完整的消息历史（MessageV2），包括 user/assistant 消息、tool calls、reasoning、patches、step-start/step-finish 等所有 parts。Session 支持 fork（分叉）。
2. **Compaction (压缩记忆)** (`src/session/compaction.ts`): 当 token 超过 context limit 时，自动运行 compaction agent 生成 anchored summary：
   - 检测已有的 compaction 历史，增量更新 summary
   - 保留最近 N 轮对话（tail preservation）作为未压缩内容
   - Summary 模板包含 Goal/Constraints/Progress/Key Decisions/Next Steps/Critical Context/Relevant Files
   - Prune 机制：对超出保护范围的旧 tool output 进行截断
3. **Snapshot (文件系统记忆)** (`src/snapshot/index.ts`): Git-based 文件系统快照，记录 agent 每个 step 的文件变更，支持 revert 到任意快照点。
4. **Instructions (指令记忆)** (`src/session/instruction.ts`): 加载 `AGENTS.md` 等指令文件，作为 system prompt 的一部分。
5. **Skills (技能记忆)** (`src/skill/index.ts`): SKILL.md 文件定义可重用的领域知识和工作流，按需加载到 context 中。

### 多Agent协作
OpenCode 通过 **Task Tool + 子会话** 实现多 Agent 协作：

1. **启动方式** (`src/tool/task.ts:30-176`): 主 agent 调用 `task` 工具，指定 `subagent_type` 和 `prompt`
2. **子会话创建**: `sessions.create({ parentID })` 创建子会话，继承 parent session 的 context
3. **权限隔离**: 子 agent 可以配置独立的 permission ruleset。默认禁止 subagent 调用 `todowrite` 和 `task`（防止无限嵌套）
4. **Model 继承**: 子 agent 默认使用与 parent agent 相同的 model，但可以在 agent config 中指定不同 model
5. **结果返回**: 子 agent 完成后，最后一条 text part 作为结果返回给 parent agent
6. **会话复用**: 通过 `task_id` 参数可以恢复之前的子会话，实现跨轮次的 subagent 协作
7. **取消传播**: parent 的 abort signal 自动取消子会话

**Agent 类型与协作模式**:
- `general`: 通用 subagent，用于并行执行多步任务
- `explore`: 专用代码搜索 subagent，只有只读工具，适合快速探索

### 执行循环
核心执行循环在 `SessionPrompt.prompt()` (推断) -> `SessionProcessor.process()` -> `LLM.stream()`:

```
SessionPrompt.prompt(input):
  1. 创建 user message 和 assistant message
  2. 转换历史消息为 LLM 格式 (MessageV2.toModelMessages)
  3. 构建 system prompt (provider-specific + environment + skills + instructions)
  4. 构建 tools (ToolRegistry.tools + MCP.tools, 过滤 permission)
  5. 进入主循环:
     while (true):
       processor = SessionProcessor.create(assistantMessage)
       result = processor.process(streamInput)
       
       if result == "compact":
         SessionCompaction.prune()  // 截断旧 tool output
         SessionCompaction.create() + .process()  // 生成 summary
         创建新 user message (continue)
         创建新 assistant message
         重建 messages + system prompt
         continue
       
       if result == "stop":
         break (错误或被阻止)
       
       if result == "continue":
         if assistantMessage.finish == "stop":  // LLM 自然停止
           break
         创建新 assistant message (继续生成)
         重建 messages
         continue

SessionProcessor.process(streamInput):
  1. LLM.stream(streamInput) -> Effect Stream
  2. Stream.tap(handleEvent) 处理每个事件:
     - start: 标记 session 为 busy
     - reasoning-start/delta/end: 处理 reasoning tokens
     - tool-input-start/tool-call: 创建/更新 tool part
     - tool-result/tool-error: 完成/失败 tool call
     - text-start/delta/end: 处理文本输出
     - start-step: 创建快照
     - finish-step: 计算 usage + 创建 patch + 检查 overflow
     - error: 抛出异常
  3. 清理: 结算所有未完成的 tool call
  4. 返回: "compact" | "stop" | "continue"
```

**关键设计**: 执行循环不是简单的 request-response，而是一个 step-by-step 的流式处理管道。每个 "step" 对应 LLM 的一次连续生成（可能包含多个 tool call + text），step 之间可以有多轮（当 LLM 返回 tool call 而非 stop 时）。

---

## 综合评分
| 维度 | 评分(1-10) | 亮点 | 可改进 |
|------|------------|------|--------|
| 代码质量 | 9 | 一致的函数式风格；严格的类型安全；Effect-TS 管道清晰 | Effect-TS 的复杂性可能阻碍贡献者 |
| 架构设计 | 9 | Client/Server 分离；Event Sourcing；Permission 系统精巧 | 部分模块间耦合（如 provider.ts 1700+ 行） |
| 可扩展性 | 10 | Plugin hooks + Custom tools + MCP + Skills + Custom agents | 部分 hooks 标记为 experimental |
| Agent 能力 | 9 | 完整的工具集；智能 compaction；Snapshot 回滚 | 无显式 planning/reasoning 框架 |
| 多模型支持 | 10 | 20+ 内置 provider；model-specific prompts；动态模型发现 | 某些 provider 配置复杂 |
| 安全设计 | 9 | Permission 系统；Doom loop 检测；.env 文件保护 | 无沙箱执行环境 |
| 开发体验 | 8 | Bun 快速启动；热重载；Storybook | Effect-TS 学习曲线 |
| 文档/社区 | 8 | 22 种语言 README；完整 contributing guide；Discord | 架构文档较少 |

---

## 核心收获

### 最值得借鉴的 3 个设计决策
1. **Agent 即配置**: 不为每种 agent 写不同的执行逻辑，而是将 agent 定义为 permission/prompt/model 的组合配置。所有 agent 共享一个执行引擎，差异化完全通过声明式配置实现。这大幅降低了添加新 agent 的成本。
2. **Permission 作为一等公民**: 权限不是事后加的装饰器，而是架构的核心组件。工具执行、文件访问、agent 切换都经过 Permission 评估。wildcard pattern + 分层规则 + 异步 ask 的组合提供了精确的控制力。
3. **Client/Server 分离 + Event Sourcing**: 将 agent 后端与 UI 前端分离，通过事件流通信。这使得同一 agent 可以被 TUI、桌面应用、Web、移动端驱动，同时事件溯源保证了状态的可追溯和可恢复。

### 最值得学习的 3 个代码模式
1. **Effect-TS Service + Layer 模式**: 每个模块定义 `Interface` -> `Service extends Context.Service` -> `Layer.effect(Service, Effect.gen(...))` -> 在 layer 中 `yield*` 依赖服务。这形成了编译时检查的依赖图，消除了运行时 DI 容器的需要。
2. **InstanceState + ScopedCache**: 用 Effect 的 `ScopedCache` 按 working directory 隔离状态，自动管理生命周期（创建/失效/清理）。对任何需要多项目隔离的工具都适用。
3. **Stream-based LLM 处理管道**: `LLM.stream() -> Stream.tap(handleEvent) -> Stream.takeUntil -> Stream.runDrain`，配合 `Effect.retry` 和 `Effect.onInterrupt`，用函数式管道处理复杂的异步流。

### 最值得复用的 3 个工具/脚本
1. **Tool.define() + ToolRegistry**: 完整的工具定义、注册、初始化、过滤框架。包含 schema 校验、output truncation、span tracing、permission 检查。可直接移植到任何 agent 框架。
2. **Permission 系统**: `Permission.fromConfig() -> merge() -> evaluate()` 的权限管道，支持 wildcard pattern 匹配、分层规则合并、异步 ask。不到 400 行实现了工业级的权限控制。
3. **Compaction 系统**: anchored summary 模板 + tail preservation + prune 机制。特别是 `select()` 函数中的 token budget 分配算法和 `splitTurn()` 的精确切分，是长对话 context 管理的最佳实践。

---

## 推荐学习路径
1. **先读** -> `packages/opencode/src/agent/agent.ts` (理解 Agent 定义模型) + `packages/opencode/src/tool/tool.ts` (理解 Tool 抽象) + `packages/opencode/src/permission/index.ts` (理解权限系统) —— 这三个文件定义了 OpenCode 的核心概念模型
2. **再看** -> `packages/opencode/src/session/llm.ts` (LLM 调用层) + `packages/opencode/src/session/processor.ts` (流式事件处理) + `packages/opencode/src/session/compaction.ts` (上下文压缩) —— 这三个文件构成了 Agent 的执行引擎
3. **最后研究** -> `packages/opencode/src/provider/provider.ts` (20+ provider 接入架构) + `packages/opencode/src/mcp/index.ts` (MCP 协议实现) + `packages/opencode/src/effect/instance-state.ts` (状态管理核心) + `packages/opencode/src/sync/index.ts` (Event Sourcing 实现) —— 这些是架构层面的深度设计
