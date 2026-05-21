---
title: "MarkItDown"
aliases: [MarkItDown, markitdown]
tags:
  - opensource
  - data-processing
  - Python
  - mcp
github: https://github.com/microsoft/markitdown
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# MarkItDown

> **GitHub**: [microsoft/markitdown](https://github.com/microsoft/markitdown)  
> **Stars**: 108,858  
> **Language**: Python  
> **License**: MIT  
> **Built by**: AutoGen Team (Microsoft)

---

## 项目简介

MarkItDown 是一个轻量级 Python 工具，用于将各种文件转换为 Markdown 格式，专为 LLM 和相关文本分析流程设计。它与 [textract](https://github.com/deanmalmgren/textract) 类似，但专注于保留重要的文档结构和内容（包括标题、列表、表格、链接等）。

**设计目标**：输出适合文本分析工具消费，而非高保真人类可读转换。

---

## 技术栈分析

### 核心依赖
| 组件 | 用途 |
|------|------|
| `beautifulsoup4` | HTML 解析 |
| `requests` | 网络请求 |
| `markdownify` | HTML 转 Markdown |
| `magika~=0.6.1` | 文件类型检测 (Google) |
| `charset-normalizer` | 字符编码检测 |
| `defusedxml` | 安全 XML 解析 |

### 可选依赖 (按格式)
| 功能 | 依赖包 |
|------|--------|
| **PDF** | pdfminer.six, pdfplumber |
| **Word** | mammoth, lxml |
| **Excel** | pandas, openpyxl, xlrd |
| **PowerPoint** | python-pptx |
| **Outlook** | olefile |
| **音频转录** | pydub, SpeechRecognition |
| **YouTube** | youtube-transcript-api |
| **Azure AI** | azure-ai-documentintelligence |

### 插件系统
- 支持第三方插件扩展
- 插件通过 entry_points (`markitdown.plugin`) 注册
- 官方 OCR 插件：`markitdown-ocr`
- 官方 MCP 插件：`markitdown-mcp`

---

## 核心功能模块

### 1. 文档转换器生态系统

| 转换器 | 支持格式 | 特性 |
|--------|----------|------|
| `PdfConverter` | PDF | 文本提取、表格识别、OCR 支持 |
| `DocxConverter` | Word (.docx) | 保留格式、数学公式 (OMML→LaTeX) |
| `PptxConverter` | PowerPoint | 幻灯片内容提取 |
| `XlsxConverter` | Excel (.xlsx) | 表格数据转换 |
| `XlsConverter` | 旧版 Excel (.xls) | 兼容格式 |
| `HtmlConverter` | HTML | 结构化转换 |
| `ImageConverter` | 图片 | EXIF 元数据、OCR (需 LLM) |
| `AudioConverter` | 音频 | 语音转录 |
| `YouTubeConverter` | YouTube URL | 字幕提取 |
| `WikipediaConverter` | Wikipedia URL | 文章提取 |
| `ZipConverter` | ZIP | 递归处理内容 |
| `EpubConverter` | EPUB | 电子书提取 |
| `OutlookMsgConverter` | Outlook (.msg) | 邮件提取 |
| `CsvConverter` | CSV | 表格转换 |
| `IpynbConverter` | Jupyter Notebook | 代码和输出提取 |

### 2. 智能文件类型检测
```python
import magika
m = magika.Magika()
result = m.identify_bytes(raw_bytes)
# 使用 Google 的 Magika 深度学习模型
```

### 3. 插件架构
```python
# 插件加载机制
for entry_point in entry_points(group="markitdown.plugin"):
    try:
        _plugins.append(entry_point.load())
    except Exception:
        warn(f"Plugin '{entry_point.name}' failed to load")
```

### 4. MCP 服务器支持
```bash
# 启动 MCP 服务器
python -m markitdown_mcp
```
支持 Claude Desktop 等 MCP 客户端集成。

---

## 代码结构概览

```
markitdown/
├── packages/
│   ├── markitdown/                 # 核心包
│   │   ├── src/markitdown/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py         # CLI 入口
│   │   │   ├── _markitdown.py      # 核心 MarkItDown 类
│   │   │   ├── _base_converter.py  # 转换器基类
│   │   │   ├── _stream_info.py     # 流信息处理
│   │   │   ├── _uri_utils.py       # URI 工具
│   │   │   ├── _exceptions.py      # 异常定义
│   │   │   ├── converters/         # 转换器实现
│   │   │   │   ├── __init__.py
│   │   │   │   ├── _pdf_converter.py
│   │   │   │   ├── _docx_converter.py
│   │   │   │   ├── _pptx_converter.py
│   │   │   │   ├── _xlsx_converter.py
│   │   │   │   ├── _html_converter.py
│   │   │   │   ├── _image_converter.py
│   │   │   │   ├── _audio_converter.py
│   │   │   │   ├── _youtube_converter.py
│   │   │   │   └── ...
│   │   │   └── converter_utils/    # 转换工具
│   │   │       └── docx/           # Word 特殊处理
│   │   │           └── math/       # 数学公式转换
│   │   └── tests/
│   │
│   ├── markitdown-mcp/             # MCP 服务器包
│   │   └── src/markitdown_mcp/
│   │
│   ├── markitdown-ocr/             # OCR 插件包
│   │   └── src/markitdown_ocr/
│   │       ├── _pdf_converter_with_ocr.py
│   │       ├── _docx_converter_with_ocr.py
│   │       ├── _pptx_converter_with_ocr.py
│   │       └── _xlsx_converter_with_ocr.py
│   │
│   └── markitdown-sample-plugin/   # 插件开发示例
│
├── pyproject.toml
└── README.md
```

---

## 关键实现亮点

### 1. 优先级转换器注册
```python
# 优先级值越小越先尝试
PRIORITY_SPECIFIC_FILE_FORMAT = 0.0   # 特定格式 (如 .docx, .pdf)
PRIORITY_GENERIC_FILE_FORMAT = 10.0   # 通用格式 (如 text/*)

@dataclass(kw_only=True, frozen=True)
class ConverterRegistration:
    converter: DocumentConverter
    priority: float
```

### 2. 流式处理架构
```python
class MarkItDown:
    def convert_stream(
        self,
        source: BinaryIO,           # 二进制文件流
        file_extension: str = None,
        url: str = None,
        **_kwargs,
    ) -> DocumentConverterResult:
        # 无需临时文件，直接处理流
```

### 3. LLM 集成 (图像描述)
```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="optional custom prompt"
)
result = md.convert("image.jpg")
```

### 4. Azure Document Intelligence 支持
```python
md = MarkItDown(docintel_endpoint="<endpoint>")
result = md.convert("document.pdf")
```

---

## 适用场景建议

### 适合场景
| 场景 | 说明 |
|------|------|
| **LLM 文档处理** | 将各种文档转为 Markdown 供 LLM 分析 |
| **RAG 系统** | 文档预处理和向量化前的格式统一 |
| **批量文档转换** | 命令行批量处理文件 |
| **内容提取** | 从 PDF、Word、PPT 中提取结构化文本 |
| **数据管道** | ETL 流程中的文档标准化步骤 |

### 使用方式

**命令行**
```bash
# 安装全部功能
pip install 'markitdown[all]'

# 基础转换
markitdown document.pdf > document.md
markitdown document.pdf -o document.md

# 使用 Azure Document Intelligence
markitdown document.pdf -o document.md -d -e "<endpoint>"

# 列出插件
markitdown --list-plugins

# 启用插件
markitdown --use-plugins document.pdf
```

**Python API**
```python
from markitdown import MarkItDown

# 基础使用
md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)

# 带 LLM 的图像描述
md = MarkItDown(
    llm_client=OpenAI(),
    llm_model="gpt-4o"
)
result = md.convert("image.png")

# 启用插件
md = MarkItDown(enable_plugins=True)
result = md.convert("scanned_document.pdf")
```

**Docker**
```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/document.pdf > output.md
```

### 安装选项
```bash
# 全部功能
pip install 'markitdown[all]'

# 按需安装
pip install 'markitdown[pdf,docx,pptx]'
pip install 'markitdown[audio-transcription]'
pip install 'markitdown[youtube-transcription]'
```

---

## 为什么选择 Markdown?

1. **接近纯文本**: 最小标记，保留结构
2. **LLM 原生理解**: GPT-4o 等模型在大量 Markdown 数据上训练
3. **Token 高效**: Markdown 约定高度节省 Token
4. **结构保留**: 标题、列表、表格、链接等结构清晰

---

## 相关资源

- **文档**: https://github.com/microsoft/markitdown#readme
- **MCP 插件**: [markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- **OCR 插件**: [markitdown-ocr](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr)
- **插件开发示例**: [markitdown-sample-plugin](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-sample-plugin)
- **AutoGen**: https://github.com/microsoft/autogen
