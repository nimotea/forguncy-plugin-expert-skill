# 活字格插件专家 (Forguncy Plugin Expert) 技能维护与发布流程

本文档详细说明了如何管理、打包和发布 `forguncy-plugin-expert` 技能。此工作流专为本仓库 (`Funguncy-Plugin-Builder`) 设计，确保技能及其依赖的知识库能够被正确打包并分发给最终用户。

## 1. 目录结构

本仓库采用了多技能管理的结构，核心逻辑与资源分离，以支持更灵活的维护。

```text
src/skills/forguncy-plugin-expert/
├── SKILL.md           # 技能核心定义文件 (Prompt, Actions)
├── package.json       # 技能依赖与版本定义
├── assets/            # 静态资源
│   ├── internal/      # 内部维护文档 (如 IDE 规则)
│   ├── templates/     # 代码生成模板
│   └── schemas/       # 数据校验 Schema
└── references/        # 知识库文档 (Markdown)
    ├── CellType/      # 单元格插件相关文档
    ├── ServerCommand/ # 服务端命令相关文档
    └── ...
```

## 2. 技能管理

### 编辑技能
所有技能的指令和逻辑都在 `src/skills/forguncy-plugin-expert/SKILL.md` 中定义。
- **元数据**：文件头部的 YAML Front Matter 定义了技能名称、描述。
- **指令**：`#` 标题定义的各个功能模块。

### 知识库维护
技能引用的知识库位于 `references/` 目录下。
- **新增文档**：添加新文档后，请确保在 `SKILL.md` 中有相应的引用，或更新索引文件。
- **引用规则**：在 `SKILL.md` 中引用文件时，请使用相对路径。打包脚本会自动处理这些路径。

## 3. 打包技能

为了让 `npx skills` 能够正确识别和加载技能，我们需要将源码打包成标准的分布格式。我们提供了一个 PowerShell 脚本来自动化此过程。

### 运行打包脚本

在项目根目录下，运行以下命令：

```powershell
.\scripts\package_skill.ps1
```

或者指定技能名称（默认为 `forguncy-plugin-expert`）：

```powershell
.\scripts\package_skill.ps1 -SkillName forguncy-plugin-expert
```

### 打包产物
脚本会将技能打包到项目根目录下的 `build/` 文件夹中。构建过程会自动执行以下操作：
1. **结构标准化**：生成 `skills/forguncy-plugin-expert/` 目录结构。
2. **元数据生成**：自动生成用于发布的 `package.json` 和 `README.md`。
3. **IDE 规则注入**：将 `assets/internal/forguncy-plugin-skill-apply.md` 自动转换为 Trae (`.trae/rules`) 和 Cursor (`.cursor/rules`) 的规则文件，确保用户安装后能直接获得最佳体验。
4. **脚本分发**：自动复制辅助脚本（如 `init_project.ps1`）到分发包中。

## 4. 本地验证

在发布之前，必须在本地验证打包后的技能是否能被 `npx skills` 正确加载。

### 安装本地构建包

使用 `npx skills` 从 `build` 目录安装：

```bash
# 1. 检查技能是否能被识别
npx skills add ./build --skill forguncy-plugin-expert --list

# 2. 实际安装/更新
npx skills add ./build --skill forguncy-plugin-expert
```

### 测试运行
安装完成后，在你的 AI 客户端或命令行中测试技能指令，确保：
- 能够触发技能（如 "创建一个活字格插件"）。
- 能够正确读取引用的文档（知识库）。
- 生成的代码模板正确。

## 5. 发布流程

当本地验证通过后，可以将更改推送到 GitHub。

1. **提交更改**：确保所有源码（`src/`）和脚本（`scripts/`）的更改都已提交。
2. **版本控制**：建议在 `package.json` 中更新版本号。
3. **推送到远程**：
   ```bash
   git push origin main
   ```
4. **用户安装**：
   用户可以通过 GitHub 直接安装最新版本的技能：
   ```bash
   npx skills add <你的GitHub用户名>/Funguncy-Plugin-Builder --skill forguncy-plugin-expert
   ```
   *(注：请将 `<你的GitHub用户名>` 替换为实际的 GitHub 用户名)*

## 6. 常见问题

- **打包失败**：请检查 Python 环境是否安装，以及 `src/skills/` 下是否存在对应的技能目录。
- **路径错误**：如果验证时提示找不到文件，请检查 `SKILL.md` 中的相对路径引用是否正确。
- **IDE 规则未生效**：确保 `assets/internal/forguncy-plugin-skill-apply.md` 存在且内容正确。
