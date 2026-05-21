# Source Code Analyzer Skill

A Qoder CLI skill for systematic analysis of open-source projects. Extracts architecture patterns, design philosophies, and actionable insights from codebases.

## Skill Structure

```
source-code-analyzer/
├── SKILL.md                    # Skill entry point (Qoder CLI loads this)
├── README.md                   # This file
├── templates/                  # 21 analysis dimension templates
│   ├── T1-architecture.md      # Architecture patterns
│   ├── T2-philosophy.md        # Design philosophy
│   ├── T3-conventions.md       # Code conventions
│   ├── T4-performance.md       # Performance optimization
│   ├── T5-security.md          # Security practices
│   ├── T6-testing.md           # Testing strategy
│   ├── T7-data-arch.md         # Data architecture
│   ├── T8-api-design.md        # API design
│   ├── P1-product.md           # Product design
│   ├── P2-competitor.md        # Competitor analysis
│   ├── P3-user-research.md     # User research
│   ├── O1-growth.md            # Growth strategy
│   ├── O2-community.md         # Community operations
│   ├── O3-content.md           # Content strategy
│   ├── A1-agent-arch.md        # Agent architecture
│   ├── A2-rag.md               # RAG system
│   ├── A3-ai-eval.md           # AI evaluation
│   ├── A4-ai-cost.md           # AI cost optimization
│   ├── B1-business.md          # Business model
│   ├── B2-compliance.md        # Compliance & risk
│   └── X1-quick-ideas.md       # Quick analysis (5 min)
└── examples/                   # Example analysis outputs
    └── TradingAgents-analysis.md
```

## Module Map

The 21 templates are organized into **6 domains**:

| Domain | Code | Templates | Focus |
|--------|------|-----------|-------|
| **Technical** | T1-T8 | 8 | Code architecture, patterns, engineering practices |
| **Product** | P1-P3 | 3 | Product design, competitors, user research |
| **Operations** | O1-O3 | 3 | Growth, community, content strategy |
| **AI/Agent** | A1-A4 | 4 | Agent arch, RAG, evaluation, cost optimization |
| **Business** | B1-B2 | 2 | Business model, compliance |
| **Express** | X1 | 1 | 5-minute quick analysis |

## Auto-Detection Rules

The skill auto-selects templates based on project type:

| Project Type | Detection Signal | Recommended Templates |
|---|---|---|
| AI/Agent/LLM | `langchain`, `langgraph`, `openai`, agent directories | T1, T2, A1, A2, A3, A4 |
| Web Framework | `express`, `fastapi`, `next.config`, `routes/` | T1, T2, T3, T8, P1 |
| CLI Tool | `commander`, `clap`, `cobra`, `argparse` | T1, T2, T3, P1 |
| Infrastructure | `docker-compose`, `terraform`, `k8s` | T1, T4, T5, T7 |
| Open Source Product | High GitHub stars, active community | T1, T2, P1, O1, O2 |
| Data Pipeline | `airflow`, `spark`, `dbt`, ETL patterns | T1, T7, T4 |

## Usage

```bash
# In Qoder CLI, trigger with:
/source-code-analyzer

# Or naturally:
"Analyze the architecture of this project"
"What patterns does this codebase use?"
"Give me insights from this open source project"
```

## Analysis Methodology

Every analysis answers three questions:
1. **So what?** -- Every technical detail must explain its value to the reader
2. **Why?** -- Not just what the code does, but why it was designed this way
3. **Then what?** -- What can the reader do with this knowledge?

## Output

Reports are saved to:
```
~/Documents/AI/opensource/OpenSource/GitHubProject/<project>-analysis.md
```

Each report includes Obsidian-compatible YAML frontmatter for knowledge graph integration.
