---
title: "PM Skills Marketplace 源码分析报告"
aliases: [PM Skills, pm-skills]
tags:
  - opensource
  - source-analysis
  - ai-skill
  - Python
github: https://github.com/nicepkg/pm-skills
created: 2026-04-15
updated: 2026-04-15
score: 5.1
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# PM Skills Marketplace — 源码分析报告

> **一句话定位**：把顶级 PM 方法论（Torres、Cagan、Savoia）编码成 AI 可执行的技能链，让 Claude 成为随时在线的产品顾问。

---

## 这个项目解决了什么问题？

**通用 AI 给你文字，PM Skills 给你结构。**

产品经理用 AI 时面临的痛点不是 AI 不够智能，而是：

1. **框架缺失**：问 ChatGPT 如何做用户调研，得到的是模糊建议，不是 Teresa Torres 的 OST 方法论
2. **流程断裂**：每次从头提示词，没有从 Discovery → Strategy → Execution → Launch 的连贯工作流
3. **知识沉没**：优秀的 PM 书籍（INSPIRED、Continuous Discovery Habits）在书架上，不在工作流里

PM Skills 做的事：**把书架变成工具箱**——将 12 位 PM 大师的方法论拆解成 65 个具名技能，让 AI 在正确场景自动调用正确框架。

---

## 新思路与设计亮点

### 1. Skills → Commands → Plugins 三层架构：知识的乐高积木

```
Skills（技能单元）
  ↓ 组合
Commands（工作流命令）
  ↓ 打包
Plugins（领域插件包）
  ↓ 集合
Marketplace（技能市场）
```

这是这个项目最核心的架构洞见：**把 AI Prompt 工程做成了乐高积木**。

- **Skills** 是原子单元：`opportunity-solution-tree` 就是 OST 方法论，`prioritize-assumptions` 就是 Impact × Risk 矩阵
- **Commands** 是技能链：`/discover` = brainstorm-ideas → identify-assumptions → prioritize-assumptions → brainstorm-experiments，四个技能自动串联
- **Plugins** 是领域聚合：按 PM 职能领域打包，可独立安装，按需取用

**为什么这个设计好**：技能可复用——同一个 `prioritization-frameworks` 技能被多个命令共享，不需要重复定义。这是软件工程里 DRY 原则在 AI Prompt 领域的应用。

---

### 2. 命令内置下一步建议：工作流的自然流动

每个命令执行完毕都会主动建议下一个命令：

```
/discover 执行完 → 建议 /write-prd
/write-prd 执行完 → 建议 /plan-okrs 或 /sprint
/sprint 执行完 → 建议 /sprint retro
```

这不是功能点，是**产品哲学**：PM 的工作本质上是流程化的，工具应该引导流程而不是让用户记忆流程。工具知道你下一步该做什么。

**对比**：普通 ChatGPT 对话是无状态的，每次都要重新构建上下文。这里的命令链让 AI 工具有了**工作流记忆**。

---

### 3. 情景感知的双轨技能：新产品 vs 现有产品

项目专门区分了两类场景，且提供不同的技能实现：

| 场景 | 技能 |
|------|------|
| 已有产品 | `brainstorm-ideas-existing`、`identify-assumptions-existing` |
| 新产品 | `brainstorm-ideas-new`、`identify-assumptions-new` |

新产品多覆盖 8 个风险维度（含 Go-to-Market、Strategy、Team），已有产品聚焦 4 个（Value、Usability、Feasibility、Viability）。

**洞见**：大多数 AI 工具忽略"情景差异"。这里把这个差异显式建模到技能层，说明作者对 PM 工作有深刻理解——Lean Startup 阶段的假设识别与持续 Discovery 阶段根本不同。

---

### 4. 多平台兼容策略：SKILL.md 的通用格式

项目支持 Claude、Gemini CLI、OpenCode、Cursor、Codex CLI、Kiro 等多个 AI 工具：

```bash
# 一键迁移到任意工具
for plugin in pm-*/; do
  cp -r "$plugin/skills/"* ~/.gemini/skills/
done
```

**关键设计**：Skills 用 SKILL.md 通用格式，Commands（/slash-commands）是 Claude 专有的。把可移植的部分和平台专有的部分清晰分离。

这是一个**平台无关的知识资产**策略——把方法论沉淀在标准格式里，不锁定单一平台。

---

### 5. validate_plugins.py：Prompt 工程的质量门控

项目内置了一个验证脚本，用于检查所有 Plugin 的合规性：

