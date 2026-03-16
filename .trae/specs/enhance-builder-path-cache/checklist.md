# Checklist

## Configuration Files
- [x] builder-paths.json 模板文件已创建在 scripts/ 目录
- [x] JSON 结构符合 spec.md 中定义的格式（version, paths, lastUpdated）
- [x] JSON 文件可被 PowerShell 正确解析

## Path Management Script (manage-builder-paths.ps1)
- [x] -List 参数正确显示所有缓存路径
- [x] -Add 参数正确添加新路径并保存到 JSON
- [x] -Remove 参数正确删除指定路径
- [x] -SetDefault 参数正确设置默认路径
- [x] -Clear 参数正确清空所有缓存
- [x] 输入验证正确处理无效路径

## init_project.ps1 Integration
- [x] 脚本优先读取缓存路径
- [x] 缓存路径无效时正确回退到常见路径
- [x] 用户输入新路径时提示是否保存
- [x] -SkipCache 参数正常工作
- [x] 原有的 -BuilderPath 参数优先级保持最高

## update_references.ps1 Integration
- [x] -UseCachedPath 参数正常工作
- [x] 从缓存读取的路径正确传递给内部函数
- [x] 缓存路径无效时给出明确错误提示

## Documentation (SKILL.md)
- [x] 已添加 manage-builder-paths.ps1 说明
- [x] 已更新 init_project.ps1 缓存机制说明
- [x] 已添加路径缓存最佳实践说明

## Integration Testing
- [ ] 完整流程测试：从添加路径到使用路径启动构建器
- [ ] 缓存失效场景测试：路径不存在时的降级行为
- [ ] 多路径管理测试：添加、删除、设置默认的完整流程
