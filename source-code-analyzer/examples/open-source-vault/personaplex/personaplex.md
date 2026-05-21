---
title: "PersonaPlex"
aliases: [PersonaPlex]
tags:
  - opensource
  - voice-ai
  - NVIDIA
  - Python
github: https://github.com/nicepkg/personaplex
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# PersonaPlex

> **Voice and Role Control for Full Duplex Conversational Speech Models**

---

## 项目简介

PersonaPlex 是 NVIDIA 开发的实时全双工语音对话模型，基于 Moshi 架构和 Helium LLM 构建。该模型支持通过文本角色提示和音频语音条件控制来生成自然、低延迟的语音交互，并保持一致的角色特征。

**核心特点：**
- 实时全双工语音对话（支持同时听和说）
- 通过文本提示控制角色（如客服、助手、休闲对话者）
- 通过音频嵌入控制语音特征（支持16种预设声音）
- 基于 Moshi 架构和 Kyutai 的 Helium LLM
- 支持用户打断、回话、流畅的轮流对话

**项目链接：**
- GitHub: https://github.com/NVIDIA/personaplex
- 模型权重: https://huggingface.co/nvidia/personaplex-7b-v1
- 论文: https://arxiv.org/abs/2602.06053
- Demo: https://research.nvidia.com/labs/adlr/personaplex/

---

## 技术栈分析

### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.10 | 核心运行时 |
| PyTorch | >= 2.2.0, < 2.5 | 深度学习框架 |
| numpy | >= 1.26, < 2.2 | 数值计算 |
| safetensors | >= 0.4.0 | 模型权重加载 |
| huggingface-hub | >= 0.24 | 模型下载 |
| einops | 0.7 | 张量操作 |
| sentencepiece | 0.2 | 文本分词 |
| sounddevice | 0.5 | 音频设备接口 |
| sphn | >= 0.1.4 | 音频处理 |
| aiohttp | >= 3.10.5 | Web 服务器 |
| accelerate | 可选 | CPU 卸载支持 |

### 前端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| TypeScript | ^5.2.2 | 类型安全 |
| React | ^18.3.1 | UI 框架 |
| Vite | ^5.2.14 | 构建工具 |
| Tailwind CSS | ^3.4.3 | 样式框架 |
| DaisyUI | ^4.12.2 | UI 组件库 |
| Opus Recorder | ^8.0.5 | 音频录制 |
| WebSocket (ws) | ^8.16.0 | 实时通信 |

### 模型架构
- **基础架构**: Moshi (Kyutai)
- **LLM 骨干**: Helium (7B 参数)
- **音频编解码器**: Mimi (24kHz, 12.5fps)
- **分词器**: SentencePiece (32k 词汇表)
- **量化**: 8-stream RVQ (Residual Vector Quantization)

---

## 核心功能模块

### 1. 语音生成模块 (`moshi/models/lm.py`)
- **LMModel**: 核心语言模型，处理文本和音频token
- **LMGen**: 生成器，管理自回归生成过程
- **StreamingStateDict**: 流式状态管理
- **延迟模式 (Delay Pattern)**: 处理多流音频token的时间对齐

### 2. 音频编解码器 (`moshi/models/compression.py`)
- **MimiModel**: 神经音频编解码器
- **SEANet 编码器/解码器**: 卷积音频处理
- **RVQ 量化器**: 残差向量量化 (32层, 2048 bins)
- **采样率**: 24kHz 输入/输出，12.5Hz 帧率

### 3. 流式Transformer (`moshi/modules/transformer.py`)
- **StreamingTransformer**: 支持流式推理的Transformer
- **RMSNorm**: 均方根层归一化
- **RoPE (Rotary Embeddings)**: 旋转位置编码
- **CUDA Graphs 优化**: 推理加速

### 4. Web 服务器 (`moshi/server.py`)
- **aiohttp 服务器**: 处理 WebSocket 连接
- **SSL 支持**: 自动生成临时证书
- **语音提示加载**: 支持 .pt 格式的语音嵌入
- **文本提示处理**: 支持系统标签包装

### 5. 离线评估 (`moshi/offline.py`)
- **批量处理**: 输入 WAV 文件，输出 WAV + JSON
- **语音条件**: 支持语音提示文件
- **文本条件**: 支持角色提示文件
- **种子控制**: 可复现的生成结果

---

## 代码结构概览

