---
title: "learn-claude-code 源码洞察"
aliases: [learn-claude-code, shareAI-lab/learn-claude-code, Harness Engineering for Real Agents]
tags:
  - opensource
  - source-analysis
  - claude-code
  - coding-agent
  - ai-skill
  - Python
  - harness-engineering
  - tutorial
github: https://github.com/shareAI-lab/learn-claude-code
created: 2026-05-14
updated: 2026-05-14
score: 4.2
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# learn-claude-code 源码洞察

## 一句话本质

> **learn-claude-code** 是一个把 Claude Code 的 harness 工程拆成 12 节最小可运行 Python 课时的教学型仓库（s01-s12 严格递进），它的核心价值是用 ~4400 行代码完整复刻 *Loop / Tool / Skill / Compact / Task / Subagent / Team / Worktree* 八大机制，让任何工程师都能在本地一节一节跑通、改透 Claude 的运行机制。

---

> 维度：T1 架构 / T2 设计理念 / A1 Agent 架构 / X1 快速收集。
> 配套学习计划由浅入深映射 Claude Code 真实机制：Agent Loop → Tool Use → Skill / Plugin / MCP → Memory → Context Compaction。

---

## 项目概览

| 项 | 值 |
|---|---|
| 名称 | learn-claude-code（shareAI-lab）|
| 类型 | **教学型仓库** — 把 Claude Code 的 harness 机制拆成 12 节可运行的最小代码 |
| 技术栈 | Python 3 + `anthropic` / `openai` SDK + `pyyaml` + `python-dotenv`；前端 Next.js（`web/`）|
| 规模 | `agents/` 目录 14 个文件、~4400 行 Python；docs/ 三语；web/ 配套站 |
| 模型后端 | 默认通过 `OPENAI_BASE_URL` 指向 Ollama（本地小模型可跑）；`s_full.py` 走 Anthropic 官方 |
| 运行方式 | 每节 `python agents/sXX_xxx.py` 是独立 REPL，输入提示词即可对话 |
| 课程结构 | s01→s12 严格递进，每节只在前节基础上加一个 harness 机制 |

**核心论点**（README.md:1-100）：
> *Agency comes from the model. Harness is what we build.*
> 智能不是代码堆出来的，是模型训出来的。我们的工作是给训好的模型造一辆"车"——工具、知识、上下文、权限边界。

---

## 维度 1 ｜ T1 架构模式

### 架构风格
**插件式分层单体（plugin-style layered monolith）**。每节文件都是同一骨架：

```
load_dotenv → client（LLM 客户端）→ SYSTEM 提示词
   → 工具实现函数 → TOOLS（JSON Schema 列表）+ TOOL_HANDLERS（dispatch map）
   → agent_loop(messages)：while tool_use 调 LLM、执行工具、回填结果
   → __main__ REPL
```

新机制不是"改架构"，而是"在 dispatch map 里挂新工具 + 在 loop 里挂新钩子"。

### 模块边界（agents/sXX 之间）
- 文件之间**不互相 import**，每节是自包含可执行脚本。这是教学优先的设计——读者只需读一个文件就懂一个机制。
- s_full.py（740 行）是"全集成参考实现"——把 s01-s11 所有机制并到一个文件，用 `# === SECTION: xxx ===` 标记分区。
- 共享面只有：`.tasks/`、`.team/`、`.transcripts/`、`.worktrees/` 这些**目录约定**——状态在文件系统里，不在进程内。

### 架构图（s_full.py 总图）

