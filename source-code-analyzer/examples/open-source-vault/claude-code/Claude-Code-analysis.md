---
title: "Claude Code 源码深度分析报告"
aliases: [Claude Code, claude-code-analysis]
tags:
  - opensource
  - source-analysis
  - claude-code
  - coding-agent
  - TypeScript
  - mcp
github: https://github.com/anthropics/claude-code
created: 2026-04-15
updated: 2026-04-15
score: 5.1
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Claude Code 源码深度分析报告

> **分析时间**: 2026-04-01
> **项目版本**: 来自2026-03-31泄露快照
> **源码规模**: ~1,900 files, 512,000+ lines of code
> **技术栈**: TypeScript + Bun + React/Ink

---

## 一、命令系统大全

### 1.1 基础命令（用户常用）

| 命令 | 功能说明 | 源码位置 |
|------|---------|---------|
| `/help` | 显示帮助信息 | `src/commands/help/index.js` |
| `/clear` | 清空当前会话 | `src/commands/clear/index.js` |
| `/login` / `/logout` | 登录/登出认证 | `src/commands/login/index.js` |
| `/config` | 设置管理 | `src/commands/config/index.js` |
| `/doctor` | 环境诊断 | `src/commands/doctor/index.js` |
| `/cost` | 查看使用成本 | `src/commands/cost/index.js` |
| `/model` | 切换模型 | `src/commands/model/index.js` |
| `/theme` | 更改主题 | `src/commands/theme/index.js` |
| `/vim` | Vim模式切换 | `src/commands/vim/index.js` |
| `/exit` | 退出程序 | `src/commands/exit/index.js` |

### 1.2 开发工作流命令

| 命令 | 功能说明 | 源码位置 |
|------|---------|---------|
| `/commit` | 创建git提交 | `src/commands/commit.js` |
| `/review` | 代码审查 | `src/commands/review.js` |
| `/diff` | 查看变更 | `src/commands/diff/index.js` |
| `/pr_comments` | 查看PR评论 | `src/commands/pr_comments/index.js` |
| `/branch` | 分支管理 | `src/commands/branch/index.js` |
| `/init` | 初始化项目 | `src/commands/init.js` |

### 1.3 会话管理命令

| 命令 | 功能说明 | 源码位置 |
|------|---------|---------|
| `/resume` | 恢复之前的会话 | `src/commands/resume/index.js` |
| `/compact` | 手动压缩上下文 | `src/commands/compact/index.js` |
| `/rewind` | 回退会话状态 | `src/commands/rewind/index.js` |
| `/share` | 分享会话 | `src/commands/share/index.js` |
| `/session` | 会话管理 | `src/commands/session/index.js` |

### 1.4 高级/进阶命令

| 命令 | 功能说明 | Feature Flag |
|------|---------|--------------|
| `/mcp` | MCP服务器管理 | 无 |
| `/skills` | 技能管理 | 无 |
| `/plugin` | 插件管理 | 无 |
| `/hooks` | 钩子配置 | 无 |
| `/memory` | 持久化记忆管理 | 无 |
| `/tasks` | 任务管理 | 无 |
| `/agents` | 多代理管理 | 无 |
| `/plan` | 计划模式 | 无 |
| `/proactive` | 主动模式 | `PROACTIVE` / `KAIROS` |
| `/voice` | 语音模式 | `VOICE_MODE` |
| `/bridge` | IDE桥接模式 | `BRIDGE_MODE` |
| `/buddy` | 宠物伴侣系统 | `BUDDY` |
| `/ultraplan` | 超级计划模式 | `ULTRAPLAN` |
| `/fork` | 子代理分叉 | `FORK_SUBAGENT` |

### 1.5 调试/内部命令（仅限Anthropic内部）

这些命令通过 `INTERNAL_ONLY_COMMANDS` 数组管理，仅在 `USER_TYPE === 'ant'` 时可用：

- `/bughunter` - Bug追踪
- `/break-cache` - 缓存破坏
- `/mock-limits` - 模拟限制
- `/heapdump` - 堆转储
- `/ant-trace` - 追踪

### 1.6 Feature Flags（特性开关）

通过Bun的 `bun:bundle` 实现编译时死代码消除：

```typescript
import { feature } from 'bun:bundle'

const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default
  : null
```

**主要Feature Flags**:
- `PROACTIVE` - 主动模式
- `KAIROS` - 新一代架构
- `BRIDGE_MODE` - IDE桥接
- `DAEMON` - 后台守护进程
- `VOICE_MODE` - 语音模式
- `AGENT_TRIGGERS` - 代理触发器
- `MONITOR_TOOL` - 监控工具
- `WORKFLOW_SCRIPTS` - 工作流脚本
- `FORK_SUBAGENT` - 子代理分叉
- `BUDDY` - 宠物系统

---

## 二、扩展机制详解

### 2.1 Plugin（插件）机制

