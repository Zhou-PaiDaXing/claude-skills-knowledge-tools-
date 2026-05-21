#!/bin/bash
# 检测项目栈, 输出 JSON 给后续步骤直接消费
# 用法: ./detect_stack.sh [project_root]

ROOT="${1:-.}"
cd "$ROOT" || exit 1

LANGUAGES=()
FRAMEWORKS=()
TYPE="unknown"
SCALE="small"

# 语言 / 包管理器
[ -f "package.json" ] && LANGUAGES+=("javascript")
[ -f "tsconfig.json" ] && LANGUAGES+=("typescript")
[ -f "go.mod" ] && LANGUAGES+=("go")
[ -f "Cargo.toml" ] && LANGUAGES+=("rust")
[ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ] && LANGUAGES+=("python")
[ -f "pom.xml" ] || [ -f "build.gradle" ] || [ -f "build.gradle.kts" ] && LANGUAGES+=("java")
[ -f "Package.swift" ] && LANGUAGES+=("swift")
[ -f "build.sbt" ] && LANGUAGES+=("scala")
[ -f "Gemfile" ] && LANGUAGES+=("ruby")
[ -f "composer.json" ] && LANGUAGES+=("php")
ls *.csproj 2>/dev/null | grep -q . || ls *.sln 2>/dev/null | grep -q . && LANGUAGES+=("csharp")
ls *.kt 2>/dev/null | grep -q . || [ -f "build.gradle.kts" ] && LANGUAGES+=("kotlin")
[ -f "pubspec.yaml" ] && LANGUAGES+=("dart")

# 构建系统
[ -f "WORKSPACE" ] || [ -f "BUILD" ] || [ -f "BUILD.bazel" ] && FRAMEWORKS+=("bazel")
[ -f "Makefile" ] && FRAMEWORKS+=("make")
[ -f "CMakeLists.txt" ] && FRAMEWORKS+=("cmake")
[ -f ".bazelrc" ] && FRAMEWORKS+=("bazel")

# Monorepo 检测
[ -f "pnpm-workspace.yaml" ] && FRAMEWORKS+=("pnpm-workspace") && TYPE="monorepo"
[ -f "nx.json" ] && FRAMEWORKS+=("nx") && TYPE="monorepo"
[ -f "turbo.json" ] && FRAMEWORKS+=("turborepo") && TYPE="monorepo"
[ -f "lerna.json" ] && FRAMEWORKS+=("lerna") && TYPE="monorepo"

# Rust workspace
if [ -f "Cargo.toml" ] && grep -q "^\[workspace\]" "Cargo.toml" 2>/dev/null; then
  FRAMEWORKS+=("cargo-workspace")
  TYPE="monorepo"
fi

# Maven multi-module
if [ -f "pom.xml" ] && grep -q "<modules>" "pom.xml" 2>/dev/null; then
  FRAMEWORKS+=("maven-multi-module")
  TYPE="monorepo"
fi

# Gradle multi-project
if [ -f "settings.gradle" ] || [ -f "settings.gradle.kts" ]; then
  if grep -q "^include " "settings.gradle" "settings.gradle.kts" 2>/dev/null; then
    FRAMEWORKS+=("gradle-multi-project")
    TYPE="monorepo"
  fi
fi

# Android / iOS
[ -d "android" ] && [ -d "ios" ] && FRAMEWORKS+=("react-native") && TYPE="mobile"
[ -f "AndroidManifest.xml" ] || [ -f "app/build.gradle" ] && FRAMEWORKS+=("android") && TYPE="mobile"
if [ -f "Podfile" ] || ls -d *.xcworkspace 2>/dev/null | grep -q .; then
  FRAMEWORKS+=("ios")
  TYPE="mobile"
fi

# Frontend frameworks (语言已是 js/ts 时再检测)
if [ -f "package.json" ]; then
  grep -q "\"next\"" package.json 2>/dev/null && FRAMEWORKS+=("nextjs")
  grep -q "\"react\"" package.json 2>/dev/null && FRAMEWORKS+=("react")
  grep -q "\"vue\"" package.json 2>/dev/null && FRAMEWORKS+=("vue")
  grep -q "\"angular\"" package.json 2>/dev/null && FRAMEWORKS+=("angular")
  grep -q "\"svelte\"" package.json 2>/dev/null && FRAMEWORKS+=("svelte")
  [ "$TYPE" = "unknown" ] && TYPE="web"
fi