```
                          ┌─────────────────────────────────────┐
                          │           SYSTEM PROMPT             │
                          │  + Layer 1 skill descriptions       │  s05
                          │  + identity (s11 重新注入)          │
                          └──────────────┬──────────────────────┘
                                         │
   ┌─ before each LLM call ──────────────┼──────────────────────┐
   │  micro_compact (s06) — 替换旧 tool_result                   │
   │  auto_compact   (s06) — 超阈值时摘要全卷                    │
   │  drain bg notif (s08) — 把后台线程结果注入 messages         │
   │  check inbox    (s09) — 拉取队友消息                        │
   └─────────────────────────────────────────────────────────────┘
                                         │
                                ┌────────▼────────┐
                                │   client.chat   │
                                │  / messages.cr  │  agent loop（s01）
                                └────────┬────────┘
                                         │ tool_calls
                            ┌────────────┴────────────┐
                            │     TOOL_HANDLERS       │  s02 dispatch map
                            ├────────────────────────┤
                            │ bash / read / write    │  base
                            │ edit                   │  base
                            │ todo                   │  s03
                            │ task (subagent)        │  s04 fresh msgs
                            │ load_skill             │  s05 layer 2
                            │ task_create/list/get   │  s07 持久化 .tasks/
                            │ bg_run / bg_check      │  s08 线程
                            │ spawn_teammate / send  │  s09 .team/inbox
                            │ shutdown / plan        │  s10 协议
                            │ idle / claim_task      │  s11 自治
                            │ worktree_*             │  s12 .worktrees/
                            └─────────────────────────┘
```

### 扩展点
| 扩展点 | 在哪 | 怎么扩 |
|---|---|---|
| 新工具 | `TOOLS[]` + `TOOL_HANDLERS{}` | 加 schema + 加 lambda，agent loop 不动 |
| 新 skill | `skills/<name>/SKILL.md` | 写文件即可，`SkillLoader` 自动扫描（s05_skill_loading.py:60-69）|
| Loop 钩子 | agent_loop 顶部 `# before each LLM call` 区块 | 注册 pre/post 处理器 |
| 持久化状态 | `.tasks/` `.team/` `.worktrees/` 目录 | 文件即数据库；compact 不丢失 |

### 关键权衡
| 决策 | 收益 | 代价 |
|---|---|---|
| 每节自包含、不复用 | 阅读路径线性、可独立运行 | 文件间大量重复代码（safe_path / run_bash 复制 12 次）|
| 状态走文件系统不走内存 | 跨会话/跨压缩存活，多 agent 共享免费 | 并发要靠目录锁（s11 用 `_claim_lock`）|
| dispatch map 用 lambda | 极简、一眼看完 | 大型项目得换成类继承体系 |
| Ollama 默认 + Anthropic 可选 | 学习成本低、免 key 跑通 | s_full 才用真接口，前面用兼容层 |

### 可借鉴的 3 个架构想法
1. **dispatch map = 1 行注册新工具**（s02:93-98）。任何 LLM Agent 项目都能照搬。
2. **状态外置到目录**（s07 `.tasks/`、s09 `.team/`）。让上下文压缩可以激进。
3. **before-LLM-call 钩子链**（s_full.py）。compaction、bg drain、inbox 全在这一处串起来，单点扩展。

---

## 维度 2 ｜ T2 设计理念

### 核心原则（从源码反推）
1. **Loop 是不可触碰的圣物**。s02 注释直白点出：*"The loop didn't change at all. I just added tools."* 一切扩展都不修改 `while True: LLM(...) → execute → append`。
2. **不要塞 system prompt**。s05 文件级 docstring：*"Don't put everything in the system prompt. Load on demand."* Layer 1 名字 + Layer 2 按需 body，是 token 经济学的内核。
3. **状态不在内存里**。s07 docstring：*"State that survives compression -- because it's outside the conversation."* 内存里的东西 compact 之后会消失；文件不会。
4. **过程隔离 = 上下文隔离**。s04 子 agent 用 `messages=[]` 起步、共享文件系统、只回摘要——免费拿到 context isolation。
5. **快速失败但不静默**。每个工具都 return `f"Error: ..."` 字符串，把异常当数据回给模型，让模型自己重试。**不抛异常打断 loop**。

### 主张评分
| 方面 | 评分 | 证据 |
|---|---:|---|
| 约定优于配置 | **5/5** | `skills/<name>/SKILL.md`、`task_<id>.json`、`.team/inbox/<name>.jsonl` 全是约定 |
| 显式优于隐式 | **5/5** | 每节文件顶部一张 ASCII 图 + 一句 *Key insight*，所有"魔法"都画出来 |
| 灵活性 vs 简洁性 | **简洁压倒一切** | 没有抽象基类、没有插件框架，最长的 s_full 才 740 行 |
| 性能 vs 可读性 | **可读性碾压** | `estimate_tokens = len(str(messages)) // 4` —— 故意用粗糙估算（s06:60）|