**源码位置**: `src/plugins/builtinPlugins.ts`

#### 核心原理

```typescript
// 插件定义结构
type BuiltinPluginDefinition = {
  name: string
  description: string
  version: string
  defaultEnabled?: boolean
  isAvailable?: () => boolean
  skills?: BundledSkillDefinition[]
  hooks?: HooksSettings
  mcpServers?: MCPServerConfig[]
}
```

#### 关键特点

1. **双重来源**:
   - 内置插件 (`@builtin`) - 随CLI发布
   - 市场插件 (`@marketplace`) - 用户安装

2. **热插拔**: 通过 `/plugin` 命令动态启用/禁用

3. **组件集成**: 插件可提供三种组件
   - Skills（技能）
   - Hooks（钩子）
   - MCP Servers（模型上下文协议服务器）

4. **持久化**: 用户配置保存在 `settings.enabledPlugins`

#### 生命周期

```
注册 → 检查可用性 → 读取用户设置 → 加载组件 → 激活
```

#### 代码示例

```typescript:src/plugins/builtinPlugins.ts
export function getBuiltinPlugins(): {
  enabled: LoadedPlugin[]
  disabled: LoadedPlugin[]
} {
  const settings = getSettings_DEPRECATED()

  for (const [name, definition] of BUILTIN_PLUGINS) {
    // 检查可用性
    if (definition.isAvailable && !definition.isAvailable()) {
      continue
    }

    const pluginId = `${name}@${BUILTIN_MARKETPLACE_NAME}`
    const userSetting = settings?.enabledPlugins?.[pluginId]

    // 优先级: 用户设置 > 插件默认值 > true
    const isEnabled = userSetting !== undefined
      ? userSetting === true
      : (definition.defaultEnabled ?? true)

    // 构建LoadedPlugin对象...
  }
}
```

---

### 2.2 MCP (Model Context Protocol) 机制

**源码位置**: `src/services/mcp/client.ts`

#### 核心架构

MCP是一个标准化的工具集成协议，支持三种传输方式：

```typescript
// 三种传输层
- StdioClientTransport              // 本地进程通信（标准输入输出）
- SSEClientTransport                // Server-Sent Events（HTTP长连接）
- StreamableHTTPClientTransport     // HTTP流式传输
```

#### 工作流程

```
┌─────────────────┐
│  配置加载        │  从 claude_desktop_config.json 读取
└────────┬────────┘
         ▼
┌─────────────────┐
│  连接建立        │  根据配置创建对应的Transport
└────────┬────────┘
         ▼
┌─────────────────┐
│  能力发现        │  tools/list, resources/list, prompts/list
└────────┬────────┘
         ▼
┌─────────────────┐
│  工具注册        │  映射为 Claude Code 可调用的 Tool
└────────┬────────┘
         ▼
┌─────────────────┐
│  权限管理        │  OAuth认证、自动刷新token
└─────────────────┘
```

#### 关键代码路径

```typescript:src/services/mcp/client.ts
// MCP工具调用核心流程
async function callMCPTool(serverName: string, toolName: string, args: any) {
  // 1. 获取MCP客户端连接
  const client = await getMCPServerClient(serverName)

  // 2. 调用工具
  const result = await client.request(
    {
      method: 'tools/call',
      params: {
        name: toolName,
        arguments: args
      }
    },
    CallToolResultSchema
  )

  // 3. 处理结果（可能需要截断）
  return processMCPResult(result)
}

// OAuth认证流程
class ClaudeAuthProvider {
  async authenticate() {
    const tokens = getClaudeAIOAuthTokens()
    return {
      Authorization: `Bearer ${tokens.accessToken}`,
      'anthropic-beta': OAUTH_BETA_HEADER
    }
  }
}
```

#### 配置示例

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    },
    "github": {
      "url": "https://github-mcp.example.com/sse",
      "transport": "sse"
    }
  }
}
```

---

### 2.3 Skill（技能）机制

**源码位置**: `src/skills/loadSkillsDir.ts`

#### 技能来源（按优先级）

1. **Bundled Skills** - 内置技能（`src/skills/bundled/`）
2. **Builtin Plugin Skills** - 内置插件提供的技能
3. **Skills Directory** - 项目/用户目录下的技能（`.claude/skills/`）
4. **Plugin Skills** - 插件市场安装的技能
5. **MCP Skills** - MCP服务器提供的技能

#### 加载流程

```typescript:src/skills/loadSkillsDir.ts
async function loadSkill(filePath: string): Promise<Command> {
  // 1. 读取文件内容
  const content = await readFile(filePath, 'utf-8')

  // 2. 解析frontmatter元数据
  const frontmatter = parseFrontmatter(content)

  // 3. 验证schema
  const validated = skillSchema.parse(frontmatter)

  // 4. 构建Command对象
  return {
    type: 'prompt',
    name: validated.name,
    description: validated.description,
    allowedTools: validated.allowedTools ?? [],
    argumentHint: validated.argumentHint,
    whenToUse: validated.whenToUse,
    model: validated.model,
    contentLength: content.length,
    source: 'skills',
    loadedFrom: determineLoadedFrom(filePath),
    hooks: parseHooksFromFrontmatter(frontmatter, validated.name),
    getPromptForCommand: async () => content
  }
}
```

#### 内置技能列表

| 技能文件 | 功能 |
|---------|------|
| `batch.ts` | 批处理操作 |
| `claudeApi.ts` | Claude API调用 |
| `claudeApiContent.ts` | API内容处理 |
| `debug.ts` | 调试辅助 |
| `keybindings.ts` | 快捷键管理 |
| `loop.ts` | 循环执行 |
| `scheduleRemoteAgents.ts` | 远程代理调度 |
| `skillify.ts` | 技能化转换 |
| `updateConfig.ts` | 配置更新 |
| `verify.ts` | 验证检查 |

#### 技能文件格式

```markdown
---
name: my-skill
description: 技能描述
allowedTools:
  - Read
  - Edit
  - Bash
