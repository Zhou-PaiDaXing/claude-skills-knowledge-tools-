---
title: "Superpowers 源码洞察"
aliases: [Superpowers]
tags:
  - opensource
  - source-analysis
  - ai-skill
  - Python
github: https://github.com/superpowers-ai/superpowers
created: 2026-04-15
updated: 2026-04-15
score: 4.2
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Superpowers 源码洞察

## 一句话本质
> Superpowers 是一套**AI 编码助手的工作流系统**，它的核心创新是：**把软件工程最佳实践"编码"成 AI 可自动执行的技能链，让 AI 从"会写代码"进化成"会做工程"**。

---

## 核心理念

### 作者在设计时秉持的价值观

**理念1：先想清楚，再动手写**

- **体现在哪里**：`brainstorming` skill 强制要求 "Do NOT invoke any implementation skill...until you have presented a design and the user has approved it"
- **为什么重要**：AI 的天性是"看到需求就写代码"，这是效率最高的响应方式，但往往导致方向错误、返工
- **如何借鉴**：任何 AI 辅助开发流程，都应该在"写代码"之前插入"设计方案"阶段，并要求显式确认

**理念2：测试先行是不可妥协的铁律**

- **体现在哪里**：`test-driven-development` skill 的 "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"，以及 "Write code before the test? Delete it. Start over."
- **为什么重要**：AI 写的代码"看起来对"但"可能错"，只有先看到测试失败，才能证明测试真的在验证什么
- **如何借鉴**：在 AI 编码流程中强制 TDD——不是建议，是约束

**理念3：每一步都要可验证**

- **体现在哪里**：`writing-plans` skill 要求每个步骤都包含 "Expected output" 和验证命令
- **为什么重要**：AI 的"完成"不等于"真正完成"，需要用客观标准检验
- **如何借鉴**：任何给 AI 的任务，都要有明确的"完成定义"（Definition of Done）

**理念4：上下文隔离，防止污染**

- **体现在哪里**：`subagent-driven-development` skill 强调 "Fresh subagent per task...They should never inherit your session's context"
- **为什么重要**：AI 的上下文会被之前的对话"污染"，导致判断偏差
- **如何借鉴**：把大任务拆成小任务，每个任务用新的会话执行，只传入必要的上下文

**理念5：调试必须找到根因，不能修症状**

- **体现在哪里**：`systematic-debugging` skill 的 "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
- **为什么重要**：AI 的天性是"看到报错就改代码"，但这往往只是修了症状，根因还在
- **如何借鉴**：在 AI 修复 bug 之前，强制要求它回答"根因是什么？你怎么知道的？"

---

### 与主流方案的哲学差异

| 维度 | 主流做法 | Superpowers 的做法 | 背后的思考 |
|------|---------|-------------------|-----------|
| AI 角色 | 代码生成器 | 软件工程师 | 不只是写代码，而是完成工程任务 |
| 响应模式 | 有需求就写代码 | 先设计 → 再计划 → 再实现 | 避免"快但错" |
| 测试策略 | 写完代码再补测试 | 先写测试，看它失败，再写代码 | 测试后写 = 没验证 |
| 任务粒度 | "实现这个功能" | 每步 2-5 分钟，有验证标准 | 小步快跑，每步可验证 |
| 调试方式 | 看报错就改代码 | 四阶段：根因分析 → 模式对比 → 假设验证 → 实现 | 修症状 = 制造新 bug |
| 上下文管理 | 一个对话搞定所有 | 每个任务新的 subagent，只传必要上下文 | 隔离 = 准确 |

---

## 设计亮点

### 亮点1：工作流链式触发——让 AI "自动"做正确的事

**问题背景：**
- AI 助手有技能，但不知道何时用哪个
- 用户需要手动告诉 AI "现在用 TDD"、"现在做 code review"
- 痛点：用户负担重，AI 行为不可预测

**创新做法：**

每个 skill 有 `description` 字段描述"何时触发"：

```yaml
---
name: brainstorming
description: "You MUST use this before any creative work..."
---

---
name: writing-plans
description: "Use when you have a spec or requirements..."
---

---
name: test-driven-development
description: "Use when implementing any feature..."
---
```

AI 在执行任务前，会检查"当前情况匹配哪个 skill 的触发条件"，然后自动激活。

**链式设计：**
```
brainstorming → writing-plans → subagent-driven-development → finishing-a-development-branch
    ↓                  ↓                    ↓                           ↓
  设计阶段           计划阶段              实现阶段                     收尾阶段
```

每个 skill 的输出，是下一个 skill 的输入。用户只需提一个需求，AI 自动走完整个流程。