### 错误理念
快速失败 + 字符串化 + 不打断模型。s05_skill_loading.py:101 是范例：

```python
return f"Error: Unknown skill '{name}'. Available: {', '.join(self.skills.keys())}"
```

错误信息**包含可选项**，让模型直接重试。不 raise，让 loop 继续转。

### 配置理念
- 单一 `.env` + 合理默认（`OLLAMA_BASE_URL` 默认 `http://localhost:11434/v1`）
- 没有 config schema、没有 `--flags`，所有参数硬编码在文件顶部（`THRESHOLD = 50000`、`KEEP_RECENT = 3`）。教学优先：你想改就改源码，看到值就懂含义。

### 理念总结（3 句话）
1. *做减法，不做加法*——每节只新增一个机制，旧机制原样不动。
2. *把状态钉在磁盘上*——内存是临时缓存，文件系统才是真相之源。
3. *把错误降级成数据*——不让 harness 替模型决策，让模型读到 Error: 自己重来。

**适合借鉴的项目**：任何想做 Agent 的人。这套理念是 *"不要把自己当 agent，把自己当 vehicle"* 的最佳示范。

---

## 维度 3 ｜ A1 Agent 架构

### Agent 核心
- **决策**：单一 LLM `client.chat.completions.create(...)`，用 OpenAI tool-calling 规范。无 ReAct 模板、无 CoT prompt 工程——*靠模型本能*。
- **感知**：`tool_result` 字符串，全是文本（甚至文件读出来都直接拼 `\n`）。
- **执行**：`subprocess.run(shell=True, ...)` 是宇宙的中心；其它都在它周围。
- **记忆**：`messages: list` 是工作记忆；`.tasks/` `.transcripts/` 是长期记忆。

### 决策机制
- **范式**：原生 tool-calling（不是 ReAct/Plan-Execute/Reflexion 的任何一种"框架"）。
- **Prompt 模板**：
  - System：一行身份 + 工具/skill 描述。
  - User：用户原话。
  - Assistant：可能含 `tool_calls`。
  - Tool：工具结果。
- s11 自治模式给"身份"加固——压缩后重新注入 `identity_block`，避免模型忘了自己叫什么。

### 工具系统（s02 是模板）
- **定义**：OpenAI JSON Schema（s02:100-109）。
- **注册**：`TOOL_HANDLERS = {name: lambda **kw: handler(**kw)}`（s02:93-98）。
- **路由**：`handler = TOOL_HANDLERS.get(tool_call.function.name); handler(**args)`。
- **安全**：`safe_path()` 防越界；`dangerous` 列表黑名单；`timeout=120` 兜底。
- **错误**：抛回字符串，不 raise。

### 记忆系统
| 层 | 实现 | 文件 |
|---|---|---|
| 短期 | `messages: list` | 进程内 |
| 微压缩 | 旧 tool_result → `[Previous: used X]` | s06:66-96 |
| 长期 | `.tasks/*.json`、`.team/inbox/*.jsonl` | 磁盘 |
| 全量摘要 | LLM 自摘要 + 替换 messages | s06:100-124 |
| 压缩前快照 | `.transcripts/transcript_<ts>.jsonl` | s06:103 |
| 压缩后身份 | `identity_block` 重新拼到 messages 前 | s11 |

**触发链**：
```
每轮 → micro_compact 静默压缩
    → estimate_tokens > 50000 → auto_compact 全摘要
    → 模型主动调 compact 工具 → 立即摘要
```

### 多 Agent 协作（s04 vs s09 vs s11）
| 模式 | 寿命 | 通信 | 控制权 |
|---|---|---|---|
| Subagent (s04) | 一次任务即销毁 | 仅返回最后文本 | 父调度 |
| Teammate (s09) | 持久线程 | `.team/inbox/<n>.jsonl` 追加 | 显式 send_message |
| Autonomous (s11) | 持久 + 自找活 | 同上 + 扫 `.tasks/` 自动 claim | 自驱（poll 5s, idle 60s 退出） |