argumentHint: "[文件路径]"
whenToUse: "当需要执行XX任务时使用"
model: claude-sonnet-4-20250514
hooks:
  PreToolUse:
    - command: "echo 'About to use tool'"
---

# 技能内容

这里是实际的技能prompt内容...
```

---

### 2.4 Hook（钩子）机制

**源码位置**: `src/utils/hooks.ts`

#### 支持的事件类型

```typescript
type HookEvent =
  | 'PreToolUse'         // 工具调用前（可拦截）
  | 'PostToolUse'        // 工具调用后
  | 'PostToolUseFailure' // 工具调用失败
  | 'PreCompact'         // 压缩前
  | 'PostCompact'        // 压缩后
  | 'SessionStart'       // 会话开始
  | 'SessionEnd'         // 会话结束
  | 'UserPromptSubmit'   // 用户提交prompt（可修改）
  | 'PermissionRequest'  // 权限请求
  | 'SubagentStart'      // 子代理启动
  | 'SubagentStop'       // 子代理停止
  | 'Stop'               // 停止
  | 'Notification'       // 通知
  | 'TaskCreated'        // 任务创建
  | 'TaskCompleted'      // 任务完成
  | 'FileChanged'        // 文件变更
  | 'ConfigChange'       // 配置变更
  | 'Setup'              // 初始化设置
  | 'CwdChanged'         // 工作目录变更
  | 'InstructionsLoaded' // 指令加载
  | 'Elicitation'        // 交互式询问
  | 'TeammateIdle'       // 队友空闲
```

#### 执行机制

```typescript:src/utils/hooks.ts
async function executeHook(
  matcher: HookMatcher,
  input: HookInput
): Promise<HookResult> {
  // 1. 准备环境变量
  const env = {
    ...process.env,
    CLAUDE_SESSION_ID: getSessionId(),
    CLAUDE_HOOK_EVENT: input.hookEventName,
    CLAUDE_TOOL_NAME: input.toolName,
    CLAUDE_TOOL_INPUT: JSON.stringify(input.toolInput),
    // ... 更多输入数据
  }

  // 2. 执行shell命令
  const process = spawn(matcher.command, {
    env,
    shell: true,
    timeout: matcher.timeout ?? 60000
  })

  // 3. 解析JSON输出
  const stdout = await readStream(process.stdout)
  const output = JSON.parse(stdout) as HookJSONOutput

  // 4. 处理返回结果
  return {
    continue: output.continue ?? true,
    decision: output.decision,      // 'approve' | 'block'
    reason: output.reason,
    updatedInput: output.updatedInput,
    additionalContext: output.additionalContext
  }
}
```

#### 权限拦截流程

```
用户请求工具调用
       │
       ▼
┌─────────────────┐
│ PreToolUse Hook │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
 decision   decision
 'block'   'approve'
    │         │
    ▼         ▼
 返回拒绝   执行工具
 原因        │
             ▼
      ┌─────────────────┐
      │ PostToolUse Hook│
      └─────────────────┘
```

#### Hook配置示例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "toolName": "Bash"
        },
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "toolName": "Write",
          "input": {
            "file_path": ".*\\.env$"
          }
        },
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Warning: .env file modified'"
          }
        ]
      }
    ]
  }
}
```

#### Hook输出格式

```json
{
  "continue": true,
  "suppressOutput": false,
  "decision": "approve",
  "reason": "安全操作，允许执行",
  "systemMessage": "此操作已被安全策略允许",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      // 可修改的工具输入
    },
    "additionalContext": "额外的上下文信息"
  }
}
```

---

## 三、压缩机制详解

**源码位置**: `src/services/compact/`

### 3.1 自动压缩触发条件

