---
title: "Lightpanda Browser"
aliases: [Lightpanda, lightpanda-browser]
tags:
  - opensource
  - browser-automation
  - Zig
  - mcp
github: https://github.com/nicepkg/lightpanda
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Lightpanda Browser

## 项目简介

**Lightpanda** 是一个为 AI 代理和自动化设计的 headless 浏览器。它不是 Chromium 或 WebKit 的分支，而是使用 Zig 语言从头编写的全新浏览器引擎。

- **GitHub Stars**: 28,718
- **开发语言**: Zig
- **许可证**: GNU Affero General Public License v3.0
- **官方网址**: https://lightpanda.io

### 核心优势

| 指标 | Lightpanda | Headless Chrome | 差异 |
|------|-----------|-----------------|------|
| 内存（100 页面峰值） | 123MB | 2GB | ~16 倍节省 |
| 执行时间（100 页面） | 5s | 46s | ~9 倍更快 |

### 主要特性

- 完整的 JavaScript 执行（V8 引擎）
- DOM API 支持
- Ajax（XHR 和 Fetch API）
- CDP（Chrome DevTools Protocol）服务器
- Puppeteer 兼容
- MCP（Model Context Protocol）服务器
- 支持点击、表单输入、Cookie
- 代理支持和网络拦截
- 尊重 robots.txt

---

## 技术栈分析

### 核心语言与构建工具
| 技术 | 版本 | 用途 |
|------|------|------|
| Zig | 0.15.2 | 主要开发语言 |
| Rust | 最新 | html5ever HTML 解析器 |
| Make | - | 构建脚本 |
| Nix | 可选 | 开发环境 |

### 关键依赖
| 组件 | 库 | 说明 |
|------|-----|------|
| JavaScript 引擎 | V8 | Google V8（Chromium 同款） |
| HTTP 客户端 | libcurl | 网络请求 |
| HTML 解析 | html5ever | Mozilla 的 Rust HTML5 解析器 |
| TLS/SSL | BoringSSL | Google 的 SSL 库 |
| 压缩 | zlib, brotli | 内容编码支持 |
| HTTP/2 | nghttp2 | HTTP/2 协议支持 |

### 架构特点
- **零依赖渲染**: 无图形渲染引擎，纯 headless
- **显式内存管理**: Zig 的内存安全特性
- **模块化设计**: 清晰的模块边界（browser、js、dom、css 等）
- **跨平台**: Linux x86_64/aarch64, macOS aarch64/x86_64

---

## 核心功能模块

### 1. 浏览器核心 (`src/browser/`)
| 文件 | 功能 | 大小 |
|------|------|------|
| `Page.zig` | 页面管理 | 143.6 KB |
| `HttpClient.zig` | HTTP 客户端 | 64.5 KB |
| `ScriptManager.zig` | 脚本管理 | 36.0 KB |
| `StyleManager.zig` | CSS 样式管理 | 29.8 KB |
| `EventManager.zig` | 事件系统 | 22.5 KB |
| `Session.zig` | 会话管理 | 16.8 KB |
| `URL.zig` | URL 解析 | 66.1 KB |

### 2. JavaScript 绑定 (`src/browser/js/`)
- V8 引擎的 Zig 绑定
- JS 对象生命周期管理
- Promise 和异步处理
- 模块加载系统

### 3. DOM 实现 (`src/dom/`)
- DOM 树结构
- DOM API（querySelector、事件等）
- 节点操作

### 4. CSS 处理 (`src/browser/css/`)
- CSS 解析器（Tokenizer、Parser）
- 选择器匹配
- 样式计算

### 5. CDP 服务器 (`src/cdp/`)
- Chrome DevTools Protocol 实现
- WebSocket 通信
- Puppeteer 兼容接口

### 6. 网络层 (`src/browser/`)
- HTTP/HTTPS 请求
- Cookie 管理
- 缓存控制
- 代理支持

---

## 代码结构概览