### 执行循环控制
- s04 子 agent 安全限制：`for _ in range(30):`（防失控）。
- s11 idle 循环：`POLL_INTERVAL=5, IDLE_TIMEOUT=60`。
- s10 协议：`request_id` 关联 request/response，超时即 reject。

### 可借鉴 3 点
1. **Subagent = `messages=[]`**。这个 1 行的"过程隔离"思路太朴素也太对。
2. **任务持久 + 依赖图（blockedBy）**（s07_task_system.py:64-89）。完成 task N 时遍历清理所有 `blockedBy` 含 N 的——简单可靠。
3. **request_id 关联协议**（s10）。同一个机制套两个场景（shutdown / plan approval），可推广到任何"请求-响应"。

---

## 维度 4 ｜ X1 快速收集

### 巧妙技巧

| 想法 | 位置 | 复用方式 |
|---|---|---|
| dispatch map = 1 行加工具 | s02_tool_use.py:93-98 | 任何 tool-calling agent 直接照抄 |
| Skill 双层加载 | s05_skill_loading.py:83-102 | 任何"知识库 + Agent"项目；列表只放 metadata，请求时再拉 body |
| micro_compact 跳过 read_file | s06_context_compact.py:57, 92-94 | 通用经验：**引用类工具结果不要压**，命令类压掉无所谓 |
| 错误字符串化（不 raise） | 各文件 `run_*` | LLM Agent 通用：让模型读到 Error 自行重试 |
| 任务文件名编码 ID | s07_task_system.py:51-52 | 用文件名做主键 + `glob` 列表，免数据库 |
| 状态在文件系统 → compact 安全 | 全局 | 想做"无限会话"的 agent 必学 |
| `safe_path` 防越界 | s02_tool_use.py:39-43 | `is_relative_to(WORKDIR)` 一行搞定 sandbox |

### 有用抽象
- **SkillLoader**（s05:57-102）—— YAML frontmatter 解析 + lazy body 提供。可剥离成独立库。
- **TaskManager**（s07:44-115）—— 文件 JSON CRUD + 完成时清理依赖。可剥离。
- **MessageBus**（s09:76-、s11:79-）—— JSONL 追加 + 读后清空。可剥离成"基于文件系统的轻量队列"。
- **EventBus**（s12:80-）—— append-only 事件日志。

### 快速收获
- 🟢 **低投入高价值**：`safe_path`、错误字符串化、dispatch map 这三件套。任何 LLM 项目 5 分钟塞进去。
- 🟡 **中等投入**：把 `TaskManager` + `SkillLoader` 抽成自己的包，给后续项目复用。
- 🔴 **高投入高价值**：复刻 s_full.py 的 "before-LLM-call 钩子链 + compact + bg drain + inbox" 综合体——是真实 production agent 的内核。

---

## 综合评分

| 维度 | 评分(1-10) | 亮点 | 可改进 |
|---|---:|---|---|
| 架构清晰度 | 10 | 文件 = 课时 = 一个机制，零认知负担 | 各文件大量代码重复（教学权衡） |
| 设计理念 | 10 | "不替模型决策"贯彻到每个错误处理 | 配置硬编码不便实验扫参 |
| Agent 完备性 | 9 | s01-s12 涵盖 production agent 90% 机制 | 没演示 MCP / Hooks / 真实 streaming |
| 代码质量 | 8 | 命名清晰、注释精炼到一行画图 | 缺类型注解、错误吞得有点广 |
| 教学性 | 10 | ASCII 图 + Key insight + REPL 即时跑 | 中级读者会嫌略简 |
| 工程性 | 6 | 教学优先；并发用 `_claim_lock` 简化处理 | 真生产得加重试/限流/审计 |

---

## 核心收获

### 最值得借鉴的 3 个设计决策
1. **Loop 不动，dispatch 上挂** —— 把 agent 系统的"易变部分"和"不变部分"切干净。
2. **状态外置到文件系统** —— 让上下文压缩、子 agent、多机协作三件事一起免费成立。
3. **错误降级成数据** —— harness 不替模型做决策，把异常变成 LLM 能读懂的 prompt 输入。

