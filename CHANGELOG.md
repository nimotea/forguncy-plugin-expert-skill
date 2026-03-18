# 变更日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [v1.1.0] - 2026-03-18

### 新增
- 增加缓存机制，避免每次都需要告诉 AI 设计器默认路径
- 缓存文件位于 `.forguncy-path-cache.json`
- 路径验证支持检查子目录 `WebSite\designerBin\Forguncy.exe`

### 变更
- 移除对活字格构建器的依赖，使用 dotnet 命令行工具
- 优化 AI 引导，自动检测开发环境
- 更新 CLI 参考文档，详细说明路径验证逻辑

### 移除
- 移除技能描述中的冗长内容，保持简洁专注