# Flutter (Dart)
[ -f "pubspec.yaml" ] && grep -q "flutter:" pubspec.yaml 2>/dev/null && FRAMEWORKS+=("flutter") && TYPE="mobile"

# Python web frameworks
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  grep -rql "fastapi\|FastAPI" . --include="*.py" 2>/dev/null | head -1 | grep -q . && FRAMEWORKS+=("fastapi")
  grep -rql "django\|Django" . --include="*.py" 2>/dev/null | head -1 | grep -q . && FRAMEWORKS+=("django")
  grep -rql "flask\|Flask" . --include="*.py" 2>/dev/null | head -1 | grep -q . && FRAMEWORKS+=("flask")
fi

# AI / Agent / RAG 关键词检测
AI_HINTS=$(grep -rl --include="*.py" --include="*.ts" --include="*.js" --include="*.ipynb" --include="*.mdx" -E "openai|anthropic|langchain|llamaindex|autogen|crewai|chromadb|pinecone|weaviate|embedding|vector_store" . 2>/dev/null | head -3)
if [ -n "$AI_HINTS" ]; then
  FRAMEWORKS+=("ai-stack")
  [ "$TYPE" = "unknown" ] && TYPE="ai"
fi

# CLI 框架检测
if [ -f "package.json" ]; then
  grep -q "\"commander\"\|\"yargs\"\|\"oclif\"\|\"clipanion\"" package.json 2>/dev/null && FRAMEWORKS+=("cli-framework")
fi
if [ -f "go.mod" ]; then
  grep -q "cobra\|urfave/cli" go.mod 2>/dev/null && FRAMEWORKS+=("cli-framework")
fi
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  grep -rql "click\|typer\|argparse" . --include="*.py" 2>/dev/null | head -1 | grep -q . && FRAMEWORKS+=("cli-framework")
fi

# 规模评估
FILE_COUNT=$(find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' -not -path '*/build/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' 2>/dev/null | wc -l | tr -d ' ')
if [ "$FILE_COUNT" -gt 1000 ]; then
  SCALE="large"
elif [ "$FILE_COUNT" -gt 200 ]; then
  SCALE="medium"
fi

# 成熟度信号检测
MATURITY=()
[ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] || [ -f "Jenkinsfile" ] && MATURITY+=("ci-cd")
[ -f "CONTRIBUTING.md" ] || [ -f "CONTRIBUTE.md" ] && MATURITY+=("contributing-guide")
[ -d "docs" ] || [ -d "documentation" ] && MATURITY+=("documentation")
[ -f "CHANGELOG.md" ] || [ -f "CHANGES.md" ] && MATURITY+=("changelog")
ls jest.config* 2>/dev/null | grep -q . || [ -f "pytest.ini" ] || [ -f "pyproject.toml" ] && grep -q "pytest\|tool.pytest" pyproject.toml 2>/dev/null && MATURITY+=("test-framework")
[ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ] && MATURITY+=("test-framework")
[ -f ".codecov.yml" ] || [ -f "codecov.yml" ] || grep -rql "coverage" . --include="*.json" --include="*.toml" 2>/dev/null | head -1 | grep -q . && MATURITY+=("coverage-config")
[ -f "LICENSE" ] || [ -f "LICENSE.md" ] && MATURITY+=("license")

# 默认 type
if [ "$TYPE" = "unknown" ]; then
  if echo "${FRAMEWORKS[@]}" | grep -q "cli-framework"; then
    TYPE="cli"
  elif echo "${LANGUAGES[@]}" | grep -q "rust\|go"; then
    TYPE="cli-or-service"
  elif echo "${LANGUAGES[@]}" | grep -q "python"; then
    TYPE="library-or-script"
  fi
fi

# 输出 JSON
LANG_JSON=$(printf '"%s",' "${LANGUAGES[@]}")
FW_JSON=$(printf '"%s",' "${FRAMEWORKS[@]}")
MAT_JSON=$(printf '"%s",' "${MATURITY[@]}")
LANG_JSON="[${LANG_JSON%,}]"
FW_JSON="[${FW_JSON%,}]"
MAT_JSON="[${MAT_JSON%,}]"

cat <<JSON
{
  "languages": ${LANG_JSON},
  "frameworks": ${FW_JSON},
  "type": "${TYPE}",
  "scale": "${SCALE}",
  "file_count": ${FILE_COUNT},
  "maturity": ${MAT_JSON}
}
JSON