### 最值得学习的 3 个代码模式
1. `TOOL_HANDLERS = { name: lambda **kw: handler(**kw) }` —— 极简工具路由（s02:93-98）。
2. SkillLoader 双层注入（s05_skill_loading.py:57-102）。
3. `micro_compact` 选择性压缩（s06_context_compact.py:66-96，按工具名 whitelist 决定要不要压）。

### 最值得复用的 3 个工具/脚本
1. `safe_path()` —— 6 行实现 sandbox。
2. `SkillLoader` —— 30 行实现 frontmatter skill 加载。
3. `TaskManager` —— 60 行实现"持久 + 依赖图 + 完成自动清依赖"。

---

# Claude 运行机制学习计划（由浅入深）

> 目标：通过本仓库源码 + Claude Code 实操，搞懂 Agent Loop / Tool Use / Skill / Plugin / MCP / Memory / Context Compaction 的真实实现。
>
> 阅读路径：每个阶段先读源文件（30 分钟）→ 跑实验（30 分钟）→ 对照真实 Claude Code 行为（30 分钟）。

## 阶段 0 ｜ 准备（半小时）

- [ ] `cp .env.example .env` 配好 OpenAI/Ollama base url 和 model id
- [ ] `pip install -r requirements.txt`
- [ ] 通读 README.md 第 1-300 行，吃透 *"Agency comes from the model. Harness = vehicle."*
- [ ] 看一遍 `agents/s_full.py:1-37` 的总图，建立全局心智模型

---

## 阶段 1 ｜ 最小内核（1 天）

### 目标
理解 *为什么 agent 只需要一个 while 循环*。

### 源码
- `agents/s01_agent_loop.py:85-116` —— 核心 loop（可以背下来）
- `agents/s02_tool_use.py:93-135` —— dispatch map + 多工具

### 实操
1. `python agents/s01_agent_loop.py`，输入 `列出当前目录最大的 5 个文件`，观察 `\033[33m$ ...\033[0m` 黄字看到模型实际跑的命令。
2. 在 s02 的 `TOOL_HANDLERS` 里加一个新工具 `glob_files(pattern)`，重启 REPL 测试。
3. 对照真实 Claude Code：开 `claude --dangerously-skip-permissions`（或正常模式），让它做同样任务，对比 tool 调用模式。

### 检查点
能不能 1 句话说清"agent 和普通 LLM 调用的区别"？答案：**就是把 tool_result 加回 messages 再调一次模型**。

---

## 阶段 2 ｜ 计划与子任务（半天）

### 目标
理解模型如何**自己**追踪进度、何时**应该**派子 agent。

### 源码
- `agents/s03_todo_write.py:50-80` —— TodoManager + nag reminder（"3 轮没更新就提醒"）
- `agents/s04_subagent.py:115-140` —— 子 agent = `messages=[]` 起步 + 仅回最后文本

### 实操
1. 跑 s03，让它做"清理项目里所有 .pyc 文件"，观察 todo 状态变化。
2. 跑 s04，要求 *"用 task 工具调研一下 agents/s06 的压缩策略"*，亲眼看父上下文如何保持干净。
3. 在 Claude Code 实际使用中观察：当你说"用 Explore agent 找 X"时，对应 `s04` 的 `run_subagent`。

### 检查点
- 子 agent 共享什么、不共享什么？
  → 共享文件系统/磁盘、不共享 messages。

---

## 阶段 3 ｜ Skill 加载（半天，对应你的"SKill 如何加载"问题）

### 目标
理解 Claude Code 的 Skill 是怎么"按需"进入上下文的。

### 源码
- `agents/s05_skill_loading.py:57-102` —— `SkillLoader._load_all` + `_parse_frontmatter`
- `skills/*/SKILL.md` —— 4 个真实示例（code-review / agent-builder / pdf / mcp-builder）

### 关键机制（直接对应真实 Claude Code）
| Layer | 内容 | 在哪 |
|---|---|---|
| 1 | 仅 name + description（~100 token/skill）| 注入 system prompt |
| 2 | SKILL.md 全文 body | 当模型调用 `load_skill(name)` 时通过 tool_result 返回 |