```typescript:src/services/compact/autoCompact.ts
// 关键阈值常量
const AUTOCOMPACT_BUFFER_TOKENS = 13_000      // 触发缓冲区
const WARNING_THRESHOLD_BUFFER_TOKENS = 20_000 // 警告阈值
const ERROR_THRESHOLD_BUFFER_TOKENS = 20_000   // 错误阈值
const MANUAL_COMPACT_BUFFER_TOKENS = 3_000     // 手动压缩缓冲区

function getAutoCompactThreshold(model: string): number {
  const effectiveContextWindow = getEffectiveContextWindowSize(model)
  // 预留20K用于摘要输出
  const reservedTokensForSummary = Math.min(
    getMaxOutputTokensForModel(model),
    20_000
  )
  return effectiveContextWindow - reservedTokensForSummary - AUTOCOMPACT_BUFFER_TOKENS
}
```

### 3.2 触发逻辑

```typescript
function calculateTokenWarningState(tokenUsage: number, model: string) {
  const autoCompactThreshold = getAutoCompactThreshold(model)

  return {
    // 剩余百分比
    percentLeft: ((threshold - tokenUsage) / threshold) * 100,

    // 是否达到警告阈值
    isAboveWarningThreshold: tokenUsage >= (threshold - 20_000),

    // 是否达到错误阈值
    isAboveErrorThreshold: tokenUsage >= (threshold - 20_000),

    // 是否触发自动压缩
    isAboveAutoCompactThreshold:
      isAutoCompactEnabled() && tokenUsage >= autoCompactThreshold,

    // 是否达到阻塞限制（必须手动压缩）
    isAtBlockingLimit: tokenUsage >= blockingLimit
  }
}
```

**熔断机制**: 最大连续失败次数 = 3次

### 3.3 压缩算法流程

```typescript:src/services/compact/compact.ts
async function compactConversation(
  messages: Message[],
  options: CompactOptions
): Promise<CompactionResult> {

  // 1. 移除图片（避免prompt过长）
  const stripped = stripImagesFromMessages(messages)

  // 2. 按API轮次分组
  const groups = groupMessagesByApiRound(stripped)

  // 3. 选择压缩策略
  if (shouldUsePartialCompact(groups)) {
    // 部分压缩：只压缩最近的消息
    return partialCompact(groups)
  }

  // 4. 全量压缩：生成完整摘要
  const compactPrompt = getCompactPrompt(groups)

  // 5. 调用LLM生成摘要（使用Sonnet模型）
  const summary = await queryModelWithStreaming({
    model: 'claude-sonnet-4-20250514',
    maxTokens: 20_000,
    messages: [{
      role: 'user',
      content: compactPrompt
    }],
    // 关键：不允许工具调用
    tools: undefined,
    maxTurns: 1
  })

  // 6. 格式化摘要
  const formattedSummary = formatCompactSummary(summary.content)

  // 7. 创建压缩边界消息
  return {
    type: 'compact_boundary',
    summary: formattedSummary,
    timestamp: Date.now(),
    tokenCount: estimateTokens(formattedSummary)
  }
}
```

### 3.4 摘要结构

压缩后的摘要包含以下结构化信息：

```markdown
<analysis>
[模型的分析思考过程，会被strip掉]
</analysis>

<summary>
1. Primary Request and Intent:
   - 用户的主要请求和意图
   - 具体目标和约束条件

2. Key Technical Concepts:
   - [技术概念1]
   - [技术概念2]
   - [框架/库/工具]

3. Files and Code Sections:
   - **文件路径**
     - 重要性说明
     - 变更摘要
     - 关键代码片段

4. Errors and Fixes:
   - 遇到的错误
   - 解决方法
   - 用户反馈

5. Problem Solving:
   - 问题解决过程
   - 关键决策点

6. All User Messages:
   - 完整的用户消息列表

7. Pending Tasks:
   - 待完成的任务

8. Current Work:
   - 当前正在进行的工作详情
   - 文件名和代码片段

9. Optional Next Step:
   - 下一步建议（与最近工作直接相关）
   - 引用原话确保一致性
</summary>
```

### 3.5 微压缩（MicroCompact）

针对特定场景的轻量级压缩策略：

#### Session Memory Compact

```typescript:src/services/compact/sessionMemoryCompact.ts
// 会话记忆压缩
async function trySessionMemoryCompaction(messages: Message[]) {
  // 提取关键记忆点
  const memories = extractMemories(messages)

  // 压缩为结构化记忆
  return memories.map(m => ({
    type: m.type,
    content: m.content.slice(0, 500), // 截断
    timestamp: m.timestamp
  }))
}
```

#### API Microcompact

```typescript:src/services/compact/apiMicrocompact.ts
// API级别的微压缩
// 用于处理特定API响应过大时的快速压缩
```

#### Time-based Compact

```typescript:src/services/compact/timeBasedMCConfig.ts
// 基于时间的压缩配置
const TIME_BASED_THRESHOLDS = {
  short: 60_000,   // 1小时内
  medium: 300_000, // 5小时内
  long: 600_000    // 10小时以上
}
```

