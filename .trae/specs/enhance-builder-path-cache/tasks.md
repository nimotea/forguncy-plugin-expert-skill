# Tasks

## Task 1: 创建路径缓存配置文件模板
- [x] 创建初始的 `scripts/builder-paths.json` 模板文件，包含版本信息和空路径对象
- [x] 定义 JSON 结构：version, paths (builder/designer), lastUpdated
- [x] 放置在 `scripts/builder-paths.json`

## Task 2: 创建路径管理脚本 manage-builder-paths.ps1
- [x] 实现 `-List` 参数：读取并格式化显示缓存的路径
- [x] 实现 `-Add` 参数：添加新路径到缓存，支持指定类型 (builder/designer) 和描述
- [x] 实现 `-Remove` 参数：从缓存中删除指定路径项
- [x] 实现 `-SetDefault` 参数：设置默认路径
- [x] 实现 `-Clear` 参数：清空所有缓存
- [x] 添加输入验证：检查路径是否存在、文件格式是否正确
- [x] 脚本放置在 `scripts/manage-builder-paths.ps1`

## Task 3: 修改 init_project.ps1 集成缓存读取
- [x] 在脚本开头添加读取缓存的函数 `Get-CachedBuilderPath`
- [x] 修改路径查找逻辑：缓存路径 > 硬编码常见路径
- [x] 当使用用户输入的路径时，提示是否保存到缓存
- [x] 支持 `-SkipCache` 参数强制跳过缓存
- [x] 保留原有参数 `-BuilderPath` 优先级最高

## Task 4: 修改 update_references.ps1 支持缓存读取
- [x] 添加 `-UseCachedPath` 参数支持
- [x] 添加读取缓存的函数 `Get-CachedDesignerPath`
- [x] 当使用 `-UseCachedPath` 时自动从缓存读取设计器路径
- [x] 如果缓存路径无效，给出明确错误提示

## Task 5: 更新 SKILL.md 文档
- [x] 在辅助工具部分添加 `manage-builder-paths.ps1` 说明
- [x] 更新 `init_project.ps1` 说明，提及缓存机制
- [x] 添加路径缓存最佳实践说明

# Task Dependencies
- [Task 1] 是基础，优先完成
- [Task 2] 依赖 [Task 1] 定义的 JSON 结构
- [Task 3] 依赖 [Task 1] 和 [Task 2]
- [Task 4] 依赖 [Task 1] 和 [Task 2]
- [Task 5] 依赖 [Task 3] 和 [Task 4] 的功能实现

# Parallel Work
- Task 1 和 Task 2 可以并行开发
- Task 3 和 Task 4 在 Task 2 完成后可并行开发