### 实操
1. 写一个新 skill：`skills/test-runner/SKILL.md`，frontmatter 里写 `name: test-runner` + `description: ...`，body 写"用 pytest 跑测试的步骤"。
2. 跑 s05，提问"帮我跑测试"，观察模型是否调 `load_skill("test-runner")`。
3. 在真实 Claude Code 里：
   - 你已经做过的事：把 `source-code-analyzer` 软链到 `~/.claude/skills/`（本仓库根 README 里的 skills 同理）。
   - 验证：本会话开头的 system-reminder 已显示 source-code-analyzer 进入了 available skills 列表——这正是 Layer 1。
   - 进一步：当 Claude 决定执行此 skill 时，它会读取 SKILL.md 的 body——这是 Layer 2（在 Claude Code 里靠 Read 工具把 SKILL.md 内容拉进上下文，等价于 s05 的 `get_content`）。

### 检查点
- 为什么不全塞 system prompt？
  → 10 个 skill × 2000 token = 20k 永久占用，绝大多数任务用不到。

### 延伸：Plugin 如何加载（本仓库未演示，但可类推）
Claude Code 的 plugin 机制更复杂，包含命令、agents、hooks、skills 的打包：
- `~/.claude/plugins/` 是用户级插件；`{repo}/.claude/plugins/` 是项目级。
- 加载流程相似：扫描目录 → 解析 manifest（plugin.json）→ 注入命令/skill/hooks 到 harness。
- 想读真实实现：参考 Anthropic 官方文档 `https://docs.claude.com/claude-code/plugins`。本仓库的"按目录约定 + frontmatter 解析"思路就是 plugin 加载机制的简化版。

---

## 阶段 4 ｜ 上下文压缩（1 天，对应"上下文压缩机制"）

### 目标
理解为什么 agent 能"无限对话"。

### 源码
- `agents/s06_context_compact.py:60-124` —— 三层压缩（micro / auto / manual）

### 关键机制
```
每轮：
  micro_compact(messages)            # 静默：把 KEEP_RECENT(3) 之前的非 read_file tool_result 替换成 "[Previous: used X]"
  if estimate_tokens > THRESHOLD:    # 50000 触发
    save .transcripts/<ts>.jsonl     # 全卷快照
    summary = LLM(summarize_prompt)
    messages = [{"role":"user", "content":"[Conversation compressed...] " + summary}]
模型主动调 compact 工具：
  立即走 auto_compact
```

### 实操
1. 跑 s06，故意让它 `cat` 几个大文件（每次贡献几 KB tool_result），观察 `[auto_compact triggered]` 是否触发。
2. 看 `.transcripts/transcript_*.jsonl`，确认完整历史在磁盘。
3. 真实 Claude Code 行为对照：当 Claude 在长会话中说 *"The system will automatically compress prior messages..."*——背后就是这套（更复杂的）逻辑。

### 检查点
- 为什么 `read_file` 的结果不被 micro_compact 压？
  → 引用类资料压了之后模型还得重读一遍，反而费 token。

---

## 阶段 5 ｜ 任务持久化（半天，对应"memory 如何管理"）

### 目标
理解"超出单次对话"的状态怎么管。

### 源码
- `agents/s07_task_system.py:44-115` —— TaskManager + 依赖图 + 完成时自动清依赖

### 关键机制（直接对应真实 Claude Code 的 TaskCreate/TaskUpdate/TaskList）
- 每个 task 一个 `task_<id>.json`，状态外置 → compact 不会丢。
- `blockedBy: [int]` 实现依赖图。
- 完成 task N 时遍历所有任务，从 `blockedBy` 里删 N。

### 实操
1. 跑 s07：`帮我做 4 件事，第 2、3 件依赖第 1 件`，看模型怎么用 task_create + blockedBy。
2. 中途按 Ctrl+C 退出，再 `python agents/s07_task_system.py`，让它 `task_list`——任务还在。
3. 真实 Claude Code 对照：本会话开头我用了 TaskCreate 建了 5 个任务，原理一致（持久 + ID 主键 + 状态机）。