### 3.6 压缩后恢复

压缩后需要恢复关键文件到上下文：

```typescript:src/services/compact/compact.ts
const POST_COMPACT_TOKEN_BUDGET = 50_000
const POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000
const POST_COMPACT_MAX_TOKENS_PER_SKILL = 5_000
const POST_COMPACT_SKILLS_TOKEN_BUDGET = 25_000

async function restoreAfterCompact(summary: string) {
  // 1. 识别关键文件
  const importantFiles = extractImportantFiles(summary)

  // 2. 重新读取（带token限制）
  const restored = await Promise.all(
    importantFiles.slice(0, 5).map(async file => ({
      path: file,
      content: await readFileTruncated(file, 5_000)
    }))
  )

  // 3. 恢复技能上下文
  const skills = await restoreSkillsContext(25_000)

  return { restored, skills }
}
```

---

## 四、封号/风控机制分析

### 4.1 Policy Limits（策略限制）

**源码位置**: `src/services/policyLimits/index.ts`

#### 核心机制

```typescript
// 从后端获取组织级别的策略限制
async function fetchPolicyLimits(): Promise<PolicyLimitsResponse> {
  const endpoint = `${BASE_API_URL}/api/claude_code/policy_limits`

  // 支持ETag缓存（减少不必要的传输）
  const response = await axios.get(endpoint, {
    headers: {
      'If-None-Match': cachedChecksum,
      ...authHeaders,
      'User-Agent': getClaudeCodeUserAgent()
    },
    timeout: 10_000
  })

  // 304: 缓存仍有效
  if (response.status === 304) {
    return { restrictions: null, etag: cachedChecksum }
  }

  // 404: 无策略限制
  if (response.status === 404) {
    return { restrictions: {} }
  }

  return response.data
}
```

#### 适用对象

| 用户类型 | 是否适用 | 条件 |
|---------|---------|------|
| Console用户（API Key） | ✅ | 有有效的API Key |
| Claude.ai - Team订阅 | ✅ | 有Team订阅 |
| Claude.ai - Enterprise订阅 | ✅ | 有Enterprise订阅 |
| Claude.ai - 个人订阅 | ❌ | 不适用 |
| 第三方服务（Bedrock/Vertex） | ❌ | 不适用 |
| 自定义Base URL | ❌ | 不适用 |

#### 策略类型示例

```typescript
type PolicyRestrictions = {
  [policy: string]: {
    allowed: boolean
    reason?: string
  }
}

// 示例策略
{
  "allow_remote_sessions": {
    "allowed": false,
    "reason": "Organization policy disables remote sessions"
  },
  "allow_product_feedback": {
    "allowed": true
  },
  "allow_third_party_integrations": {
    "allowed": false
  }
}
```

#### 检查逻辑

```typescript
export function isPolicyAllowed(policy: string): boolean {
  const restrictions = getRestrictionsFromCache()

  if (!restrictions) {
    // Fail open：无缓存时默认允许（HIPAA模式除外）
    if (isEssentialTrafficOnly() &&
        ESSENTIAL_TRAFFIC_DENY_ON_MISS.has(policy)) {
      return false
    }
    return true
  }

  const restriction = restrictions[policy]

  if (!restriction) {
    return true // 未知策略 = 允许
  }

  return restriction.allowed
}
```

#### 后台轮询

```typescript
const POLLING_INTERVAL_MS = 60 * 60 * 1000 // 每小时检查

function startBackgroundPolling() {
  pollingIntervalId = setInterval(async () => {
    await fetchAndLoadPolicyLimits()
  }, POLLING_INTERVAL_MS)

  // 不阻塞进程退出
  pollingIntervalId.unref()
}
```

### 4.2 Fingerprint（指纹识别）

**源码位置**: `src/utils/fingerprint.ts`

#### 算法详解

```typescript
// 硬编码盐值（必须与后端完全匹配）
export const FINGERPRINT_SALT = '59cf53e54c78'

function computeFingerprint(
  messageText: string,
  version: string
): string {
  // 步骤1: 提取特定位置字符 [4, 7, 20]
  const indices = [4, 7, 20]
  const chars = indices
    .map(i => messageText[i] || '0')
    .join('')

  // 步骤2: 组合指纹输入
  const fingerprintInput = `${FINGERPRINT_SALT}${chars}${version}`

  // 步骤3: SHA256哈希
  const hash = createHash('sha256')
    .update(fingerprintInput)
    .digest('hex')

  // 步骤4: 取前3位作为最终指纹
  return hash.slice(0, 3)
}
```

#### 用途

1. **请求识别**: 识别来自Claude Code的请求
2. **跨平台协调**: 与1P和3P API（Bedrock/Vertex/Azure）协调
3. **版本追踪**: 绑定到客户端版本
4. **防滥用**: 追踪异常使用模式

#### 特点

