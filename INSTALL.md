# Installation Guide

## 前置

- macOS / Linux(Windows 未测试)
- Python 3.11+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)(否则 skill 触发不了)
- Obsidian + [Dataview 插件](https://github.com/blacksmithgu/obsidian-dataview)(强烈建议,让 audit 报告里的查询块变实时表)

---

## 方式 A:Symlink(推荐)

让 `~/.claude/skills/` 指向 git 仓库,改完代码立即在 Claude Code 生效。

```bash
# 1. clone 仓库到你常用的代码目录
git clone https://github.com/<你>/claude-skills-knowledge-tools.git ~/repos/claude-skills
cd ~/repos/claude-skills

# 2. symlink 到 Claude Code skill 目录
ln -s "$(pwd)/obsidian-vault-curator" ~/.claude/skills/obsidian-vault-curator
ln -s "$(pwd)/source-code-analyzer"   ~/.claude/skills/source-code-analyzer

# 3. 验证 Claude Code 看到 skill
ls ~/.claude/skills/ | grep -E "obsidian-vault-curator|source-code-analyzer"
```

---

## 方式 B:Copy(独立副本)

如果你不想让 skill 跟着仓库改动,用 cp。

```bash
git clone https://github.com/<你>/claude-skills-knowledge-tools.git /tmp/cs
cp -r /tmp/cs/obsidian-vault-curator ~/.claude/skills/
cp -r /tmp/cs/source-code-analyzer    ~/.claude/skills/
rm -rf /tmp/cs
```

---

## 配置你的 Obsidian Vault

`obsidian-vault-curator` skill 需要你的 vault 根目录有 `VAULT-SCHEMA.md` 才能工作。

```bash
# 1. 设 vault 路径环境变量(可选,默认从 Claude CLAUDE.md 读)
export OBSIDIAN_VAULT="/path/to/your/Obsidian Vault"

# 2. 复制规范模板到 vault 根
cp ~/.claude/skills/obsidian-vault-curator/templates/VAULT-SCHEMA.md "$OBSIDIAN_VAULT/"

# 3. 按你的 vault 结构编辑 §9 异常清单(把 work/、journal/ 等加入 exempt_paths)
$EDITOR "$OBSIDIAN_VAULT/VAULT-SCHEMA.md"

# 4. 跑第一次 baseline 扫描
cd "$OBSIDIAN_VAULT"
python3 ~/.claude/skills/obsidian-vault-curator/scripts/scan.py --full && \
python3 ~/.claude/skills/obsidian-vault-curator/scripts/score.py && \
python3 ~/.claude/skills/obsidian-vault-curator/scripts/auto_fix.py && \
python3 ~/.claude/skills/obsidian-vault-curator/scripts/audit_report.py

# 5. 在 Obsidian 里打开 audit/YYYY-MM-DD/INDEX.md 看首份报告
```

---

## 安装 Dataview 插件(让报告变实时)

`audit/*` 报告里嵌入了 Dataview 查询块,装了 Dataview 它们会渲染为实时表格。

**方式 A:Obsidian 内安装**
- Settings → Community plugins → Browse → 搜 "Dataview" → Install → Enable

**方式 B:手动安装**
```bash
mkdir -p "$OBSIDIAN_VAULT/.obsidian/plugins/dataview"
curl -sL -o "$OBSIDIAN_VAULT/.obsidian/plugins/dataview/main.js"      https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/main.js
curl -sL -o "$OBSIDIAN_VAULT/.obsidian/plugins/dataview/manifest.json" https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/manifest.json
curl -sL -o "$OBSIDIAN_VAULT/.obsidian/plugins/dataview/styles.css"    https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/styles.css

# 把 dataview 加到启用列表
python3 -c "
import json, pathlib
p = pathlib.Path('$OBSIDIAN_VAULT/.obsidian/community-plugins.json')
plugins = json.loads(p.read_text()) if p.exists() else []
if 'dataview' not in plugins:
    plugins.append('dataview')
    p.write_text(json.dumps(plugins, indent=2))
print('Enabled')
"
```

重启 Obsidian 即可。

---

## 验证

在 Claude Code 里输入:
```
/obsidian-curate --since=7d
```

预期:Claude 识别到 skill,跑 scan→score→dry-run→audit_report 链路,告诉你本次发现什么。

---

## 卸载

```bash
# 删 symlink(方式 A)
rm ~/.claude/skills/obsidian-vault-curator ~/.claude/skills/source-code-analyzer

# 或删副本(方式 B)
rm -rf ~/.claude/skills/obsidian-vault-curator ~/.claude/skills/source-code-analyzer

# 保留 vault 里的 VAULT-SCHEMA.md / BACKLOG.md / audit/ — 这些是你 vault 的数据,与 skill 解耦
```