### 检查点
为什么任务不放在 `messages` 里？
→ 放在 messages 里会被 auto_compact 摘掉、字符串化丢失结构。文件 JSON 永远精确。

### 延伸：Memory（自动记忆）如何工作
Claude Code 的 `memory/` 系统（`~/.claude/projects/.../memory/`）是更高一级的"任务持久化"：
- 内容**跨会话**而非跨压缩生效。
- 文件结构同样是 frontmatter + body（和 s05 的 SKILL.md、s07 的 task JSON 是同一个思路）。
- 加载时机：每次会话开头扫 MEMORY.md 索引，按需读具体 .md。
- 这就是"状态外置 + frontmatter 索引"思路在第三个场景（user/feedback/project/reference）的复用。

---

## 阶段 6 ｜ 后台与团队（1 天）

### 目标
理解 agent 如何不阻塞 + 多 agent 协作。

### 源码
- `agents/s08_background_tasks.py:46-110` —— 线程 + 通知队列
- `agents/s09_agent_teams.py:76-118` —— MessageBus（基于 JSONL inbox）
- `agents/s10_team_protocols.py:79-90` —— request_id 关联的协议

### 实操
1. s08：让模型 `background_run("sleep 30 && date")` 然后继续干别的事，观察"完成通知"是怎么在下一轮 LLM 调用前注入的。
2. s09：spawn 两个队友 alice/bob，各派活看 inbox 文件如何变化。
3. s10：跑 shutdown 协议，观察 request_id pending → approved 的状态流。

### 检查点
- s04 subagent 和 s09 teammate 区别？
  → 寿命：subagent 一次性、teammate 长期；通信：subagent 仅返回值、teammate 走 inbox。

---

## 阶段 7 ｜ 自治 + 工作树隔离（1 天）

### 目标
理解 *"agent 自己找活做"*，以及并行任务如何不互相踩。

### 源码
- `agents/s11_autonomous_agents.py:1-140` —— idle 循环 + 任务认领
- `agents/s12_worktree_task_isolation.py:1-100` —— `git worktree` 作为执行隔离

### 实操
1. s11：往 `.tasks/` 丢两个 unclaimed 任务，启动 teammate 看它自动 claim。
2. s12：让模型为某 task 分配 worktree、改文件、看磁盘上 `.worktrees/` 出现 + 主仓库不动。
3. 真实 Claude Code 对照：你看到的 `EnterWorktree` 工具就是 s12 的工业化版本。

---

## 阶段 8 ｜ MCP & 真实生态（1 天，对应"MCP 如何使用"）

> 注：本仓库**没有**直接演示 MCP（README.md:228 明说"Full MCP runtime details"是 *out of scope*）。但 skills/mcp-builder 教你如何写 MCP server。

### 推荐路径
1. **概念**：读 Anthropic 官方 MCP 介绍 `https://modelcontextprotocol.io/`。
2. **运行机制**：MCP = stdio/SSE 的 JSON-RPC 协议，把"服务器进程"暴露的 tool/resource/prompt 注册到 Claude Code 的 dispatch map。本仓库的 `TOOL_HANDLERS`（s02）就是 MCP 在客户端这一侧的简化映射。
3. **实操**：
   - `claude mcp list` 看当前已配的 MCP server。
   - 用本仓库的 `skills/mcp-builder/SKILL.md` 让 Claude 替你写一个最小 MCP server（比如查股价、查日历）。
   - 写完后 `claude mcp add ...` 注册，下个会话里你就会在 system reminder 看到新工具自动加进来。
4. **代码对照**：MCP 在本仓库类比是 *"远程的 TOOL_HANDLERS"*——你本地客户端只是个 thin proxy，实际逻辑在另一进程里跑。

### 检查点
- 为什么 MCP 比"自己写 Python 工具"好？
  → 进程隔离、语言无关、可独立部署/重启、可复用给其它 MCP-aware 客户端（不只 Claude Code）。

---

## 阶段 9 ｜ 综合实战（1-2 天）

