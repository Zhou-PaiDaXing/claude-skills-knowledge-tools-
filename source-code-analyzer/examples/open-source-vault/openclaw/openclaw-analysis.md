---
title: OpenClaw 源码洞察
aliases:
  - OpenClaw
  - openclaw
  - Multi-channel AI Gateway
tags:
  - 开源分析
  - TypeScript
  - AI-Agent
  - LLM
  - 多渠道网关
  - 插件架构
  - MCP
  - ACP
  - 工具调用
  - 消息平台
  - coding-agent
  - multimedia-pipeline
  - commitments
  - i18n
  - clawhub
  - qa-lab
github: https://github.com/openclaw/openclaw
created: 2026-04-29
updated: 2026-05-18
score: 7.3
lifecycle: ACTIVE
last_audit: 2026-05-21
---

## 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-29 | v1.0 | 初版：基于 commit 492e2a3060 完成全量源码分析，覆盖核心理念、6 大设计亮点、6 个可学习模式、架构全景图、Agent 编排/Memory+RAG/Prompt 工程三个深度专题 |
| 2026-04-29 | v1.1 | 补充 6 页 draw.io 系统架构图 (System Overview / Agent Loop / MCP+ACP / Memory+RAG+Context / Prompt Compiler / Hook+Plugin Lifecycle)，导出 PNG 并嵌入文档 |
| 2026-05-18 | v1.2 | 增量更新：对齐 openclaw `2026.5.17` (HEAD `816fbe0cf0`)。**Δ 扩展** 125→128 (新增 admin-http-rpc / canvas / clickclack / file-transfer / oc-path；移除 bluebubbles / shared)；**Δ src/** 新增 commitments / plugin-state / provider-runtime / talk / tools / oc-path，移除 canvas-host / realtime-voice；**新概念** ClawHub & Clawpack / QA-Lab + Mantis / Autoreview / Commitments / Codex App-Server 深度集成 / 媒体生成统一异步生命周期 / Mid-turn compaction precheck / Post-compaction loop guard / Active-memory 熔断 / i18n (en/zh-CN/zh-TW) / xAI Grok OAuth / NVIDIA Provider / TUI / Tool Descriptor Planner / 批量 active steering / Plugin SDK `defineToolPlugin` / Context Engine `thread_bootstrap` projection。**数据校正** v1.0/v1.1 声明的 "131 个扩展" 实测为 125 (v1.1 时) / 128 (现在)；"53+ Skills" 现统计为 30 顶层 + 71 插件捆绑 = 101 SKILL.md。架构图 6 张全部 patch + 重新导出。 |

---

## v1.2 增量变更 (2026-04-29 → 2026-05-18)

> 基准 commit `492e2a3060` → 当前 `816fbe0cf0`，区间 **12,768 commits / 226 feat**。openclaw 版本 `2026.4.27` → `2026.5.17`。
> 行级标记图例：🆕 新增 ｜ ♻️ 更新 ｜ ⚠️ 已废弃 ｜ ✅ 自上版仍然成立

### 1. 结构性变化

**src/ 顶层目录**

- 🆕 **`src/commitments/`** — Agent 承诺(commitment) 抽取与跟踪。`extraction.ts` / `store.ts` / `runtime.ts` / `model-selection.runtime.ts` / `commitments-heartbeat-policy.e2e.test.ts`。把 Agent 在对话中做出的"承诺/后续动作"结构化抽取并放入轻量调度心跳，避免承诺被遗忘。
- 🆕 **`src/plugin-state/`** — SQLite 后端的 Plugin State Store (PR #74190)。9 个文件，含权限/路径隔离测试，是新的插件持久化基线 (`plugin-state-store.sqlite.ts` 为核心实现)。
- 🆕 **`src/provider-runtime/`** — `operation-retry.ts`，统一 provider 重试入口（目前仅 1 个 helper，是新抽象的起点）。
- 🆕 **`src/talk/`** — 替代旧 `realtime-voice/` 的实时语音 + Agent-to-Agent **consult/talkback** 子系统。`agent-consult-runtime.ts` / `agent-talkback-runtime.ts` / `audio-codec.ts` / `fast-context-runtime.ts` / `diagnostics.ts`。
- 🆕 **`src/tools/`** — 工具模块整合层（与 `extensions/` 中的工具插件协作）。
- 🆕 **`src/oc-path/`** — 路径标准化器（配合新扩展 `extensions/oc-path/`）。
- ⚠️ **`src/canvas-host/`** → 能力外置到 `extensions/canvas/`。
- ⚠️ **`src/realtime-voice/`** → 拆分到 `src/talk/` + `extensions/voice-call` + `extensions/talk-voice`。

**extensions/ 目录** (125 → 128, +5 / −2)

- 🆕 `admin-http-rpc` — 内建管理 RPC（暴露 admin HTTP 接口）
- 🆕 `canvas` — 画板/绘图能力，从 `src/canvas-host` 迁出
- 🆕 `clickclack` — 渠道侧 channel-plugin（具体语义见其 `channel-plugin-api.ts`）
- 🆕 `file-transfer` — 文件传输能力
- 🆕 `oc-path` — PATH 辅助工具
- ⚠️ `bluebubbles` — 移除 (iMessage relay 路径)
- ⚠️ `shared` — 移除（公共代码下沉到 SDK / 各插件本地）
- ♻️ **扩展总数从 125 → 128**（v1.0/v1.1 旧文档声称的 "131" 经实测为口径错误，本版校正）

### 2. 新增核心能力（v1.1 完全没提）

1. 🆕 **ClawHub & Clawpack** — 新的插件分发系统（类比 npm Registry）。`prefer clawhub for channel setup installs / bundled cutovers / onboarding`、`install clawhub clawpack artifacts`、`type clawhub security reports`。详见 [v1.2 新增章节 §架构全景图 — ClawHub 通路](#v12-新增插件分发新通路-clawhub-)。
2. 🆕 **QA-Lab + Mantis + qa-channel / qa-matrix** — 正式 QA 基础设施：runtime parity tiers (standard / soak / live-only)、scenario packs (personal-agent / runtime-parity)、`openclaw qa suite --pack` + `qa coverage --tools`。对比基准已更新为 **GPT-5.5 vs Claude Opus 4.7**。
3. 🆕 **Autoreview** — 强制 pre-land 自动评审 skill；commit `73f4657869 docs: require autoreview before PR landing`。
4. 🆕 **Tideclaw alpha gates** — alpha 通道发布支持，`feat: support alpha releases` + `ci: make Tideclaw alpha long gates advisory`。
5. 🆕 **Commitments 系统** — 与 `src/commitments/` 对应，是 Agent 自我跟踪 follow-up 的新能力。
6. 🆕 **`defineToolPlugin` + `openclaw plugins build/validate/init`** — 降低插件作者门槛的 SDK 新接口（`src/plugin-sdk/tool-plugin.ts:131`）。
7. 🆕 **i18n** — wizard / 渠道安装向导本地化（en / zh-CN / zh-TW，PR #80645）；Telegram 命令菜单本地化；UI i18n baseline report。
8. 🆕 **Active-memory 熔断** — 连续失败后自动跳过 recall（`extensions/active-memory`，PR #74158）。
9. 🆕 **Codex App-Server 深度集成** — context-engine projections 绑定到 Codex threads（PR #82351）；native tool call 落入 trajectory 导出；Codex OAuth 与 sidecar profile 兼容。
10. 🆕 **xAI Grok OAuth** (SuperGrok)、**Xiaomi MiMo 思考模式**、**NVIDIA Provider**（PR #71204）、**Together v2 video API**、**MiniMax** image understanding 路由、**SenseAudio / Telnyx Media Streaming / Synthetic / Vydra** 等渠道扩展。
11. 🆕 **媒体生成统一异步任务生命周期** — `image_generate` / `music_generate` / `video_generate` 走同一套 async task lifecycle（status / dedupe / message-tool completion handoff）。fal + OpenRouter 新增 music generation providers。详见 [v1.2 新增章节 §架构全景图 — 媒体生成 + 实时语音集群](#v12-新增媒体生成--实时语音集群-)。
12. 🆕 **TUI** — `extensions/tui` 渐成形，TUI submitted draft 在 chat busy 时恢复（fix #45326）。
13. 🆕 **Channel progress drafts + 默认批量 active steering** — `feat: default active steering to batched delivery` + Slack rich progress drafts；`streaming.progress.maxLineChars` 可调。
14. 🆕 **Mid-turn compaction precheck (PR #73499) + Post-compaction loop guard** — 两个新的 attempt-loop 防护点。实现位于 `src/agents/pi-embedded-runner/post-compaction-loop-guard.ts`；配置 schema 校验位于 `src/config/zod-schema.post-compaction-guard.test.ts`。
15. 🆕 **Generic code mode runtime** — `feat: add generic code mode runtime`，新 Harness 类型。
16. 🆕 **Tool Descriptor Planner** — `feat: add tool descriptor planner`，配合内建工具描述精简（media / messaging / sessions / cron / Gateway / web / image/PDF / TTS / nodes / plan tools 全面瘦身）。
17. 🆕 **Per-agent bootstrap profiles** — `feat(agents): support per-agent bootstrap profiles`。
18. 🆕 **Admin HTTP RPC bundled plugin** — 新插件 `extensions/admin-http-rpc`，对外暴露管理 RPC。
19. 🆕 **观测性升级** — gateway stall diagnostics / restart trace instrumentation / control-ui responsiveness diagnostics / diagnostics timeline / 拆分 attempt-dispatch startup 子 span。
20. 🆕 **Group chat room events** — opt-in `messages.groupChat.unmentionedInbound: "room_event"`（PR #81317），让未被 @ 的群闲聊作为"安静上下文"，只通过 message tool 显式发言。
21. 🆕 **Slack assistant thread lifecycle** — manifest assistant view、suggested prompts、thread-scoped assistant sessions。
22. 🆕 **Context Engine 接口大幅扩展**（v1.1 提到 7+ 方法时尚未存在）：新增 `ContextEngineProjection`（`per_turn` / `thread_bootstrap`，配合 epoch 复用 backend 线程）、`promptAuthority`、`TranscriptRewriteRequest/Result` 与 runtime `rewriteTranscriptEntries` helper、完整的 `ContextEnginePromptCacheInfo`（retention / usage / observation / cache-touch）、`turnMaintenanceMode` (foreground/background)、`SubagentSpawnPreparation` rollback。

### 3. 行为/默认值的关键改动

- 🆕 active steering 默认 batched delivery（`feat: default active steering to batched delivery`）
- 🆕 plugin `before_agent_start` hook 默认 15 秒超时（fix #48534）
- 🆕 ClawHub 优先安装路径（bundled cutover → clawhub clawpack）
- 🆕 group chat 支持 `unmentionedInbound: "room_event"`
- 🆕 GPT-5 默认不再硬截断（Fix #82910）
- 🆕 `openclaw cron run --wait` 阻塞模式（PR #81929）
- 🆕 GPT-5.5 Codex 上下文按 Codex runtime context window 算 compaction（Fix #82982）

### 4. 文档需修订的旧声明

- ♻️ **"131 个扩展"** → 校正为 **128** (当前) / **125** (v1.1 时实际)
- ♻️ **"53+ Skills"** → 校正为 **30 个顶层 skills**（`.agents/skills/`） + **71 个插件捆绑 skills** = **101 SKILL.md**（含 `.qoder/skills` 与 `extensions/*/skills/`）
- ♻️ **Context Engine 接口"7+ 方法"** → 仍成立，但 v1.2 起带 thread_bootstrap projection、transcript rewrite、prompt cache observation 等新数据通路
- ♻️ **Skills "18,000 字符预算"** → `SYSTEM_PROMPT_CACHE_BOUNDARY = "<!-- OPENCLAW_CACHE_BOUNDARY -->"` 仍是 cache 分区核心常量；具体 skills 字符预算常量名在 v1.2 期间存在重命名/抽取，原文中"18000"待新版本号下二次确认。
- 其余 v1.1 章节结论（微内核 + 契约边界、auth profile 轮换、MCP+ACP 双协议、SubAgent spawn/announce/steer、Hook 40+ 切面、Memory 单槽位 + 0.7/0.3 Hybrid Search、QMD 模式）**经核对仍然成立**（详见正文 ✅ 标记）

---

# OpenClaw 源码洞察

## 一句话本质

> OpenClaw 是一个运行在本地设备上的**多渠道 AI 网关 + 个人 AI 助手**，它的核心创新是将 **"微内核 + 131 个插件"** 的架构模式应用于 Agent 系统，让一个 AI 能同时接入 20+ 消息渠道、20+ LLM 提供商，并通过 MCP/ACP/SubAgent/Memory/Context Engine 五大子系统实现真正可执行任务的 Agent 能力。

**规模** ♻️ (v1.2 数据): ~8,000+ TS 文件 | **128 个扩展插件**（旧文档误称 131） | **30 顶层 + 71 插件捆绑 = 101 SKILL.md** (旧文档误称 53+) | 版本 **2026.5.17** (日历版本号，每日 release) | MIT 许可证

---

## 核心理念

### 作者在设计时秉持的价值观

**理念1: "微内核 + 契约边界" -- 核心永远不知道具体插件是谁** ✅

- 体现在哪里: 核心代码 (`src/`) 通过 `openclaw/plugin-sdk/*` 与扩展交互，**脚本化守护边界** (`scripts/check-extension-plugin-sdk-boundary.mjs`, `scripts/check-architecture-smells.mjs`) 在 CI 中持续验证没有跨界引用
- 为什么重要: 131 个插件可以独立演进而不破坏核心，核心可以自由重构内部实现。第三方插件开发者只需面对稳定的 SDK 契约
- 如何借鉴: 任何需要插件生态的系统，都应该在**架构边界上投资自动化守护脚本**，而不是靠 Code Review。人会犯错，脚本不会

**理念2: "Prompt Cache 是一等公民" -- 每一个字节的稳定性都值得投资** ✅

- 体现在哪里: `src/agents/prompt-cache-stability.ts` + `SYSTEM_PROMPT_CACHE_BOUNDARY` 标记将系统提示严格分为 "稳定前缀" 和 "动态后缀"。所有 maps/sets/registries/工具列表/文件列表在送入 LLM 前做稳定排序
- 为什么重要: LLM 提供商的 KV Cache 机制要求 system prompt 前缀**逐字节一致**才能复用。一个不确定性的排序就意味着每次调用都要重新计算注意力 -- 既贵又慢
- 如何借鉴: 在任何频繁调用 LLM 的系统中，**将 system prompt 分为静态/动态两区**，静态区做确定性排序，仅此一项就能显著降低成本和延迟

**理念3: "弹性优先" -- 每一层都有 fallback** ✅ ♻️ v1.2 补强：mid-turn compaction precheck / post-compaction loop guard / active-memory 熔断 / ACP backend provider failover / per-agent bootstrap profiles 进一步把"为每种失败原因定义恢复策略"贯彻到更多边界

- 体现在哪里: Auth Profile 轮换 + Cooldown (`src/agents/auth-profiles.ts`)，模型 Failover 链 (`src/agents/model-fallback.ts`)，Harness 降级 (插件 -> PI Fallback)，SubAgent 孤儿恢复 (`src/agents/subagent-orphan-recovery.ts`)
- 为什么重要: 生产级 AI 应用面对的是: API Key 限流、模型不可用、子进程崩溃、网关重启。每一层都需要自己的容灾策略
- 如何借鉴: 构建 AI 应用时，将 "失败处理" 作为核心设计维度而非事后补丁。**为每种失败原因定义专门的恢复策略**

**理念4: "声明式配置 + 程序化扩展" -- 静态描述能力，动态注入行为** ✅ ♻️ v1.2 强化：新增 `defineToolPlugin` + `openclaw plugins build/validate/init` 三件套，让"简单工具插件"的声明门槛进一步降低（`src/plugin-sdk/tool-plugin.ts:131`）

- 体现在哪里: 插件通过 `openclaw.plugin.json` 声明能力 (模型前缀、渠道、认证方式)，通过代码 `register()` 注入运行时行为。Skills 通过 `SKILL.md` 声明式定义，通过 Hooks 动态修改
- 为什么重要: 声明式部分可以被工具链解析 (市场发现、安全审计、静态分析)，程序化部分提供无限灵活性
- 如何借鉴: 设计扩展系统时，**把 "我能做什么" 和 "我怎么做" 分开**。前者用 manifest/schema，后者用代码

### 与主流方案的哲学差异

| 维度 | 主流 Agent 框架 (LangChain/CrewAI) | OpenClaw 的做法 | 背后的思考 |
|------|------|------|------|
| 部署模型 | 云端服务 / SDK 嵌入 | **本地设备优先** (macOS/iOS/Android) | 数据主权 + 离线能力 + 低延迟 |
| Agent 编排 | DAG/Graph (LangGraph) | **嵌入式循环 + SubAgent spawn** | 低延迟 + 流式友好 + 状态就地管理 |
| 工具系统 | 框架定义 Tool 接口 | **MCP 协议 + Plugin Tool + 内置 Tool** 三层并行 | 生态兼容 + 灵活性 + 标准化 |
| Memory | 向量数据库 API | **单槽位插件 + Hybrid Search + QMD** | 可替换后端 + 多模态检索 + 行为决策 |
| Context | 固定窗口 | **Context Engine 接口 + Compaction + 分区缓存** | 无限对话 + 缓存友好 + 可插拔策略 |
| 扩展方式 | 继承/装饰器 | **40+ Hook 点 + Manifest 声明 + SDK 契约** | 非侵入式 + 声明式发现 + 三方友好 |

---

## 设计亮点

### 亮点1: Context Engine -- 比 RAG 更完整的上下文生命周期 ✅ ♻️ v1.2 大幅扩展

**问题背景:**
- 传统做法: "RAG = 检索 + 拼接到 prompt"，一个函数搞定
- 缺陷: 没有上下文的**生命周期管理** -- 谁负责摄入？谁负责压缩？谁负责组装？多久维护一次？

**创新做法:**

OpenClaw 将上下文管理抽象为一个完整的**生命周期引擎** (`src/context-engine/types.ts`):

```
bootstrap → ingest → assemble → compact → maintain → dispose
    |          |         |          |          |
  初始导入   消息摄入   上下文组装   压缩总结   后台维护
```

- `bootstrap()`: 导入历史上下文 (恢复会话)
- `ingest()` / `ingestBatch()`: 新消息摄入引擎 (不止是存储，可能触发索引)
- `assemble()`: 在 token budget 内组装最优上下文 (这才是 "RAG" 发生的地方)
- `compact()`: 超出上下文窗口时做智能压缩 (不是简单截断)
- `maintain()`: 后台维护任务 (索引重建、过期清理)
- `afterTurn()`: 每轮对话后的持久化和后台 compaction
- `prepareSubagentSpawn()` / `onSubagentEnded()`: 子 Agent 上下文传递

**关键设计: Registry + 可插拔实现**

```typescript
// 插件可注册自定义引擎
api.registerContextEngine("my-engine", (params) => new MyContextEngine(params));

// 核心通过 registry 选择引擎
const engine = resolveContextEngine(sessionKey); // 按 session 选择
```

Legacy 引擎作为 fallback，确保向后兼容。

**代价与适用性:**
- 代价: 接口复杂 (7+ 方法)，对插件开发者有学习成本
- 适用: 任何需要长对话、多轮交互、跨会话记忆的 Agent 系统
- 不适用: 简单的 Q&A 场景 (过度设计)

#### v1.2 新增 🆕：thread_bootstrap projection + 安全 transcript rewrite + prompt cache observation

`src/context-engine/types.ts` 在 v1.2 期间显著扩展（v1.1 时这些字段并不存在）：

```typescript
// 新的 projection 模式：让支持持久 backend 线程的宿主复用线程
type ContextEngineProjection = {
  mode: "per_turn" | "thread_bootstrap";
  epoch?: string;        // epoch 不变就复用 backend 线程；变化触发轮转
  fingerprint?: string;  // 投影载荷的诊断指纹
};

// 安全 transcript 重写（不依赖 Pi 内部，由 runtime 提供）
runtimeContext.rewriteTranscriptEntries?(request: TranscriptRewriteRequest)
  => Promise<{ changed, bytesFreed, rewrittenEntries }>;

// Prompt cache observability：完整暴露 retention / 用量 / 是否被打破
type ContextEnginePromptCacheInfo = {
  retention?: "none" | "short" | "long" | "in_memory" | "24h";
  lastCallUsage?: { input, output, cacheRead, cacheWrite, total };
  observation?: { broke, changes: [{ code, detail }] };  // code: cacheRetention | model | streamStrategy | systemPrompt | tools | transport
  lastCacheTouchAt?: number;
  expiresAt?: number;
};

// 维护任务可以选 foreground / background
turnMaintenanceMode?: "foreground" | "background";

// SubAgent spawn 准备阶段可以注册回滚
type SubagentSpawnPreparation = { rollback: () => void | Promise<void> };
```

最大意义：**Context Engine 与 Codex App-Server 等"持有持久后端线程"的集成方式终于有了统一抽象**（thread_bootstrap projection），不再需要每轮重投影；同时 prompt cache 命中/打破有了可观测、可归因的字段。

---

### 亮点2: Compaction System -- 无限对话的核心引擎 ✅ ♻️ v1.2 新增双重防护点

**问题背景:**
- 所有 LLM 都有上下文窗口限制
- 传统做法: 简单截断旧消息 / 滑动窗口
- 缺陷: 丢失关键上下文 (进行中的任务状态、决策理由、承诺)

**创新做法:**

```
消息序列 → 自适应分块 → 工具调用配对保护 → 分阶段总结 → 合并 → 标识符保留
```

核心参数:
- `BASE_CHUNK_RATIO = 0.4` -- 保留 40% 上下文
- `MIN_CHUNK_RATIO = 0.15` -- 最少保留 15%
- `SAFETY_MARGIN = 1.2` -- 20% 安全余量 (token 估算不精确)

**三个精妙设计:**

1. **工具调用配对保护** (`repairToolUseResultPairing`): 压缩时绝不把 `tool_use` 和 `tool_result` 分开，避免 LLM 看到孤立的工具结果
2. **自适应分块** (`computeAdaptiveChunkRatio`): 当单条消息很大 (>10% 上下文) 时自动调低 chunk ratio，防止一条大消息撑爆整个保留区
3. **标识符完整保留**: UUID、hash、IP、URL 在总结中原样保留，不截断不重构 -- 这对后续工具调用至关重要

**总结指令中的关键要求:**
```
必须保留:
- 活跃任务及其状态
- 批处理进度
- 最后一次用户请求
- 决策理由
- TODO/开放问题/约束条件
- 承诺或后续行动
```

**代价:** 每次 compaction 需要一次额外 LLM 调用 (生成总结)，增加成本和延迟

#### v1.2 新增 🆕：Mid-turn compaction precheck + Post-compaction loop guard

- 🆕 **Mid-turn compaction precheck** (PR #73499)：在一轮 LLM 调用即将溢出 token budget 时，先做一次抢占式 compaction precheck，避免到 attempt loop 末端才发现溢出。
- 🆕 **Post-compaction loop guard** (`src/agents/pi-embedded-runner/post-compaction-loop-guard.ts`)：防止 compaction 之后 Agent 仍然立即触发又一次 compaction 形成死循环。配置 schema 校验在 `src/config/zod-schema.post-compaction-guard.test.ts`。
- 🆕 **GPT-5.5 Codex 上下文按 Codex runtime context window 算 compaction**（Fix #82982）：之前用宿主上下文窗口偏大，导致 Codex native 段超限。

---

### 亮点3: MCP + ACP 双协议架构 -- 工具标准化 + Agent 会话化 ✅ ♻️ v1.2 ACP 加 UNAVAILABLE failover + Codex 深度绑定

**问题背景:**
- MCP (Model Context Protocol) 解决了工具发现和调用的标准化，但它是**无状态的**
- 真正的 Agent 需要**会话管理、权限控制、状态同步** -- MCP 不够用

**创新做法: MCP 管工具，ACP 管会话**

```
┌──────────────────────────────────────────────────┐
│                    Agent 执行循环                  │
│                                                   │
│  ┌─────────┐    ┌─────────┐    ┌──────────────┐  │
│  │ 内置工具  │    │ 插件工具  │    │  MCP 工具     │  │
│  │ read/exec│    │ 自定义    │    │ 外部 MCP 服务 │  │
│  └────┬─────┘    └────┬─────┘    └──────┬───────┘  │
│       └───────────────┼─────────────────┘          │
│                       v                            │
│              Tool Policy Pipeline                  │
│         (多层 allow/deny 策略叠加)                  │
└──────────────────────────────────────────────────┘
         ^                              ^
         │ ACP (会话协议)                │ MCP (工具协议)
         │ ndJson over stdio           │ stdio/SSE/HTTP
┌────────┴────────┐           ┌────────┴────────┐
│  IDE/CLI Client  │           │  外部 MCP Server │
│ (VSCode/Terminal)│           │ (数据库/API/...)  │
└─────────────────┘           └─────────────────┘
```

**MCP 架构要点:**
- 三种传输: Stdio (子进程) / SSE / Streamable HTTP
- 插件通过 manifest 声明 MCP 服务器配置 (`mcpServers`)
- 工具名称空间化: `serverName:toolName` 避免冲突
- Per-session MCP runtime + 10 分钟 idle TTL + Lease 保活
- 安全边界: 所有 MCP 工具都包装 `before_tool_call` Hook

**ACP 架构要点:**
- 完整会话生命周期: `newSession` → `prompt` → `cancel` → `loadSession` → `close`
- Actor Queue 模式: 每个 session 一个 actor，序列化操作防竞态
- 事件映射: Gateway 事件 <-> ACP 通知 (chat/tool_call/session_update)
- 持久绑定: ACP session 可绑定到 Discord/Telegram 等外部渠道
- 溯源追踪: `off` / `meta` / `meta+receipt` 三级模式

**MCP vs ACP 定位:**

| 维度 | MCP | ACP |
|------|-----|-----|
| 核心功能 | 工具发现与调用 | 完整 Agent 会话控制 |
| 传输 | stdio/HTTP | ndJson over stdio |
| 状态 | 无状态 | 完整会话生命周期 |
| 方向 | Agent -> 外部工具 | IDE/CLI -> Agent |
| 典型场景 | 数据库查询、API 调用 | VSCode 集成、终端交互 |

#### v1.2 新增 🆕：ACP backend provider failover + Codex App-Server 深度绑定

- 🆕 **ACP backend provider failover for UNAVAILABLE errors** (PR #69542)：ACP 后端在 UNAVAILABLE 时自动切换到候选 provider，与现有 model failover 链对齐。
- 🆕 **Codex App-Server 深度绑定**：context-engine projections 通过 thread_bootstrap epoch 绑定到 Codex threads (PR #82351)；native Codex 工具调用全部录入 trajectory 导出；Codex OAuth 与 sidecar profile 双栈兼容；oversized Codex thread 在 resume 前 rotate（Fix #82981）。
- 🆕 **ACP 终结型 turn 结果**：失败的 Codex/acpx 运行不再被仅凭进度文本误判为成功（Fix #79522）。

---

### 亮点4: SubAgent 编排 -- 没有 DAG，只有 Spawn/Announce/Steer ✅ ♻️ v1.2 多处可靠性补强

**问题背景:**
- 主流方案 (LangGraph) 用 DAG 编排多 Agent
- 缺陷: DAG 在编译时确定拓扑，难以处理动态涌现的子任务

**创新做法: 运行时 Spawn + 异步 Announce**

```
Parent Agent                     Child Agent
    │                                │
    │── spawn(task, mode, context) ──>│
    │                                │── 独立 session 运行
    │                                │── 可以再 spawn 子 Agent
    │<── announce(result) ───────────│
    │                                │
    │── steer(instruction) ─────────>│  (动态调整)
    │                                │
```

**Spawn 参数设计 -- 精细控制每个子 Agent:**
- `mode`: `run` (一次性) vs `session` (持久)
- `context`: `isolated` (干净) vs `fork` (复制父对话)
- `sandbox`: `inherit` (共享) vs `require` (隔离)
- `cleanup`: `delete` (完成后删除) vs `keep` (保留)
- 深度限制 + 并行数限制，防止无限递归

**孤儿恢复 -- 真正生产级的考虑:**
当 Gateway 收到 SIGUSR1 重载信号时:
1. 扫描所有 `abortedLastRun: true` 的 session
2. 读取原始任务上下文
3. 发送合成的恢复消息: "你的上一轮被网关重载中断了，原始任务是..."
4. 指数退避重试 (最多 3 次)

**代价:** 40+ 文件的复杂度，调试分布式子 Agent 生命周期困难

#### v1.2 新增 🆕：spawn 注册写入屏障 + sandbox-peer 控制器路由 + announce loop guard

- 🆕 **spawn 注册写入屏障**（PR #83146）：subagent registry 首次保存成功之前不报告 spawn accepted，registry 写失败直接返回 spawn error，避免未跟踪的孤儿 run。
- 🆕 **sandbox-peer 控制器所属保留 + 完成路由回原 session**（Fix #80201）：subagent 控制权与完成投递被严格按"发起 run session"分发。
- 🆕 **keep-mode 完成 payload 在 final-delivery retry 耗尽后保持 pending**（Fix #82583）：requester 恢复仍可拿到最终结果。
- 🆕 **`subagent-registry.announce-loop-guard`** 单元保护：防止 announce 走入循环。
- 🆕 **subagent_spawning hook** 加完成投递路由感知（group/channel 完成可强制 message-tool-only handoff，Fix #82803）。

---

### 亮点5: 系统提示工程 -- 不是模板，是编译器 ✅ ♻️ v1.2 工具描述精简 + 工具描述符规划器

**问题背景:**
- 大多数 Agent 框架的 system prompt 是一个字符串模板
- 缺陷: 不可组合、不可测试、不可缓存

**创新做法: 分段组装 + 缓存分区 + Provider 覆写**

System prompt 通过 `buildAgentSystemPrompt()` (~1000 行) 按严格顺序组装 20+ 个 section:

```
[Identity] → [Tooling] → [Safety] → [CLI Reference] → [Skills Catalog]
    → [Memory] → [Self-Update] → [Model Aliases] → [Workspace]
    → [Bootstrap Context] → [Heartbeat]
    
    ─── CACHE_BOUNDARY ───  ← 这条线之上的所有内容都是 byte-identical
    
    → [Dynamic Context] → [Channel-specific] → [Group Context]
    → [Reactions] → [Provider Dynamic] → [Runtime Info]
```

**三个精妙设计:**

1. **三种 Prompt Mode**: `full` (主 Agent, 全量) / `minimal` (子 Agent, 仅工具+工作区+运行时) / `none` (仅一句话)
2. **Provider Section Override**: 模型提供商可以**整体替换** interaction_style / tool_call_style / execution_bias 三个 section
3. **Skills 三级降级**: Full format (名称+描述+路径) -> Compact format (名称+路径) -> 二分搜索截断 (部分列表)。预算默认 18,000 字符 ♻️ v1.2: SKILL.md 总数已达 101 (30 顶层 + 71 插件捆绑)，cache boundary 常量名 `SYSTEM_PROMPT_CACHE_BOUNDARY = "<!-- OPENCLAW_CACHE_BOUNDARY -->"` 仍位于 `src/agents/system-prompt-cache-boundary.ts`；`buildAgentSystemPrompt` 仍位于 `src/agents/system-prompt.ts:665`

#### v1.2 新增 🆕：Tool Descriptor Planner + 工具描述全面精简 + Per-agent bootstrap profiles

- 🆕 **Tool Descriptor Planner** (`feat: add tool descriptor planner`)：在 prompt 编译期为每个工具计算最优描述符（按可用性 / 调用频率 / 上下文相关性裁剪），与"内建工具描述全面精简"(media / messaging / sessions / cron / Gateway / web / image-PDF / TTS / nodes / plan tools) 协作。
- 🆕 **Per-agent bootstrap profiles**：agents.defaults 可按 agent 分别定制 bootstrap 文件加载（之前只能全局）。
- 🆕 **`skipOptionalBootstrapFiles` config**（PR #62110）：允许跳过非必需 bootstrap 文件以节省 token。
- 🆕 **i18n locale 注入**：wizard / 渠道安装向导按 en / zh-CN / zh-TW 三语动态注入 prompt。
- 🆕 **deterministic tool payload ordering for prompt-cache reuse**（OpenAI Responses + chat completions 双路径，PR #82940）。

---

### 亮点6: Memory System -- 单槽位 + Hybrid Search + 预 Compaction Flush ✅ ♻️ v1.2 加熔断 + 中文 trigger + 人物 wiki

**问题背景:**
- 多个 Memory 后端同时激活容易冲突
- 纯向量搜索对关键词查询效果差

**创新做法:**

**单槽位设计**: 同时只有一个 Memory 插件激活，通过 `config.plugins.slots.memory` 切换。消除了多后端竞争。

**Hybrid Search 流水线:**
```
Query → [向量搜索 (0.7 权重)] + [关键词搜索 (0.3 权重)]
    → 分数融合
    → 时间衰减 (半衰期 30 天)
    → MMR 多样性重排 (可选, lambda=0.7)
    → Top-K 返回 (默认 6, 最低分 0.35)
```

**预 Compaction Memory Flush:**
在 compaction 触发前，先把对话摘要**写入持久化文件** (`memory/YYYY-MM-DD.md`)。这样即使 compaction 丢失了细节，memory 文件中仍然保留。

**QMD (Query-Memory-Decide) 模式:**
不只是"检索-返回"，而是"检索-记忆-决策"。Agent 通过 system prompt 被引导在回答问题前**主动搜索记忆**:
```
Before answering anything about prior work... run memory_search...
```

#### v1.2 新增 🆕：Active Memory 熔断 + LanceDB CJK + Memory Wiki 人物元数据

- 🆕 **Active Memory 超时熔断**（PR #74158）：`extensions/active-memory` 在连续多次 recall 失败后短时间内自动跳过 recall，避免拖垮整个 attempt loop。
- 🆕 **memory-lancedb 支持中文 memory trigger keywords**（PR #70040）+ **memory-lancedb llm CLI 接 `query` 命令**（PR #71112）。
- 🆕 **memory-wiki agent-facing people wiki metadata**（PR #82749 类同）：把人物条目的元数据暴露给 Agent，便于 QMD 模式下定向召回。
- 🆕 **memory-core 启动期 incremental dirty 标记**（Fix #82341）：扫描持久 source session，只把缺失/更新/变形文件标 dirty，避免每次启动全量重扫。
- 🆕 **memory-core 区分 sqlite-vec 加载失败 vs 缺失语义向量维度**（Fix #75624）：诊断信息更精准。
- 🆕 **QMD 词法搜索保留原始连字符查询**（Fix #81328）：避免破折号被规范化成空白导致词法 fallback。

---

## 可学习的模式

### 模式1: Tool Policy Pipeline -- 多层策略叠加 ✅

**解决的问题:** 在复杂系统中，工具权限需要从多个维度控制 (全局、Provider、Agent、Group)，简单的角色-权限模型不够用。

**核心做法:**
```typescript
// 策略按顺序叠加，每层可 allow/deny
const steps = [
  tools.profile,              // 1. Profile 级别
  tools.byProvider.profile,   // 2. Provider Profile 级别
  tools.allow,                // 3. 全局允许列表
  agents.{id}.tools.allow,    // 4. Agent 级别
  group.tools.allow,          // 5. Group 级别
];
// 最终取交集
```

**适用场景:** 任何需要多级权限控制的系统 (API 鉴权、Feature Flag、内容审核)

**注意事项:** Pipeline 顺序很重要，文档化每层的语义

---

### 模式2: Auth Profile 轮换 + Cooldown ✅ ♻️ v1.2: `src/provider-runtime/operation-retry.ts` 启动 provider 重试 helper 统一入口

**解决的问题:** 单个 API Key 会被限流，导致整个 Agent 不可用。

**核心做法:**
```typescript
// 多个 Auth Profile 组成候选池
const profiles = resolveAuthProfileOrder(provider);

for (const profile of profiles) {
  if (isInCooldown(profile)) continue;  // 跳过冷却中的
  
  try {
    return await callLLM(profile);
  } catch (e) {
    markFailure(profile, classifyReason(e)); // rate_limit/auth/billing/overloaded
    setCooldown(profile, backoff);
  }
}
```

**适用场景:** 任何依赖第三方 API 且需要高可用的系统

**注意事项:** Cooldown 时间需要按失败原因区分 (限流 30s vs 账单错误 24h)

---

### 模式3: 架构边界脚本化守护 ✅

**解决的问题:** 架构决策被写在文档里，但代码里没人遵守。

**核心做法:**
```bash
# scripts/check-architecture-smells.mjs
# 扫描所有 import 语句，检测:
# - 扩展直接引用核心内部模块 (应通过 plugin-sdk)
# - 核心深入引用扩展内部 (应通过 api.ts)
# - 扩展之间互相引用

# scripts/check-extension-plugin-sdk-boundary.mjs  
# 确保 extensions/ 只 import from 'openclaw/plugin-sdk/*'
```

在 CI 中作为必须通过的 gate 运行。

**适用场景:** 任何有明确模块边界的项目 (微服务间、SDK 与内部实现间)

**注意事项:** 脚本需要随架构演进而更新

---

### 模式4: Changed Lanes CI 加速 ✅ ♻️ v1.2: 配合 **Tideclaw alpha long gates (advisory)** + **QA-Lab runtime parity tiers** 形成"快速 lane + 阻塞 release-check + 软门 alpha gate"三段式

**解决的问题:** 8,000+ 文件的 monorepo，每次 PR 跑全量 CI 太慢。

**核心做法:**
```
git diff → 分析影响的文件 → 映射到 lane:
  - core prod 变更 → core typecheck + core tests
  - extension prod 变更 → extension typecheck + extension tests  
  - public SDK 变更 → extension prod/test 也要跑
  - 未知变更 → all lanes
```

**适用场景:** 任何大型 monorepo (100+ 个子项目)

**注意事项:** 需要维护准确的 "文件 -> lane" 映射关系

---

### 模式5: 懒加载模块分支 ✅ ♻️ v1.2: `pnpm check:import-cycles` + 架构 smell 检查持续 green；CLI subcommand `--help` 也被刻意保持轻量（fix #83228）

**解决的问题:** 同一个包既要当 CLI 工具又要当可编程库，但 CLI 路径不需要所有重型依赖。

**核心做法:**
```typescript
// src/index.ts
if (isMainModule()) {
  // CLI 路径: 极轻, 只加载 CLI 解析器
  const { runMain } = await import("./cli/run-main.js");
  await runMain();
} else {
  // 库路径: 导出完整 API
  export { Gateway } from "./gateway/index.js";
  export { Agent } from "./agents/index.js";
}
```

**适用场景:** 任何双用途 Node.js 包 (CLI + Library)

---

### 模式6: Prompt Cache Boundary 分区 ✅ ♻️ v1.2 增强：Context Engine 新增 `ContextEnginePromptCacheInfo` 直接暴露 cache 是否被打破、被什么打破 (`code: cacheRetention | model | streamStrategy | systemPrompt | tools | transport`)

**解决的问题:** LLM 调用成本高，system prompt 前缀的 KV Cache 命中率直接影响成本。

**核心做法:**
```
System Prompt:
  [稳定内容 -- 所有列表确定性排序]
  <!-- OPENCLAW_CACHE_BOUNDARY -->
  [动态内容 -- 每轮变化的部分]
```

**适用场景:** 任何高频调用 LLM 的系统

**注意事项:** 需要配合所有集合类型 (Map/Set/Array) 的稳定排序

---

## 架构全景图

```
                        ┌─────────────────────────────────────────────┐
                        │              入口层 (Entry)                  │
                        │  entry.ts → compile-cache → isMainModule()  │
                        └──────────┬──────────┬──────────┬────────────┘
                                   │          │          │
                    ┌──────────────┘          │          └──────────────┐
                    v                         v                         v
           ┌───────────────┐      ┌────────────────┐      ┌────────────────┐
           │  Gateway Server│      │  Control UI    │      │ Companion Apps │
           │  (Hono HTTP/WS)│      │  (React/Vite)  │      │(macOS/iOS/And) │
           └───────┬───────┘      └───────┬────────┘      └───────┬────────┘
                   │                      │                        │
                   └──────────────────────┼────────────────────────┘
                                          v
        ┌─────────────────────────────────────────────────────────────────┐
        │                   Agent 执行循环 (PI Embedded Runner)            │
        │                                                                 │
        │  enqueue → workspace → plugins → hooks → harness → model       │
        │                                                                 │
        │  ┌──────────────────────────────────────────────────────────┐   │
        │  │              重试循环 (Attempt Loop)                      │   │
        │  │  auth profile → build payload → LLM call → tool loop    │   │
        │  │  → failover → compaction → retry                        │   │
        │  └──────────────────────────────────────────────────────────┘   │
        │                                                                 │
        │  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌─────────────────┐  │
        │  │ System   │  │ Context │  │  Memory  │  │   SubAgent     │  │
        │  │ Prompt   │  │ Engine  │  │  System  │  │   Registry     │  │
        │  │ Builder  │  │ (可插拔) │  │ (单槽位)  │  │ (spawn/steer/ │  │
        │  │ (20+段)  │  │         │  │          │  │  announce)     │  │
        │  └─────────┘  └─────────┘  └──────────┘  └─────────────────┘  │
        └───────────┬────────┬───────────┬────────────┬──────────────────┘
                    │        │           │            │
         ┌──────────┘   ┌────┘      ┌────┘       ┌────┘
         v              v           v             v
   ┌──────────┐  ┌───────────┐ ┌────────┐  ┌───────────┐
   │ Channels │  │   Tools   │ │  MCP   │  │    ACP    │
   │ (20+渠道) │  │ (文件/执行/ │ │ (工具  │  │ (会话协议) │
   │ Telegram │  │  Web/媒体) │ │  协议)  │  │ IDE/CLI  │
   │ Discord  │  └─────┬─────┘ └───┬────┘  └───┬───────┘
   │ Slack... │        │           │            │
   └────┬─────┘        v           v            v
        │        ┌──────────────────────────────────┐
        │        │       Plugin SDK 契约层            │
        │        │   openclaw/plugin-sdk/*            │
        │        │   (注册/钩子/类型/生命周期)          │
        │        └──────────────┬───────────────────┘
        │                       │
        v                       v
   ┌─────────────────────────────────────────────────┐
   │              Extensions (131 个插件)              │
   │                                                   │
   │  Providers: anthropic, openai, google, ollama...  │
   │  Channels: telegram, discord, slack, imessage...  │
   │  Tools: diffs, memory-core, memory-lancedb...     │
   │  Services: cron, doctor, canvas, nodes...         │
   └───────────────────────────────────────────────────┘
```

### v1.2 新增：媒体生成 + 实时语音集群 🆕

```
┌───────────────── Media Pipeline (统一 async task lifecycle) ─────────────────┐
│   image_generate ─┐                                                          │
│   music_generate ─┼─► task: status / dedupe / message-tool completion handoff│
│   video_generate ─┘                                                          │
│                                                                              │
│   realtime-transcription ◄─► voice-call (Telnyx Media Streaming) ◄─► talk    │
│   speech-core / tts-local-cli / azure-speech / deepgram / senseaudio /       │
│   elevenlabs / fal / runway / minimax / together-v2-video                    │
│                                                                              │
│   src/talk/ (Agent-to-Agent consult + talkback + audio-codec)                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### v1.2 新增：插件分发新通路 ClawHub 🆕

```
本地 openclaw doctor / onboard ─────► clawhub registry ─────► clawpack artifact
                                          │                       │
                                          ├─► typed security report
                                          └─► storepack metadata 持久化
                              (bundled cutover 也优先走 clawhub)
```

### v1.2 新增：QA-Lab 正式发布闸 🆕

```
openclaw qa suite --pack {personal-agent | runtime-parity | ...}
       │
       ├─► runtime parity tiers: standard │ optional │ live-only │ soak
       │   (GPT-5.5 ⇄ Claude Opus 4.7 基准对比)
       ├─► runtime tool fixture coverage  ──► openclaw qa coverage --tools
       ├─► qa-channel (redacted tool-start traces 进入 QaBusMessage)
       └─► release-check 阻塞门 + Tideclaw alpha long-gate (advisory)
```

### v1.2 新增：Plugin State + Commitments + ProviderRuntime 🆕

```
┌────────── Persistence ─────────┐    ┌──────── Self-tracking ─────────┐
│ src/plugin-state/              │    │ src/commitments/                │
│   sqlite store +               │    │   extraction → store → 心跳策略  │
│   path / permissions isolation │    │   (Agent follow-up 主动跟踪)    │
└────────────────────────────────┘    └─────────────────────────────────┘
              │                                    │
              └──────── src/provider-runtime/ ─────┘
                       (operation-retry helper)
```

### 系统架构图 (draw.io)

> 完整 6 页架构图源文件: [[openclaw-architecture.drawio]] ♻️ v1.2 已 patch（标题版本号、Plugin State / Commitments / ClawHub / Media Pipeline / Tool Descriptor Planner / mid-turn precheck / post-compaction loop guard 等新节点已加入对应图）

**P1. 系统整体架构 (7 层分层)**
![[openclaw-arch-p1-overview.png]]

**P2. Agent 执行循环 (PI Embedded Runner 完整流程)**
![[openclaw-arch-p2-agent-loop.png]]

**P3. MCP + ACP 双协议架构**
![[openclaw-arch-p3-mcp-acp.png]]

**P4. Memory + RAG + Context Engine**
![[openclaw-arch-p4-memory-rag.png]]

**P5. System Prompt 编译器 (Cache Boundary 架构)**
![[openclaw-arch-p5-prompt.png]]

**P6. Hook 系统 (4 种执行模式) + 插件生命周期**
![[openclaw-arch-p6-hooks.png]]

**模块职责一句话说明:**
- **Entry**: 极轻启动器，compile-cache + 环境检测 + 按需加载
- **Gateway**: HTTP/WS 服务器，认证、会话路由、事件分发
- **Agent 执行循环**: 核心推理引擎，attempt-retry-failover-compaction 闭环
- **System Prompt Builder**: 20+ section 分段组装，cache boundary 分区
- **Context Engine**: 上下文生命周期 (bootstrap/ingest/assemble/compact/maintain)
- **Memory System**: 单槽位插件，Hybrid Search (向量 0.7 + 关键词 0.3)
- **SubAgent Registry**: 子 Agent 全生命周期 (spawn/steer/announce/orphan-recovery)
- **MCP**: 工具协议层，stdio/SSE/HTTP 传输，per-session runtime
- **ACP**: 会话协议层，IDE/CLI 集成，actor queue 序列化
- **Plugin SDK**: 核心与扩展的唯一契约面，~400 文件
- **Extensions**: 131 个插件，in-tree 管理，每个有 manifest + code

**为什么这样划分?**
- **Gateway vs Agent**: 网络关注点与推理关注点分离，Gateway 可以独立升级协议
- **Core vs Extensions**: 微内核哲学，核心不知道任何具体插件
- **MCP vs ACP**: 工具 (无状态) 和会话 (有状态) 是根本不同的协议需求
- **Context Engine vs Memory**: 短期上下文管理和长期记忆存储是两个独立的关注点，但通过 assemble() 在推理时协作

---

## 深度专题: Agent 编排设计 ✅ ♻️ v1.2 attempt loop 增 mid-turn precheck + post-compaction loop guard

### 执行循环详解

```
1. enqueueSession(sessionKey)        ← 会话级排队
2. enqueueGlobal(lane)               ← 全局级排队
3. resolveRunWorkspaceDir()           ← 工作区解析
4. ensureRuntimePluginsLoaded()       ← 插件热加载
5. Hook: before_agent_reply           ← 可拦截整个请求
6. selectAgentHarness()               ← 选择执行后端 (PI/Plugin)
7. resolveModelAsync()                ← 模型解析 (含 failover 链)
8. ═══ Auth Profile Rotation Loop ═══
   8a. 选择 profile candidate
   8b. buildEmbeddedRunPayloads()     ← 构建完整 payload
       - buildAgentSystemPrompt()     ← 系统提示组装 (20+ sections)
       - Context Engine assemble()    ← 上下文组装 (token budget)
       - Tool definitions             ← 工具定义序列化
   8c. LLM API 调用 (streaming)
       - subscribeEmbeddedPiSession() ← 流式分块处理
       - EmbeddedBlockChunker        ← 按段落/代码块边界分段
       - Tool Loop                    ← 工具调用 → 结果 → 继续推理
   8d. 结果分类:
       ✓ 成功 → 返回
       ✗ Empty Response → retry with instruction
       ✗ Context Overflow → compaction → retry
       ✗ Rate Limit → profile rotation / backoff
       ✗ Auth Error → mark failure → next profile
       ✗ Timeout + token>65% → compaction → retry
       🆕 Mid-turn 抢占式 compaction precheck (PR #73499)：在 8c 流式中段就识别可能溢出，提前压缩
       🆕 Post-compaction loop guard：刚 compaction 完又触发 compaction 时阻断，避免死循环
   8e. Compaction (if needed)
       - Memory Flush (预 compaction 持久化)
       - generateSummary (分阶段总结)
       - Tool call pairing repair
       🆕 Codex 通道用 Codex runtime context window 算阈值 (Fix #82982)
   8f. SubAgent 交互 (if tool calls spawn)
       🆕 spawn 注册写入屏障 + sandbox-peer 控制器路由 + keep-mode payload pending
9. ═══ 循环结束 ═══
10. return EmbeddedPiRunResult
```

### Harness 抽象 -- 可插拔的 Agent 后端

```typescript
interface AgentHarness {
  id: string;
  supports(provider, model): boolean;  // 能否处理这个请求
  runAttempt(params): Promise<Result>;  // 执行一次推理
  compact(params): Promise<void>;       // 压缩上下文
  reset(params): Promise<void>;         // 重置状态
}

// 选择逻辑:
// pinned > forced_plugin > auto_plugin > auto_pi_fallback
// auto 模式按 priority 排序候选者
```

### Hook 系统 -- 40+ 个精细切面

**四种执行模式:**

| 模式 | 语义 | 典型 Hook |
|------|------|----------|
| **Void** (并行，Fire-and-Forget) | 观察，不影响流程 | `message_sent`, `agent_end`, `model_call_started` |
| **Modifying** (顺序，结果合并) | 修改流程数据 | `before_prompt_build`, `before_tool_call`, `message_sending` |
| **Claiming** (顺序，First-Win) | 抢占式处理 | `before_agent_reply`, `inbound_claim`, `reply_dispatch` |
| **Sync** (同步，热路径) | 零延迟变换 | `tool_result_persist`, `before_message_write` |

**关键 Hook 的用途:**

- `before_agent_reply`: 插件可以完全拦截请求，返回合成回复 (不走 LLM)
- `before_prompt_build`: 注入额外系统上下文 / 修改 system prompt
- `before_tool_call`: 修改/阻止工具调用参数 (安全边界)
- `before_model_resolve`: 动态切换 Provider/Model
- `subagent_spawning`: 在子 Agent 创建前修改参数 (如绑定到线程)

---

## 深度专题: Memory + RAG 设计 ✅ ♻️ v1.2 active-memory 熔断 + LanceDB CJK + 启动期 incremental dirty

### Hybrid Search 流水线

```
用户查询 "上周讨论的 API 方案"
    │
    ├── 向量搜索 (语义相似度, 权重 0.7)
    │     └── 嵌入模型: OpenAI/Voyage/Ollama/本地 ONNX
    │
    ├── 关键词搜索 (精确匹配, 权重 0.3)
    │     └── SQLite FTS + CJK 分词 + 停用词过滤
    │
    └── 分数融合: score = 0.7*vector + 0.3*keyword
         │
         ├── 时间衰减 (半衰期 30 天, 近期优先)
         │
         ├── MMR 多样性重排 (可选, Jaccard 相似度)
         │     └── MMR = lambda*relevance - (1-lambda)*max_sim_to_selected
         │
         └── Top-6 返回 (最低分 0.35)
```

### Memory Flush 设计

```
对话积累 → 超过 softThresholdTokens
    │
    ├── 构建 Flush Plan:
    │     - 目标文件: memory/YYYY-MM-DD.md
    │     - 系统指令: "提取关键信息，保留标识符"
    │     - 用户提示: "总结对话要点"
    │
    ├── Agent 执行 Flush Turn (额外一轮 LLM 调用)
    │     └── 写入 memory/YYYY-MM-DD.md (append-only)
    │
    └── 然后才触发 Compaction
```

### 记忆注入 Prompt

Memory 插件通过 `buildPromptSection()` 向 system prompt 注入引导:
```
Before answering anything about prior work, context, or previous conversations,
run memory_search with a relevant query to find related information.

[Optional citation instructions based on citationsMode]
```

Agent 被引导**主动搜索**记忆，而非被动接收 -- 这确保了只在需要时才消耗 token。

### v1.2 新增 🆕：Active-Memory 熔断流水线

```
recall request ─► active-memory plugin ─► [timer + consecutive_failures]
                       │                          │
                       │                          ├─ N 次连续失败 ──► 短时间 skip recall
                       │                          └─ 成功 ──► 重置计数器
                       └─► 命中 ──► hybrid search 流水线 (同 v1.1)
```

避免一个失联的向量后端把整个 attempt loop 拖垮。

---

## 深度专题: Prompt 工程哲学 ✅ ♻️ v1.2 Tool Descriptor Planner + i18n + per-agent bootstrap

### 设计原则

1. **分段组合，不是模板**: Prompt 是 `string[]` 数组，每个 section 是独立函数，可测试、可条件化
2. **确定性第一**: 所有集合类型排序后再序列化，消除随机性
3. **缓存感知**: `CACHE_BOUNDARY` 是最重要的架构决策，分离静态和动态
4. **插件可扩展**: Provider 可以替换三个 section + 注入前缀/后缀
5. **Skills 懒加载**: 只在 prompt 中列目录，Agent 按需 read 具体 SKILL.md
6. **安全净化**: 所有不可信内容经过 `sanitizeForPromptLiteral()` (Unicode 控制字符/双向标记)

### Skills 三级降级策略

```
Skills 总量 → 预算 18,000 字符
    │
    ├── Tier 1: Full format (名称+描述+路径) -- 如果放得下
    │
    ├── Tier 2: Compact format (名称+路径, 无描述) -- 如果放得下
    │
    └── Tier 3: 二分搜索找最大前缀 -- "included X of Y" 警告
```

### Bootstrap Context 文件优先级

| 优先级 | 文件 | 用途 |
|--------|------|------|
| 10 | AGENTS.md | 工作区 Agent 配置规则 |
| 20 | SOUL.md | Agent 人格/语气 |
| 30 | IDENTITY.md | Agent 身份 |
| 40 | USER.md | 用户身份/偏好 |
| 50 | TOOLS.md | 工具使用指南 |
| 60 | BOOTSTRAP.md | 首次运行工作流 |
| 70 | MEMORY.md | 长期记忆 |
| 动态 | HEARTBEAT.md | 心跳任务 (在 cache boundary 之下) |

每个文件有 12,000 字符上限，总共 60,000 字符上限，超出按 75% 头部 + 25% 尾部截断。

### v1.2 新增 🆕：Tool Descriptor Planner + Per-agent bootstrap profiles + i18n 注入

- **Tool Descriptor Planner**：在 prompt 编译期为可见工具列表生成最优描述符（按可用性 / 调用频率 / 上下文相关性裁剪），配合"内建工具描述全面瘦身"（media/messaging/sessions/cron/Gateway/web/image-PDF/TTS/nodes/plan tools），把 system prompt 中工具部分的字节占用显著下压。
- **Per-agent bootstrap profiles**：agents.defaults 可以为每个 agent 单独配 bootstrap 文件清单，子 Agent / 不同人格 / 不同渠道可以走不同的"开机指令"。
- **`skipOptionalBootstrapFiles` config**（PR #62110）：跳过非必需 bootstrap 文件以省 token。
- **i18n locale 注入**：wizard / 渠道安装向导按 en / zh-CN / zh-TW 三语动态注入；UI i18n baseline report 守 locale 完整度。
- **Deterministic tool payload ordering**（PR #82940）：OpenAI Responses + chat completions 双路径都做了工具载荷的确定性排序，强化 prompt cache 命中。

---

## 对我的启发

### 如果我在做类似项目

**我会借鉴:**
1. **Cache Boundary 分区** -- 这是投入产出比最高的优化，5 行代码就能实现
2. **架构边界脚本化守护** -- 不依赖人的自觉，CI 自动检测越界
3. **Tool Policy Pipeline** -- 比 RBAC 更灵活的多层策略模型
4. **Context Engine 生命周期** -- 把上下文管理从 "一个函数" 升级为 "一组接口"
5. **Single-Slot Memory** -- 简单但有效，消除多后端竞争

**我会改进:**
1. **src/agents/ 拆分** -- 700+ 文件太重，可以按功能域拆为 sub-packages (harness/, subagent/, tools/, prompt/)
2. **SubAgent 调试工具** -- 40+ 文件的子系统需要专门的可视化/调试面板
3. **Context Engine 默认实现** -- 当前 legacy engine 是 pass-through，应该提供一个开箱即用的 "智能" 实现
4. **MCP/ACP 统一传输** -- 两套协议有重复的传输层代码，可以抽象出 common transport

### 这个项目教会我的 3 件事

1. **"生产级"的差距在于弹性设计**: 功能代码可能只占 30%，另外 70% 是 failover/retry/recovery/cooldown/orphan-cleanup。OpenClaw 的每一层都有自己的容灾策略，这才是真正可以 24/7 运行的系统
2. **Prompt 是需要"编译"的**: 不是拼字符串，而是分段组装、确定性排序、缓存分区、安全净化、预算管控。System prompt 的工程质量直接决定 LLM 调用的成本和效果
3. **架构边界的价值体现在规模上**: 128 个插件（v1.1 错记 131）、8,000+ 文件、20+ 贡献者 -- 在这个规模下，Plugin SDK 契约 + 脚本化守护不是 "nice to have"，而是 "项目能否存活" 的关键。没有边界，128 个插件会在 3 个月内把核心搅成一团泥

### v1.2 新增 🆕：本轮 3 周观察补的 3 件事

1. **"运营性能力"也能用同一套微内核搭载**：QA-Lab（runtime parity gates）、ClawHub（插件分发）、Autoreview（pre-land 强制评审）都不是核心 Agent 能力，但全部通过插件 + skill + script 一致表达。**这说明微内核架构的护城河比"代码隔离"更深 — 它让团队的工程文化也能被模块化沉淀**。
2. **多媒体集群"统一异步任务生命周期"是被低估的设计**：image / music / video 三个高度异质的生成任务被同一个 `status / dedupe / completion handoff` 流程吃下，意味着新增任意一种 "生成 X" 都是注册 provider + 复用生命周期；这种"长任务用同一份脚手架"的模式可以泛化到任意 SaaS 后台。
3. **Context Engine 已从"接口"演化成"框架"**：v1.2 的 `thread_bootstrap projection` + `transcript rewrite` + `prompt cache observation` 让 Context Engine 不再只是"组装上下文"，而是接管了整个长会话 + 持久 backend thread + cache 命中可观测的全链路。**对于任何要做长会话 Agent 的团队，这套接口的演进路径值得逐版精读**。

---
*分析时间: 2026-05-18 (v1.2) | 项目版本: 2026.5.17 | 基于 commit 816fbe0cf0 | 上一版基准: 2026-04-29 (v1.1, commit 492e2a3060)*
