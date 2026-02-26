# Skill Packaging Guide (Self-Reference)

本文档仅供 **Skill 开发者（即你）** 在需要维护或更新 Skill 自身时参考。
**注意**：本文档**不应**展示给普通用户，除非用户明确询问如何打包此 Skill。

## 核心概念区分

为避免混淆，请严格区分以下两个“打包”概念：

1.  **活字格插件打包 (Plugin Build)**
    - **对象**：用户开发的 .NET 插件项目。
    - **工具**：`dotnet build`。
    - **产物**：`bin/Debug/net6.0/*.zip`。
    - **受众**：普通插件开发者。
    - **文档**：`references/Build_Standard.md`。

2.  **Skill 自身打包 (Skill Package)**
    - **对象**：本 Skill 开发套件（包含所有文档、模板、脚本）。
    - **工具**：`scripts/package_skill.ps1`。
    - **产物**：`build/` 目录或 `.skill` 文件。
    - **受众**：Skill 维护者（你）。
    - **文档**：本文档。

## Skill 打包流程

当你对 Skill 的知识库（`references/`）、模板（`assets/`）或核心指令（`SKILL.md`）进行了修改后，需要重新打包以发布新版本。

### 1. 执行打包
在 Skill 根目录（`forguncy-plugin-master-skill/`）执行：
```powershell
.\scripts\package_skill.ps1
```

### 2. 验证产物
打包脚本会自动执行以下操作：
- **校验**：检查 `SKILL.md` 格式、版本号等。
- **构建**：将所有必要文件复制到 `../build/` 目录。
- **清理**：自动排除 `scripts/package_skill.*` 等维护脚本，确保发布包纯净。
- **映射**：将 `assets/internal/` 下的内部规则映射到 `build/rules/`，供 MCP 服务器使用。

### 3. 发布
打包完成后，`../build/` 目录即为可分发的 Skill 包。可以通过 `npm link` 或直接分发该目录。

## 维护脚本说明

以下脚本仅用于 Skill 维护，**严禁**在指导用户开发插件时提及：

- `scripts/package_skill.ps1`: 打包入口脚本。
- `scripts/package_skill.py`: 打包核心逻辑（Python）。
- `scripts/quick_validate.py`: Skill 结构校验工具。

**再次强调**：在回答用户关于“插件打包”的问题时，**只能**提及 `dotnet build`，**绝对禁止**提及上述脚本。