```
personaplex/
├── moshi/                          # Python 后端包
│   ├── __init__.py
│   ├── server.py                   # Web 服务器入口 (20KB)
│   ├── offline.py                  # 离线评估脚本 (16KB)
│   ├── client_utils.py             # 客户端工具 (6KB)
│   ├── models/                     # 模型定义
│   │   ├── __init__.py
│   │   ├── lm.py                   # 语言模型 (47KB)
│   │   ├── compression.py          # 音频编解码 (17KB)
│   │   └── loaders.py              # 模型加载器 (13KB)
│   ├── modules/                    # 神经网络模块
│   │   ├── __init__.py
│   │   ├── transformer.py          # Transformer (28KB)
│   │   ├── seanet.py               # SEANet (17KB)
│   │   ├── streaming.py            # 流式处理 (24KB)
│   │   ├── conv.py                 # 卷积模块 (12KB)
│   │   ├── rope.py                 # RoPE (4KB)
│   │   ├── gating.py               # 门控机制 (4KB)
│   │   └── resample.py             # 重采样 (5KB)
│   ├── quantization/               # 量化模块
│   │   ├── __init__.py
│   │   ├── base.py                 # 基础量化 (6KB)
│   │   ├── core_vq.py              # VQ 核心 (14KB)
│   │   └── vq.py                   # 向量量化 (15KB)
│   └── utils/                      # 工具函数
│       ├── __init__.py
│       ├── compile.py              # CUDA Graphs (12KB)
│       ├── connection.py           # 连接工具 (7KB)
│       ├── logging.py              # 日志 (3KB)
│       ├── sampling.py             # 采样 (6KB)
│       └── autocast.py             # 自动类型转换 (2KB)
├── client/                         # React 前端
│   ├── src/
│   │   ├── app.tsx                 # 应用入口
│   │   ├── audio-processor.ts      # 音频处理 (6KB)
│   │   ├── decoder/                # Opus 解码器
│   │   ├── pages/
│   │   │   ├── Conversation/       # 对话页面 (10KB)
│   │   │   │   ├── Conversation.tsx
│   │   │   │   ├── components/     # UI 组件
│   │   │   │   └── hooks/          # React hooks
│   │   │   └── Queue/              # 队列页面
│   │   └── protocol/               # 通信协议
│   ├── package.json                # npm 配置
│   └── index.html
├── assets/                         # 测试资源
│   ├── architecture_diagram.png    # 架构图
│   └── test/                       # 测试音频和提示
├── pyproject.toml                  # Python 包配置
├── requirements.txt                # 依赖列表
└── README.md                       # 项目文档
```

---

## 关键实现亮点

### 1. 全双工对话架构
```python
# 核心参数 (moshi/models/lm.py)
AUDIO_TOKENS_PER_STREAM = 8      # 8 流音频 token
FRAME_RATE_HZ = 12.5             # 12.5 Hz 帧率
SILENCE_TOKENS = [...]           # 静音 token 定义
SINE_TOKENS = [...]              # 正弦波 token 定义
```

### 2. 延迟模式处理
- 使用 `_delay_sequence` 和 `_undelay_sequence` 处理多流音频token的时间对齐
- 支持可配置的延迟列表，确保音频流正确交错

### 3. 流式推理优化
- **StreamingTransformer**: 支持逐帧处理，无需等待完整序列
- **CUDA Graphs**: 通过 `CUDAGraphed` 类捕获和重放 CUDA 操作，减少 CPU 开销
- **状态管理**: `StreamingStateDict` 管理 KV 缓存和流式状态

### 4. 语音条件控制
```python
# server.py 中的语音提示处理
voice_prompt: str = "NATF2.pt"   # 自然女声预设
text_prompt: str = "You are a wise and friendly teacher..."
```
- 支持 16 种预设声音 (NATF0-3, NATM0-3, VARF0-4, VARM0-4)
- 语音嵌入通过 .pt 文件加载，在生成时作为条件

### 5. 多平台支持
- **Web UI**: React + WebSocket 实时通信
- **离线模式**: 命令行批量处理
- **Docker 支持**: 容器化部署

---

## 适用场景建议

### 1. 智能客服系统
- **场景**: 银行、电信、电商的语音客服
- **优势**: 低延迟响应、可定制的角色声音、支持打断
- **部署**: 服务器端运行，通过 WebSocket 连接客户端

### 2. 语音助手应用
- **场景**: 个人助理、智能家居控制
- **优势**: 自然对话流、多角色切换、情感表达
- **集成**: 可嵌入移动应用或智能设备

### 3. 教育和培训
- **场景**: 语言学习、在线辅导
- **优势**: 耐心的教师角色、可重复练习、即时反馈
- **定制**: 通过文本提示定义教学风格

### 4. 游戏和娱乐
- **场景**: NPC 对话、互动故事
- **优势**: 沉浸式语音交互、角色一致性
- **扩展**: 可训练自定义角色声音

### 5. 无障碍应用
- **场景**: 视障用户界面、语音导航
- **优势**: 纯语音交互、自然对话
- **考虑**: 需要处理噪音环境和口音变化

---

## 性能指标

| 指标 | 数值 |
|------|------|
| 模型参数 | 7B |
| 音频采样率 | 24kHz |
| 帧率 | 12.5 Hz |
| 音频流数 | 8 |
| 量化层数 | 32 |
| 词汇表大小 | 32k (文本) + 2048 (音频) |
| 理论延迟 | < 200ms (GPU) |

---

## 许可证

- **代码**: MIT License
- **模型权重**: NVIDIA Open Model License

---

## 引用

```bibtex
@misc{roy2026personaplexvoicerolecontrol,
  title={PersonaPlex: Voice and Role Control for Full Duplex Conversational Speech Models},
  author={Rajarshi Roy and Jonathan Raiman and Sang-gil Lee and Teodor-Dumitru Ene and Robert Kirby and Sungwon Kim and Jaehyeon Kim and Bryan Catanzaro},
  year={2026},
  eprint={2602.06053},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2602.06053},
}
```