- **确定性**: 相同的输入总是产生相同的指纹
- **不可逆**: 无法从指纹反推原始内容
- **轻量级**: 只需提取3个字符
- **跨平台**: 所有API提供商使用相同算法

### 4.3 Rate Limit处理

**源码位置**: `src/services/api/errors.ts`

```typescript
export function getRateLimitErrorMessage(
  limits: ClaudeAILimits
): string {
  const {
    remaining,
    limit,
    resetAt,
    tier
  } = limits

  const resetTime = new Date(resetAt).toLocaleTimeString()

  return `Rate limit reached. You've used ${limit - remaining}/${limit} ${tier} messages. ` +
         `Limit resets at ${resetTime}.`
}
```

### 4.4 降低风险建议

基于源码分析，以下是**合规使用**的建议：

#### ✅ 推荐做法

1. **使用官方API Key或订阅账号**
   - 避免使用来路不明的共享账号
   - OAuth认证需有合法订阅（Team/Enterprise）

2. **避免异常使用模式**
   - 不使用自动化脚本高频调用
   - 遵守API Rate Limit限制
   - 正常的交互频率

3. **企业用户注意Policy Limits**
   - 检查 `~/.claude/policy-limits.json`
   - 组织管理员可能设置了远程会话禁用等限制
   - HIPAA模式有更严格的限制

4. **保持客户端版本更新**
   - Fingerprint与版本号绑定
   - 旧版本可能被标记

5. **尊重内容安全策略**
   - 源码中有content filtering机制
   - 避免生成违禁内容

#### ⚠️ 注意事项

- Policy Limits是**组织级别**的控制，不是个人封禁
- Fingerprint用于**识别客户端**，不是监控内容
- 风控主要依赖**后端API验证**，不在客户端实现

---

## 五、Buddy系统详解

### 5.1 系统概述

**源码位置**: `src/buddy/`

Buddy是一个**虚拟宠物伴侣系统**，通过确定性随机算法为每个用户生成独特的伙伴形象，具有：
- 稀有度系统（5个等级）
- 属性系统（5种属性）
- 视觉动画（ASCII艺术）
- 个性化灵魂（LLM生成）

### 5.2 生成算法

```typescript:src/buddy/companion.ts
// Mulberry32 PRNG - 小型种子随机数生成器
function mulberry32(seed: number): () => number {
  let a = seed >>> 0
  return function () {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = Math.imul(a ^ (a >>> 15), 1 | a)
    t = (t + Math.imul(t ^ (a >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

// 使用用户ID生成确定性结果
export function roll(userId: string): Roll {
  const SALT = 'friend-2026-401'
  const rng = mulberry32(hashString(userId + SALT))

  // 1. 滚动稀有度
  const rarity = rollRarity(rng)

  // 2. 生成基础属性（骨骼）
  const bones: CompanionBones = {
    rarity,
    species: pick(rng, SPECIES),     // 18种物种
    eye: pick(rng, EYES),            // 6种眼睛
    hat: pick(rng, HATS),            // 8种帽子
    shiny: rng() < 0.01,             // 1%闪光概率
    stats: rollStats(rng, rarity)    // 属性值
  }

  return {
    bones,
    inspirationSeed: Math.floor(rng() * 1e9)
  }
}
```

### 5.3 稀有度权重

```typescript:src/buddy/types.ts
const RARITY_WEIGHTS = {
  common: 60,      // 60% 概率 - 灰色
  uncommon: 25,    // 25% 概率 - 绿色
  rare: 10,        // 10% 概率 - 蓝色
  epic: 4,         // 4% 概率  - 紫色
  legendary: 1     // 1% 概率  - 橙色
}
```

**稀有度显示**:
| 稀有度 | 星级 | 颜色 | 概率 |
|--------|-----|------|------|
| Common | ★ | 灰色 | 60% |
| Uncommon | ★★ | 绿色 | 25% |
| Rare | ★★★ | 蓝色 | 10% |
| Epic | ★★★★ | 紫色 | 4% |
| Legendary | ★★★★★ | 橙色 | 1% |

### 5.4 属性系统

#### 五大属性

```typescript
const STAT_NAMES = [
  'DEBUGGING',   // 调试能力 - 解决bug的效率
  'PATIENCE',    // 耐心度 - 长任务的持久性
  'CHAOS',       // 混乱度 - 意外行为的倾向
  'WISDOM',      // 智慧值 - 知识和建议质量
  'SNARK'        // 讽刺度 - 回复的幽默/讽刺程度
]
```

#### 属性生成规则

```typescript
function rollStats(
  rng: () => number,
  rarity: Rarity
): Record<StatName, number> {
  const floor = RARITY_FLOOR[rarity]

  // 选择一个巅峰属性和一个低谷属性
  const peak = pick(rng, STAT_NAMES)
  let dump = pick(rng, STAT_NAMES)
  while (dump === peak) dump = pick(rng, STAT_NAMES)

  const stats = {} as Record<StatName, number>

  for (const name of STAT_NAMES) {
    if (name === peak) {
      // 巅峰属性: 基础值 + 50 + 0~30
      stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30))
    } else if (name === dump) {
      // 低谷属性: 基础值 - 10 + 0~15
      stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15))
    } else {
      // 普通属性: 基础值 + 0~40
      stats[name] = floor + Math.floor(rng() * 40)
    }
  }

  return stats
}
```

#### 稀有度基础值

| 稀有度 | 基础值(flo or) | 巅峰属性范围 | 低谷属性范围 | 普通属性范围 |
|--------|---------------|-------------|-------------|-------------|
| Common | 5 | 55-85 | 1-10 | 5-45 |
| Uncommon | 15 | 65-95 | 5-20 | 15-55 |
| Rare | 25 | 75-100 | 15-30 | 25-65 |
| Epic | 35 | 85-100 | 25-40 | 35-75 |
| Legendary | 50 | 100 | 40-55 | 50-90 |

### 5.5 物种列表

```typescript
const SPECIES = [
  'duck',       // 鸭子
  'goose',      // 鹅
  'blob',       // 团块
  'cat',        // 猫
  'dragon',     // 龙
  'octopus',    // 章鱼
  'owl',        // 猫头鹰
  'penguin',    // 企鹅
  'turtle',     // 乌龟
  'snail',      // 蜗牛
  'ghost',      // 幽灵
  'axolotl',    // 蝾螈
  'capybara',   // 水豚
  'cactus',     // 仙人掌
  'robot',      // 机器人
  'rabbit',     // 兔子
  'mushroom',   // 蘑菇
  'chonk'       // 胖墩
]
```

### 5.6 视觉表现

**源码位置**: `src/buddy/sprites.ts`

每个物种有3帧动画用于idle状态：

```typescript
// 示例：鸭子的动画帧
const BODIES = {
  [duck]: [
    // 帧1 - 正常
    [
      '            ',
      '    __      ',
      '  <({E} )___',  // {E} 会被眼睛样式替换
      '   (  ._>   ',
      '    `--´    '
    ],
    // 帧2 - 轻微摆动
    [
      '            ',
      '    __      ',
      '  <({E} )___',
      '   (  ._>   ',
      '    `--´~   '  // 尾巴摆动
    ],
    // 帧3 - 扩展
    [
      '            ',
      '    __      ',
      '  <({E} )___',
      '   (  .__>  ',  // 嘴巴张开
      '    `--´    '
    ]
  ]
}
```

#### 眼睛样式

```typescript
const EYES = ['·', '✦', '×', '◉', '@', '°']
```

#### 帽子类型

```typescript
const HATS = [
  'none',       // 无帽子
  'crown',      // 皇冠
  'tophat',     // 高礼帽
  'propeller',  // 螺旋桨帽
  'halo',       // 光环
  'wizard',     // 巫师帽
  'beanie',     // 毛线帽
  'tinyduck'    // 小鸭子
]
```

### 5.7 灵魂生成

首次孵化时，通过LLM生成个性化信息：

```typescript
type CompanionSoul = {
  name: string        // 名字（由LLM生成）
  personality: string // 性格描述（由LLM生成）
}

type Companion = CompanionBones & CompanionSoul & {
  hatchedAt: number   // 孵化时间戳
}

// 存储策略
type StoredCompanion = CompanionSoul & { hatchedAt: number }
// Bones每次从userId重新生成（防止伪造稀有度）
```

### 5.8 系统特点

1. **确定性**: 相同用户ID总是生成相同的Buddy
2. **不可伪造**: Bones每次重新计算，无法通过修改配置获得高稀有度
3. **个性化**: 灵魂信息由LLM基于inspirationSeed生成
4. **收集要素**: 闪光(Shiny)有1%概率，增加收集乐趣

---

## 六、架构全景图

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLI Entry (main.tsx)                       │
│                    Commander.js + React/Ink                       │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐               │
│  │ Prefetch   │  │  Keychain   │  │  GrowthBook  │               │
│  │  MDM/Keys  │  │   Prefetch  │  │    Init      │               │
│  └────────────┘  └─────────────┘  └──────────────┘               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  ┌─────────────┐    ┌─────────────┐     ┌─────────────┐
  │  Commands   │    │   Skills    │     │   Plugins   │
  │   (/xxx)    │    │  (.md/.ts)  │     │   (@src)    │
  │  50+ cmds   │    │  Bundled +  │     │  Built-in + │
  │             │    │  User/Proj  │     │  Marketplace│
  └──────┬──────┘    └──────┬──────┘     └──────┬──────┘
         │                  │                   │
         └──────────────────┼───────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │    Tool System      │
                 │    (40+ tools)      │
                 │  ┌───────────────┐  │
                 │  │ BashTool      │  │
                 │  │ FileReadTool  │  │
                 │  │ FileEditTool  │  │
                 │  │ MCPTool       │  │
                 │  │ AgentTool     │  │
                 │  │ SkillTool     │  │
                 │  │ ...           │  │
                 │  └───────────────┘  │
                 └──────────┬──────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │  MCP Client │    │ LSP Manager │    │ Hooks System│
  │  Transport: │    │  Servers:   │    │  Events:    │
  │  - Stdio    │    │  - TS/JS    │    │  - PreTool  │
  │  - SSE      │    │  - Python   │    │  - PostTool │
  │  - HTTP     │    │  - Go/Rust  │    │  - Session  │
  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
         │                  │                   │
         └──────────────────┼───────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │   QueryEngine       │
                 │  (LLM调用核心)       │
                 │  - Streaming        │
                 │  - Retry Logic      │
                 │  - Token Counting   │
                 └──────────┬──────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │   Compact   │    │  Analytics  │    │   Policy    │
  │   Service   │    │   Service   │    │   Limits    │
  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
  │ │Auto     │ │    │ │GrowthBook│ │    │ │Org      │ │
  │ │Manual   │ │    │ │OTel     │ │    │ │Policies │ │
  │ │Micro    │ │    │ │DDog     │ │    │ │HIPAA    │ │
  │ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │
  └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 七、核心设计模式

### 7.1 并行预加载

```typescript:src/main.tsx
// 在模块加载前启动预加载（作为副作用）
startMdmRawRead()       // MDM配置读取
startKeychainPrefetch() // Keychain预取
```

### 7.2 懒加载

```typescript
// OpenTelemetry等重模块延迟导入
const otel = await import('@opentelemetry/api')

// 大型技能延迟加载（如insights.ts 113KB）
const usageReport: Command = {
  type: 'prompt',
  name: 'insights',
  async getPromptForCommand() {
    const real = await import('./commands/insights.js')
    return real.getPromptForCommand(args, context)
  }
}
```

### 7.3 熔断器

```typescript
// 连续失败3次停止autocompact
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3

if (state.consecutiveFailures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES) {
  logForDebugging('Autocompact circuit breaker triggered')
  return { shouldCompact: false }
}
```

### 7.4 多级缓存

```
┌─────────────┐
│ Session     │ ← 内存缓存（最快）
│ Cache       │
└──────┬──────┘
       ▼
┌─────────────┐
│ File Cache  │ ← 磁盘缓存
│ (.json)     │
└──────┬──────┘
       ▼
┌─────────────┐
│ ETag/304    │ ← HTTP缓存
│ Validation  │
└─────────────┘
```

---

## 八、总结

### 核心发现

1. **命令系统**
   - 50+命令，分为基础/工作流/会话/高级/内部5类
   - Feature Flag控制功能开关，编译时消除死代码

2. **扩展机制**
   - Plugin > MCP > Skill > Hook 四层架构
   - 支持用户自定义、市场分发、内置集成

3. **压缩算法**
   - 自动触发 + LLM摘要 + 分组策略
   - 熔断机制防止无限重试

4. **风控系统**
   - 基于后端Policy Limits接口
   - Fingerprint识别客户端来源
   - 无客户端"封号"代码

5. **Buddy系统**
   - 确定性随机生成
   - 五大属性 + 五级稀有度
   - 不可伪造的收集要素

### 设计亮点

| 特性 | 实现方式 | 优势 |
|------|---------|------|
| 并行预加载 | 启动时prefetch | 加快启动速度 |
| 懒加载 | 动态import() | 减少内存占用 |
| 熔断机制 | 连续失败计数 | 防止资源浪费 |
| 多级缓存 | Session + File + ETag | 平衡性能与一致性 |
| 确定性随机 | 种子PRNG | 可重现 + 不可伪造 |

### 技术启示

1. **性能优化**: 预加载 + 懒加载的组合拳
2. **可扩展性**: 插件系统设计模式
3. **可靠性**: 熔断 + 重试 + 降级策略
4. **用户体验**: 渐进式功能暴露

---

## 附录：关键文件索引

| 文件路径 | 行数 | 功能 |
|---------|------|------|
| `src/QueryEngine.ts` | ~46K | LLM调用核心引擎 |
| `src/Tool.ts` | ~29K | 工具类型定义 |
| `src/commands.ts` | ~25K | 命令注册管理 |
| `src/commands/insights.ts` | ~113KB | 使用洞察报告 |
| `src/hooks/useReplBridge.tsx` | ~115KB | REPL桥接逻辑 |
| `src/hooks/useTypeahead.tsx` | ~212KB | 自动完成 |
| `src/services/compact/compact.ts` | - | 压缩核心逻辑 |
| `src/services/mcp/client.ts` | - | MCP客户端 |
| `src/buddy/CompanionSprite.tsx` | ~46K | 伴侣精灵渲染 |

---

*报告生成时间: 2026-04-01*
*数据来源: Claude Code 源码快照 (2026-03-31)*
