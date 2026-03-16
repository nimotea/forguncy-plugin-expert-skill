# 插件构建器路径缓存增强 Spec

## Why
当前 skill 流程要求用户每次提供插件构建器路径（ForguncyPluginCreator.exe），但没有在本地缓存任何用户路径信息。这导致用户每次都需要重新填写路径，即使他们之前已经成功设置过。活字格设计器路径同样需要每次手动提供，缺乏统一的路径管理机制。

## What Changes
- 新增本地 JSON 配置文件 `builder-paths.json`，用于持久化存储用户路径
- 创建路径管理脚本 `manage-builder-paths.ps1`，支持查看、添加、删除、设置默认路径
- 修改 `init_project.ps1` 优先从缓存中读取路径，其次才使用硬编码的常见路径
- 修改 `update_references.ps1` 支持从缓存读取活字格设计器路径
- 缓存文件存储在 skill 目录内，对用户可见且可手动编辑

## Impact
- Affected specs: 插件项目初始化流程、活字格路径更新流程
- Affected code:
  - `scripts/init_project.ps1`
  - `scripts/update_references.ps1`
  - 新增 `scripts/builder-paths.json`
  - 新增 `scripts/manage-builder-paths.ps1`

## ADDED Requirements
### Requirement: 路径缓存存储
系统 SHALL 提供本地 JSON 配置文件存储用户路径信息，文件位于 `scripts/builder-paths.json`。

#### Scenario: 首次使用无缓存
- **WHEN** 用户首次运行 `init_project.ps1`，且缓存文件不存在
- **THEN** 脚本尝试硬编码的常见路径；若仍无法找到，提示用户输入路径并询问是否保存到缓存

#### Scenario: 已有缓存
- **WHEN** 用户运行脚本且缓存文件存在
- **THEN** 脚本优先使用缓存中的路径；若缓存路径无效，则回退到常见路径

### Requirement: 路径管理脚本
系统 SHALL 提供 `manage-builder-paths.ps1` 脚本，用于管理缓存的路径。

#### Scenario: 查看缓存路径
- **WHEN** 用户运行 `manage-builder-paths.ps1 -List`
- **THEN** 显示所有已缓存的路径及默认路径

#### Scenario: 添加新路径
- **WHEN** 用户运行 `manage-builder-paths.ps1 -Add -Path "D:\Forguncy\Builder\ForguncyPluginCreator.exe"`
- **THEN** 将路径添加到缓存文件，并设置为默认路径

#### Scenario: 删除路径
- **WHEN** 用户运行 `manage-builder-paths.ps1 -Remove -Key "builder"`
- **THEN** 从缓存文件中删除指定的路径项

#### Scenario: 设置默认路径
- **WHEN** 用户运行 `manage-builder-paths.ps1 -SetDefault -Key "builder"`
- **THEN** 将指定路径设为默认，后续脚本优先使用该路径

### Requirement: 路径缓存自动验证
系统 SHALL 在使用缓存路径前自动验证路径有效性。

#### Scenario: 缓存路径失效
- **WHEN** 脚本尝试使用缓存路径但路径不存在或文件无效
- **THEN** 警告用户路径无效，提示是否更新为新路径，然后继续尝试其他路径

## MODIFIED Requirements
### Requirement: init_project.ps1 路径查找顺序
**原始行为**：仅按顺序检查硬编码的常见路径列表
**新行为**：优先检查缓存配置 > 硬编码常见路径 > 提示用户输入

#### Scenario: 使用缓存的构建器路径
- **WHEN** 缓存中存在有效的构建器路径
- **THEN** 直接使用缓存路径启动构建器，无需用户干预

### Requirement: update_references.ps1 路径输入
**原始行为**：强制要求通过 `-TargetForguncyPath` 参数传入路径
**新行为**：支持通过 `-UseCachedPath` 参数自动从缓存读取活字格设计器路径

#### Scenario: 使用缓存的设计器路径
- **WHEN** 用户运行 `update_references.ps1 -UseCachedPath`
- **THEN** 自动从缓存读取活字格设计器路径并执行更新

## REMOVED Requirements
无

## Configuration File Format
```json
{
  "version": "1.0",
  "paths": {
    "builder": {
      "path": "D:\\Forguncy\\Builder\\ForguncyPluginCreator.exe",
      "description": "活字格插件构建器",
      "isDefault": true
    },
    "designer": {
      "path": "D:\\Forguncy\\Designer",
      "description": "活字格设计器安装目录",
      "isDefault": true
    }
  },
  "lastUpdated": "2026-03-16T10:00:00Z"
}
```