### 实战题（任选）
1. **加一个工具**：在 `s_full.py` 里加 `web_search(query)` 工具，挂到 dispatch map，不改 loop。
2. **写一个 skill**：在 `skills/release-notes/SKILL.md` 写发布说明生成流程，让 Claude 用它生成 PR 描述。
3. **写一个 MCP server**：用 mcp-builder 写一个能查公司内部 wiki 的 MCP，并在真实 Claude Code 里调通。
4. **造一个 agent 团队**：用 s09+s10 起 2 个队友（reviewer/coder），用 inbox + plan_approval 完成一次小重构。

### 每完成一项，回答 3 个问题
- 我加的东西是 *Loop 改了* 还是 *Dispatch 改了*？（应该永远是后者）
- 我的状态是放在 messages 里还是磁盘上？（长期状态必须磁盘）
- 我的错误是 raise 还是 return string？（应该永远是后者）

---

## 推荐学习路径（最短路径）

如果时间紧，**只读这 4 个文件**就能 80% 理解 Claude Code 内核：

| # | 文件 | 你会学到 |
|---:|---|---|
| 1 | `agents/s_full.py:1-72` | 全局心智模型 + before-LLM-call 钩子链 |
| 2 | `agents/s05_skill_loading.py` | 按需知识加载 = MCP / Plugin / Skill 的统一思想 |
| 3 | `agents/s06_context_compact.py` | 上下文压缩 = 无限会话的根基 |
| 4 | `agents/s07_task_system.py` | 状态外置 = 跨压缩、跨 agent 共享的根基 |

把这 4 个文件读懂，剩下 8 个文件都是它们的组合变体。

---

## 附录 ｜ 速查表

### Claude 运行机制 → 本仓库对应

| Claude 真实机制 | 本仓库对应 |
|---|---|
| Tool calls | `agents/s02_tool_use.py` 全文 |
| TaskCreate / TaskUpdate / TaskList | `agents/s07_task_system.py` `TaskManager` |
| TodoWrite（隐式） | `agents/s03_todo_write.py` `TodoManager` |
| Subagent (Explore/Plan/general-purpose) | `agents/s04_subagent.py` `run_subagent` |
| Skill 加载（system-reminder 列表 + Skill tool 调用） | `agents/s05_skill_loading.py` `SkillLoader` 双层 |
| Memory（`~/.claude/.../memory/`） | `agents/s07_task_system.py` 思路 + frontmatter（s05 思路）的合体 |
| 上下文自动压缩 | `agents/s06_context_compact.py` 三层 |
| Plugin 加载 | 本仓库未演示；类比 s05 SkillLoader 的目录扫描 + manifest 解析 |
| MCP servers | 本仓库未演示；类比 s02 dispatch map 的"远程版" |
| EnterWorktree | `agents/s12_worktree_task_isolation.py` |
| Background Bash | `agents/s08_background_tasks.py` `BackgroundManager` |
| Agent 协作（FleetView） | `agents/s09_agent_teams.py` + `s10_team_protocols.py` |

### 关键文件行号锚点

- Loop 内核：`agents/s01_agent_loop.py:85-116`
- Dispatch map：`agents/s02_tool_use.py:93-98`
- safe_path sandbox：`agents/s02_tool_use.py:39-43`
- 子 agent fresh context：`agents/s04_subagent.py:117`（`sub_messages = [{"role": "user", ...}]`）
- Skill 双层加载：`agents/s05_skill_loading.py:83-102`
- micro_compact 选择性：`agents/s06_context_compact.py:66-96`
- auto_compact 全摘要：`agents/s06_context_compact.py:100-124`
- Task 完成清依赖：`agents/s07_task_system.py:92-98`
- Background 通知队列：`agents/s08_background_tasks.py:80-86`
- Inbox JSONL 队列：`agents/s09_agent_teams.py:96-110`
- request_id 协议：`agents/s10_team_protocols.py:79-82`
- Identity 重新注入：`agents/s11_autonomous_agents.py:30-34`（注释）
- Worktree 索引：`agents/s12_worktree_task_isolation.py:8-29`（注释 ASCII 图）

---

*分析人：Claude（Opus 4.7）｜ 工具：source-code-analyzer skill ｜ 日期：2026-05-14*
