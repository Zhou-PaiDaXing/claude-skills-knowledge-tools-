---
title: "Andrej Karpathy Skills"
aliases: [Karpathy Skills, Karpathy CLAUDE.md]
tags:
  - opensource
  - ai-skill
  - claude-code
  - best-practices
github: https://github.com/karpathy/dotfiles
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Andrej Karpathy Skills 项目分析报告

## 项目概述

**Andrej Karpathy Skills** 是一个极简的 Claude Code 行为改进指南项目，基于 Andrej Karpathy 对 LLM 编码陷阱的观察而创建。

- **GitHub Stars**: 36,490
- **内容形式**: 单文件 (`CLAUDE.md`)
- **许可证**: MIT
- **核心**: 一个 66 行的行为准则文件

### 核心定位

这不是一个传统意义上的软件项目，而是一个**AI 编程助手的行为规范文档**，旨在通过四个核心原则改善 Claude Code（及其他 LLM 编程助手）的代码生成行为。

---

## 技术栈分析

### 项目构成

| 组件 | 说明 |
|------|------|
| **CLAUDE.md** | 核心行为准则文件 (66行) |
| **EXAMPLES.md** | 使用示例和案例 (14KB) |
| **README.md** | 项目说明 (6KB) |
| **skills/** | 可选技能扩展目录 |

### 无依赖设计

这是一个**零依赖**项目：
- 无编程语言要求
- 无运行时依赖
- 无构建步骤
- 纯 Markdown 文档

---

## 核心功能模块

### 1. 四大核心原则

```markdown
## 1. Think Before Coding
**不要假设。不要隐藏困惑。呈现权衡。**

- 明确陈述假设——如果不确定，询问而非猜测
- 如果存在多种解释，展示它们——不要默默选择
- 如果存在更简单的方法，说出来——适时反驳
- 如果有不清楚的地方，停下来——指出困惑之处并询问

## 2. Simplicity First
**解决问题的最小代码。不做推测性设计。**

- 不添加超出要求的功能
- 不为一次性代码创建抽象
- 不添加未被要求的"灵活性"或"可配置性"
- 不为不可能的场景做错误处理
- 如果 200 行可以写成 50 行，重写它

## 3. Surgical Changes
**只触碰必须触碰的。只清理自己造成的混乱。**

编辑现有代码时：
- 不要"改进"相邻代码、注释或格式
- 不要重构没有损坏的东西
- 匹配现有风格，即使你自己会做得不同
- 如果注意到无关的死代码，提及它——不要删除它

当变更产生孤儿代码时：
- 删除 YOUR 变更导致未使用的导入/变量/函数
- 不要删除预先存在的死代码，除非被要求

## 4. Goal-Driven Execution
**定义成功标准。循环直到验证。**

将任务转化为可验证的目标：
- "添加验证" → "为无效输入编写测试，然后让它们通过"
- "修复 bug" → "编写重现它的测试，然后让它通过"
- "重构 X" → "确保测试在前后都通过"
```

### 2. 文件结构

```
andrej-karpathy-skills/
├── CLAUDE.md              # 核心行为准则 (66行)
├── README.md              # 项目说明
├── EXAMPLES.md            # 详细示例
├── .claude-plugin/        # Claude Code 插件配置
└── skills/                # 扩展技能目录
```

### 3. 安装方式

#### 方式 A: Claude Code 插件（推荐）

```bash
# 添加市场
/plugin marketplace add forrestchang/andrej-karpathy-skills

# 安装插件
/plugin install andrej-karpathy-skills@karpathy-skills
```

#### 方式 B: 单项目配置

```bash
# 新项目
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md

# 现有项目（追加）
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

---

## 代码结构概览

### CLAUDE.md 完整内容

```markdown
# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. 
Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. 
For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. 
Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, 
fewer rewrites due to overcomplication, and clarifying questions come 
before implementation rather than after mistakes.
```

---

## 关键实现亮点

### 1. 问题根源分析

来自 Andrej Karpathy 的观察：

> "模型会代表你做出错误假设并继续执行而不检查。它们不管理困惑，不寻求澄清，不呈现不一致性，不展示权衡，不在应该反驳时反驳。"

> "它们真的喜欢过度复杂化代码和 API，膨胀抽象，不清理死代码... 实现 1000 行的臃肿结构，而 100 行就能搞定。"

> "它们有时仍会改变/删除它们理解不足的注释和代码作为副作用，即使与任务正交。"

### 2. 解决方案映射

| 问题 | 解决原则 |
|------|----------|
| 错误假设、隐藏困惑、缺少权衡 | **Think Before Coding** |
| 过度复杂、膨胀抽象 | **Simplicity First** |
| 正交编辑、触碰不该碰的代码 | **Surgical Changes** |
| 无法验证的完成标准 | **Goal-Driven Execution** |

### 3. 关键洞察

> "LLMs 非常擅长循环直到达到特定目标... 不要告诉它做什么，给它成功标准然后看着它执行。"

—— Andrej Karpathy

### 4. 效果验证指标

指南有效的标志：
- **更少的 diff 中不必要变更** —— 只出现请求的变更
- **更少的过度复杂化重写** —— 代码第一次就简洁
- **澄清问题在实现之前提出** —— 而非在错误之后
- **干净、最小的 PR** —— 没有顺手的重构或"改进"

### 5. 权衡说明

这些指南偏向于**谨慎而非速度**。对于琐碎任务（简单的拼写修复、明显的一行修改），使用判断——并非每个变更都需要完整的严谨性。

目标是减少非琐碎工作上的昂贵错误，而非拖慢简单任务。

---

## 适用场景建议

### 推荐场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| **AI 辅助编程** | ★★★★★ | 改善任何 LLM 编程助手的行为 |
| **代码审查** | ★★★★★ | 作为人工审查的检查清单 |
| **团队规范** | ★★★★★ | 作为团队编码规范基础 |
| **Claude Code 用户** | ★★★★★ | 直接作为插件使用 |
| **Cursor/其他AI工具** | ★★★★☆ | 添加到系统提示词 |

### 使用方法

#### 个人项目

```bash
# 添加到项目
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

#### 团队项目

```bash
# 追加到现有 CLAUDE.md
cat >> CLAUDE.md << 'EOF'

## Project-Specific Guidelines

- Use TypeScript strict mode
- All API endpoints must have tests
- Follow the existing error handling patterns in `src/utils/errors.ts`
EOF
```

#### Claude Code 插件

```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

### 与其他工具结合

| 工具 | 结合方式 |
|------|----------|
| **Claude Code** | 作为插件安装 |
| **Cursor** | 添加到 .cursorrules |
| **GitHub Copilot** | 添加到项目提示词 |
| **OpenAI Codex** | 添加到 AGENTS.md |
| **其他 LLM 工具** | 添加到系统提示词 |

---

## 总结

Andrej Karpathy Skills 是一个极简但极具影响力的项目，它不是一个软件工具，而是一套**AI 时代的行为准则**。

**核心价值**:
- 基于行业顶尖专家 (Andrej Karpathy) 的观察
- 直接解决 LLM 编程的核心痛点
- 极简设计，零成本采用
- 可与其他工具无缝结合

**设计智慧**:
- 不增加复杂度，而是减少
- 不限制能力，而是引导
- 不替代判断，而是增强

**最佳实践**:
- 添加到所有 AI 辅助编程项目
- 与项目特定规范结合使用
- 对简单任务灵活应用
- 对复杂任务严格执行

**影响力**:
- 36,490+ Stars 证明了社区对 AI 行为规范的强烈需求
- 被多个主流 AI 编程工具采用或推荐
- 成为 AI 辅助编程的最佳实践参考

---

## 附录：相关项目

> **Looking for a managed agents platform?** 
> Check out [Multica](https://github.com/multica-ai/multica) — 
> an open-source platform for running and managing coding agents with reusable skills.