- YAML Frontmatter 必填字段检查
- 技能名称与目录名一致性校验
- 命令跨引用技能的存在性验证
- README 结构完整性检查
- 技能词数上限（>3000 words → 警告）

**这个细节揭示了作者的认知**：Prompt 也是代码，也需要代码质量管理。大多数 AI Prompt 项目是随意的，这里有严格的规范体系，还有自动化验证工具确保执行。

---

## 方法论嵌入深度：技能内容设计

以 `/discover` 命令为例，它的工作流设计：

```
Step 1: 判断产品阶段（新 or 已有）
Step 2: 多视角发散（PM/Designer/Engineer 三视角各10个想法）
Step 3: 用户筛选（选3-5个继续）
Step 4: 假设识别（按风险分类）
Step 5: 假设优先级（Impact × Risk 矩阵）
Step 6: 实验设计（pretotype/A-B test/landing page）
Step 7: 输出 Discovery Plan 文档
Step 8: 建议下一步命令
```

每个 Checkpoint 设计得很精妙：先发散、再收敛、再聚焦、再验证。这不是 AI 生成的流程，是 Teresa Torres《Continuous Discovery Habits》的核心方法论的精确实现。

**关键**：技能文档不只是说"做发散"，而是说"从 PM、Designer、Engineer 三个角色视角生成想法，每个视角 3-4 个，合计展示 Top 10"。越具体，AI 执行质量越高。

---

## 值得学习的模式

### 模式一：方法论的可执行化

**问题**：好的方法论往往停留在概念层，难以在实际工作中执行。

**解法**：把方法论拆解成"在这个步骤，AI 应该做具体什么事，问用户什么问题，输出什么格式"。

**可迁移**：任何领域的知识密集型工作（法律、财务、设计、市场）都可以用这个思路构建 AI 技能包。

---

### 模式二：显式的 Checkpoint 设计

工作流中关键节点设置用户确认点：

```
"Here are 10 ideas. Which ones should we stress-test? Pick 3-5, or I can carry all forward."
```

这避免了 AI 自作主张继续走，让用户始终在驾驶位。**AI 做高质量的分析工作，人做判断和决策**，这是 Human-in-the-loop 的正确打开方式。

---

### 模式三：技能的原子化 + 可组合

不是写一个大而全的"PM助手"，而是把每个工具拆成最小单元，再通过命令组合。这让技能可以：
- 被多个命令复用
- 独立调用而不触发完整流程
- 随时扩展新技能不破坏现有结构

---

### 模式四：明确区分"技能"和"命令"

- **技能**：AI 获得的能力/知识（自动激活，按需调用）
- **命令**：用户主动触发的流程（`/discover`）

这个区分让 AI 工具有了两种工作模式：被动辅助（技能隐式激活）和主动驱动（命令显式执行）。

---

## 项目的局限与取舍

| 取舍 | 分析 |
|------|------|
| Claude 平台依赖 | Commands（斜杠命令）绑定 Claude Code，其他工具只能用 Skills |
| 无状态持久化 | 每次对话结束，工作进度不会保留，Discovery Plan 需手动存档 |
| 人工维护成本 | 65个技能、36个工作流，随 PM 方法论演进需要持续更新 |
| 方法论权威性 | 选择了主流但特定的方法论体系，与公司内部 PM 流程可能不匹配 |

---

## 个人启发

**这个项目证明了一件事**：AI 的价值不在于它知道多少，而在于**它知道在什么情况下用什么框架思考问题**。

给 AI 一个大而全的指令不如给它一个精准的场景化技能。PM Skills 的核心贡献是**把隐性的专家知识（PM 大师方法论）转化成显性的、AI 可执行的结构化工作流**。

对于任何知识工作者：如果你正在重复地用 AI 做某类专业工作，值得考虑是否可以把这个工作流做成可复用的"技能包"——不只给自己用，而是让整个团队的 AI 都具备这个能力。

---

## 快速上手

```bash
# Claude Code 安装
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-execution@pm-skills

# 核心命令速查
/discover     # 新想法 → 完整探索周期
/write-prd    # 写 PRD
/strategy     # 产品策略画布
/plan-launch  # GTM 策略
/north-star   # 定义北极星指标
/analyze-test # A/B 测试分析
```

---

**分析日期**：2026-03-31  
**项目地址**：https://github.com/phuryn/pm-skills  
**作者**：Paweł Huryn（The Product Compass Newsletter）