**为什么有效：**
- 触发条件是声明式的，AI 能自己判断
- 链式结构保证了顺序，不会跳过步骤
- 用户只需介入"确认设计"等关键节点

**代价与适用性：**
- 代价：需要精心设计每个 skill 的边界和触发条件
- 适用：任何"有最佳实践流程"的领域（数据分析、写作、设计...）

---

### 亮点2：Subagent-Driven Development——用"分工"换取"质量"

**问题背景：**
- 一个 AI 会话从头做到尾，上下文越来越乱
- 写代码、做审查、跑测试都是同一个 AI，缺乏制衡
- 痛点：错误累积，质量失控

**创新做法：**

把任务分给不同角色的 subagent：

```
[Controller Agent] 你（主控）
    ↓ 派发任务
[Implementer Agent] 只负责写代码
    ↓ 提交完成
[Spec Reviewer Agent] 只负责检查是否符合设计
    ↓ 发现问题
[Implementer Agent] 修复问题
    ↓ 通过审查
[Code Quality Agent] 只负责检查代码质量
    ↓ 通过审查
[Controller Agent] 标记任务完成
```

**关键设计：**
- **每个 subagent 是新的会话**：不继承之前的上下文，只拿到当前任务需要的精确信息
- **两阶段审查**：先查"是否符合设计"，再查"代码质量"
- **审查不通过必须修复后重新审查**：不能"差不多就过"

**为什么有效：**
- 角色分离 = 利益分离 = 更客观的审查
- 上下文隔离 = 更准确的判断
- 两阶段审查 = 既不错做，也做好

**代价与适用性：**
- 代价：更多 API 调用，更多时间
- 适用：任何"需要质量把关"的 AI 工作流

---

### 亮点3："铁律"式规则——把软建议变成硬约束

**问题背景：**
- 很多 AI 助手有"最佳实践建议"，但只是建议
- AI 会说"这次先跳过 TDD，下次一定"
- 痛点：规则没有强制力，形同虚设

**创新做法：**

在 skill 中用"铁律"式表述：

```markdown
## The Iron Law

NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

Write code before the test? Delete it. Start over.
```

```markdown
## The Iron Law

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

If you haven't completed Phase 1, you cannot propose fixes.
```

**配套机制：**
- **Red Flags 清单**：列出所有"你正在违反规则"的信号
- **Rationalizations 表格**：列出所有"自我辩解"并一一反驳
- **强制检查点**：比如 "Verify RED - Watch It Fail - MANDATORY. Never skip."

**为什么有效：**
- "铁律"不是建议，是不可违反的约束
- Red Flags 让 AI 能自我检测是否在违反规则
- Rationalizations 堵住了"这次例外"的借口

**代价与适用性：**
- 代价：可能降低灵活性，某些场景确实需要例外
- 适用：任何"核心原则不可妥协"的流程

---

### 亮点4：任务粒度设计——2-5 分钟一个动作

**问题背景：**
- 传统任务分解到"实现用户登录功能"，粒度太粗
- AI 做 30 分钟后，中间出了什么问题很难定位
- 痛点：任务太大 = 难验证 = 难回滚

**创新做法：**

`writing-plans` skill 定义了极细粒度的任务结构：

```markdown
### Task N: [Component Name]

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
```

每一步是 2-5 分钟的动作，有明确的输入、输出、验证标准。

**为什么有效：**
- 粒度足够小，每一步都可以独立验证
- 出问题只需要回滚一个步骤
- AI 不会在长任务中"迷失方向"

**代价与适用性：**
- 代价：规划成本高，需要详细设计每一步
- 适用：任何"质量优先于速度"的开发任务

---

## 可学习的模式

### 模式1：Skill 链式触发模式

**解决的问题：** 如何让 AI 自动遵循一套复杂的最佳实践流程？

**核心做法：**

```yaml
# skill 1
name: brainstorming
description: "Use this BEFORE implementation"
# 输出：设计文档
# 触发下一个：writing-plans

# skill 2
name: writing-plans
description: "Use when you have a spec"
# 输出：实现计划
# 触发下一个：subagent-driven-development

# skill 3
name: subagent-driven-development
description: "Use when executing plans"
# 输出：完成的代码
# 触发下一个：finishing-a-development-branch
```

**适用场景：**
- 任何"有标准流程"的 AI 应用
- 客服机器人（问题分类 → 答案检索 → 答案生成 → 质量检查）
- 内容创作（选题 → 大纲 → 初稿 → 修订 → 发布）

**注意事项：**
- 每个 skill 的边界要清晰，输入输出要明确
- 触发条件要足够具体，避免误触发

---

### 模式2：两阶段审查模式