```
browser/
├── src/
│   ├── main.zig                    # 主入口
│   ├── main_snapshot_creator.zig   # V8 快照生成器
│   ├── main_legacy_test.zig        # 遗留测试入口
│   ├── lightpanda.zig              # 核心库入口
│   ├── App.zig                     # 应用管理（3.4 KB）
│   ├── Config.zig                  # 配置解析（43.4 KB）
│   ├── Server.zig                  # CDP 服务器（29.7 KB）
│   ├── SemanticTree.zig            # 语义树（24.8 KB）
│   ├── browser/
│   │   ├── Browser.zig             # 浏览器实例
│   │   ├── Page.zig                # 页面（143.6 KB）
│   │   ├── HttpClient.zig          # HTTP 客户端（64.5 KB）
│   │   ├── ScriptManager.zig       # 脚本管理（36.0 KB）
│   │   ├── StyleManager.zig        # 样式管理（29.8 KB）
│   │   ├── EventManager.zig        # 事件管理（22.5 KB）
│   │   ├── Session.zig             # 会话（16.8 KB）
│   │   ├── URL.zig                 # URL 处理（66.1 KB）
│   │   ├── css/                    # CSS 处理
│   │   │   ├── Parser.zig
│   │   │   └── Tokenizer.zig
│   │   ├── js/                     # JS 绑定
│   │   │   ├── Context.zig
│   │   │   ├── Isolate.zig
│   │   │   ├── Local.zig
│   │   │   ├── Promise.zig
│   │   │   └── ...
│   │   └── ...
│   ├── dom/                        # DOM 实现
│   ├── html/                       # HTML 处理
│   ├── cdp/                        # CDP 协议
│   ├── network/                    # 网络层
│   └── tests/                      # 测试
├── src/html5ever/                  # Rust HTML5 解析器
│   ├── Cargo.toml
│   ├── lib.rs
│   └── sink.rs
├── build.zig                       # Zig 构建配置（31.9 KB）
├── build.zig.zon                   # 依赖管理
├── Makefile                        # 构建脚本
├── flake.nix                       # Nix 开发环境
└── Dockerfile                      # 容器镜像
```

---

## 关键实现亮点

### 1. Zig 语言优势
```zig
// 显式内存管理
var gpa_instance: std.heap.DebugAllocator(...) = .init;
const gpa = if (builtin.mode == .Debug) 
    gpa_instance.allocator() 
else 
    std.heap.c_allocator;

// 编译时检查
const Build = blk: {
    if (builtin.zig_version.order(min_zig_version) == .lt) {
        @compileError("Zig version is too old");
    }
    break :blk std.Build;
};
```

### 2. V8 集成
- 使用 V8 快照加速启动
- 支持嵌入式快照或运行时生成
- Zig 与 C++ 的 FFI 绑定

### 3. 模块化 HTTP 客户端
```zig
// libcurl 集成
fn linkCurl(b: *Build, mod: *Build.Module, is_tsan: bool) !void {
    const curl = buildCurl(b, target, optimize, is_tsan);
    const zlib = buildZlib(b, target, optimize, is_tsan);
    const brotli = buildBrotli(b, target, optimize, is_tsan);
    const nghttp2 = buildNghttp2(b, target, optimize, is_tsan);
    const boringssl = buildBoringSsl(b, target, optimize);
    // ... 链接所有依赖
}
```

### 4. CDP 协议兼容
- 实现 Chrome DevTools Protocol 子集
- 支持 Puppeteer 连接
- WebSocket 服务器模式

### 5. 跨平台构建
```zig
// 条件编译
const is_linux = os == .linux;
const is_darwin = os.isDarwin();
const is_windows = os == .windows;

// 平台特定代码
switch (target.result.os.tag) {
    .macos => {
        mod.linkFramework("CoreFoundation", .{});
        mod.linkFramework("SystemConfiguration", .{});
    },
    else => {},
}
```

### 6. 测试策略
- 单元测试：`make test`
- 端到端测试：`make end2end`
- Web Platform Tests：与 WPT 兼容

---

## 适用场景建议

### 适合的场景
1. **大规模网页抓取** - 需要同时运行数千实例
2. **AI 代理浏览** - 为 LLM 提供网页内容
3. **自动化测试** - 需要快速、轻量的浏览器
4. **服务器端渲染** - 资源受限的环境
5. **云原生应用** - 容器化部署，内存敏感

### 不适合的场景
1. **需要图形界面** - 纯 headless，无渲染
2. **复杂 WebGL** - 图形支持有限
3. **生产环境稳定性** - 目前处于 Beta 阶段

### 使用示例
```bash
# 安装（Linux）
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux
chmod a+x ./lightpanda

# 抓取页面
./lightpanda fetch --obey-robots --dump html https://example.com

# 启动 CDP 服务器
./lightpanda serve --host 127.0.0.1 --port 9222

# Docker 运行
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

### Puppeteer 集成
```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

const page = await browser.newPage();
await page.goto('https://example.com');
// ... 标准 Puppeteer API
```

### MCP 集成
```json
{
  "mcpServers": {
    "lightpanda": {
      "command": "/path/to/lightpanda",
      "args": ["mcp"]
    }
  }
}
```

---

## 开发指南

### 构建要求
- Zig 0.15.2
- Rust（用于 html5ever）
- clang、cmake、curl、git

### 构建命令
```bash
# 开发构建
make build-dev

# 发布构建
make build

# 运行测试
make test

# 生成 V8 快照
zig build snapshot_creator -- src/snapshot.bin
```

### 项目状态
- **当前状态**: Beta
- **稳定性**: 持续改进中
- **覆盖率**: 许多网站已可正常工作

---

## 相关链接

- **GitHub**: https://github.com/lightpanda-io/browser
- **官网**: https://lightpanda.io
- **文档**: https://lightpanda.io/docs
- **Discord**: https://discord.gg/K63XeymfB5
- **Twitter**: https://twitter.com/lightpanda_io
- **演示仓库**: https://github.com/lightpanda-io/demo
