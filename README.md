# Claude Skills · 知识库工具集

> 两个互补的 Claude Code Skill,把"开源源码学习 → Obsidian 知识库沉淀"做成自动化闭环。
>
> **通用工具**——无任何业务/组织特定逻辑,所有路径与场景通过 `VAULT-SCHEMA.md` 配置驱动。

---

## 📦 包含的 Skills

### 1. `source-code-analyzer/` — 开源项目系统性分析

按多维度(架构 / 设计理念 / Agent 架构 / RAG / 业务策略 等)分析开源项目源码,产出结构化分析报告。

**触发**:`分析源码`、`拆解开源项目`、`提取架构模式`、`analyze repo` ...

**核心**:
- 4 步骤工作流(扫描 → 维度选择 → 深度分析 → 输出报告)
- 20+ 分析维度模板(`templates/`)

### 2. `obsidian-vault-curator/` — Obsidian 知识库自维护

按 vault 内 `VAULT-SCHEMA.md` 规范扫描笔记,自动修机械问题(命名/frontmatter),语义问题写 BACKLOG 等人工裁决,生成 audit 时间序列报告。

**触发**:`/obsidian-curate`、`维护知识库`、`扫描 vault`、`找孤立笔记` ...

**核心**:
- **规范=数据 / 逻辑=代码**:`VAULT-SCHEMA.md` 放 vault(用户改),scripts 放 skill(版本化)
- **机械自动 / 语义等人**:命名/frontmatter 自动修;关联/合并写 BACKLOG
- **autoresearch 闭环**:audit 时间序列 + BACKLOG 信心累积(连续 3 次有效升至自动修候选)
- **零运行时依赖**:纯 Python stdlib;装 Dataview 更好,没装也能跑

---

## 🔁 两个 Skill 如何协同

```
   用户:"分析 hermes-agent 这个开源项目"
              ↓
   ┌──────────────────────────┐
   │  source-code-analyzer     │  产出:hermes-agent.md / analysis.md / learning-plan.md
   └──────────────┬───────────┘
                  │ Mode B 联动
                  ▼
   ┌──────────────────────────┐
   │  obsidian-vault-curator   │  按 SCHEMA 归位:
   │                          │    1. 落到 <vault>/<分区>/hermes-agent/
   └──────────────────────────┘    2. 补 frontmatter
                                   3. 加横向关联
                                   4. 写入 audit + BACKLOG
```

---

## 🚀 安装(2 种方式)

详见 [INSTALL.md](./INSTALL.md)。

最简:
```bash
git clone https://github.com/<you>/claude-skills-knowledge-tools.git ~/repos/claude-skills
ln -s ~/repos/claude-skills/obsidian-vault-curator ~/.claude/skills/obsidian-vault-curator
ln -s ~/repos/claude-skills/source-code-analyzer    ~/.claude/skills/source-code-analyzer
cp ~/.claude/skills/obsidian-vault-curator/templates/VAULT-SCHEMA.md "$OBSIDIAN_VAULT/"
```

---

## 🧱 设计理念

| 原则 | 体现 |
|------|------|
| **规范 = 数据,逻辑 = 代码** | 用户能不改代码改行为(改 VAULT-SCHEMA.md 即可) |
| **机械自动 / 语义等人** | 高确定性问题自动修,模糊问题写 BACKLOG 留人 |
| **增量优先** | 默认 `--since=7d`,避免每次重扫全 vault |
| **autoresearch 闭环** | 借鉴 hermes-agent 的 Curator(7 天周期)+ Background Review(每轮评估)双层 |
| **零运行时依赖** | 纯 Python stdlib;Obsidian Dataview 装了更好,没装也能跑 |

---

## 📊 使用案例

| 场景 | 命令 |
|------|------|
| 冷启动 vault baseline | `/obsidian-curate --full --apply` |
| 日常增量 | `/obsidian-curate` → 看报告 → `/obsidian-curate --apply` |
| 周期自维护 | `/loop 7d /obsidian-curate --since=7d --synthesize --apply` |
| 跨笔记模式提取 | `/obsidian-curate --scope=<分区> --synthesize` |
| 只补 frontmatter 不动链接 | `/obsidian-curate --apply --frontmatter-only` |

---

## 🛠️ 依赖

- **必需**:Python 3.11+(纯 stdlib,无 pip 依赖)
- **强烈建议**:Obsidian + [Dataview 插件](https://github.com/blacksmithgu/obsidian-dataview)(让 audit 报告里的查询块变实时表)
- **可选**:vault 在 git 管理下(供 frontmatter 用 git first commit 时间)

---

## 🤝 贡献

PRs welcome。请遵守:
- 不引入任何业务/组织特定字眼到 skill 代码或文档(可通过 grep 验证)
- 任何路径/scope/exempt 都通过 `VAULT-SCHEMA.md` 配置,不硬编码
- 改 SKILL.md 前先在本地 `~/.claude/skills/<name>/` 验证 Claude 能识别

---

## 📜 License

MIT(见 [LICENSE](./LICENSE))