**解决的问题：** AI 自我审查不可靠，如何引入制衡？

**核心做法：**

```
[实现者 Agent] → 完成 → [规范审查 Agent] → 通过? → [质量审查 Agent]
                      ↓                ↓
                    不通过 ← 发现问题 ←
                      ↓
                [实现者 Agent 修复]
```

**审查分工：**
- **规范审查**：代码是否符合设计？有没有多做或少做？
- **质量审查**：代码质量如何？有无坏味道？

**适用场景：**
- 任何需要"质量把关"的 AI 产出
- 文档生成（内容审查 → 格式审查）
- 代码生成（功能审查 → 风格审查）

---

### 模式3：Red Flags + Rationalizations 模式

**解决的问题：** 如何防止 AI 找借口绕过规则？

**核心做法：**

```markdown
## Red Flags - STOP and Start Over

- Code before test
- Test passes immediately
- "I'll test after"

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
```

**适用场景：**
- 任何"有不可妥协规则"的 AI 流程
- 安全检查（禁止绕过的检查点）
- 合规流程（必须完成的步骤）

---

### 模式4：四阶段调试模式

**解决的问题：** AI 看到报错就改代码，怎么让它找到根因？

**核心做法：**

```
Phase 1: 根因调查
  - 读错误信息
  - 稳定复现
  - 检查最近改动
  - 追踪数据流

Phase 2: 模式分析
  - 找类似的工作代码
  - 对比差异

Phase 3: 假设验证
  - 形成单一假设
  - 最小化测试
  - 不要叠加修复

Phase 4: 实现
  - 写失败的测试
  - 实现单一修复
  - 验证修复
```

**适用场景：**
- 任何 AI 辅助调试流程
- 生产事故排查
- 测试失败定位

---

## 架构全景图

```
┌────────────────────────────────────────────────────────────────┐
│                     Superpowers Workflow                        │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐  │
│  │ brainstorming│ → │writing-plans│ → │subagent-driven-dev  │  │
│  │  (设计阶段)   │   │  (计划阶段)  │   │     (实现阶段)       │  │
│  └─────────────┘   └─────────────┘   └─────────────────────┘  │
│                           │                    │               │
│                           ▼                    ▼               │
│                    ┌─────────────┐     ┌─────────────────┐    │
│                    │ TDD (铁律)   │     │ 两阶段审查       │    │
│                    │ Red-Green   │     │ Spec + Quality  │    │
│                    │ Refactor    │     │                 │    │
│                    └─────────────┘     └─────────────────┘    │
│                                               │                │
│                                               ▼                │
│                                    ┌───────────────────────┐  │
│                                    │finishing-a-dev-branch │  │
│                                    │      (收尾阶段)        │  │
│                                    └───────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                    │                              │
                    ▼                              ▼
          ┌─────────────────┐            ┌─────────────────┐
          │ Platform Layer  │            │ Supporting Skills│
          │ Claude / Cursor │            │ systematic-debug │
          │ Codex / OpenCode│            │ code-review      │
          │ Gemini CLI      │            │ verification     │
          └─────────────────┘            └─────────────────┘
```

**核心流程一句话：**
- **brainstorming**：理解需求 → 设计方案 → 用户确认
- **writing-plans**：设计方案 → 细化任务 → 每步可验证
- **subagent-driven-dev**：任务 → 实现 → 审查 → 修复 → 完成
- **finishing-branch**：验证 → 合并/PR → 清理

---

## 对我的启发

### 如果我在做类似项目

**我会借鉴：**
1. **Skill 链式触发**——让最佳实践自动化，而不是依赖用户提醒
2. **两阶段审查**——实现者和审查者分离，用"制衡"换"质量"
3. **任务粒度 2-5 分钟**——小步快跑，每步可验证
4. **Red Flags + Rationalizations**——堵住所有"自我辩解"的借口

**我会改进：**
1. **增加可视化**——让用户看到当前在流程的哪个阶段，进度如何
2. **支持"部分跳过"**——对于简单任务，允许用户声明"我知道风险，跳过设计阶段"
3. **增加"学习模式"**——让 AI 从用户的修改中学习，改进后续任务

### 这个项目教会我的 3 件事

1. **AI 需要的不是"能力"，而是"约束"**——Superpowers 的价值不是让 AI 更聪明，而是让 AI 遵循纪律

2. **最佳实践需要"编码"成流程**——光有原则不够，必须有触发条件、执行步骤、验证标准

3. **质量来自"制衡"，而非"信任"**——实现者不能是审查者，两阶段审查比自我审查可靠 10 倍

---
*分析时间：2026-03-30 | 项目版本：5.0.6*
