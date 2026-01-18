# 活字格 (Forguncy) 插件开发文档索引

本索引旨在帮助开发者（及 AI 助手）快速定位相关技术文档。

## 1. 核心指南 (Core Guides)

*   **SOP 标准流程**: `docs/SOP.md`
*   **最佳实践**: `docs/SDK_BestPractices.md`
*   **API 速查表**: `docs/API_Cheatsheet.md`

## 2. 插件类型参考 (Plugin Types)

### 2.1 服务端命令 (ServerCommand)
*   **基础结构**: `docs/references/ServerCommand/Basic_Structure.md`
*   **数据库交互**: `docs/references/ServerCommand/Other_Database_Interaction.md`
*   **日志记录**: `docs/references/ServerCommand/Other_ServerCommand_Log.md`
*   **异常处理**: `docs/references/ServerCommand/Process_Exception_Handling.md`
*   **返回结果**: `docs/references/ServerCommand/Process_Return_Results.md`
*   **第三方网络请求**: `docs/references/ServerCommand/Other_ThirdParty_Network.md`

#### 属性定义 (Properties)
*   **字符串**: `docs/references/ServerCommand/Add_Property_String.md`
*   **整数/浮点数**: `docs/references/ServerCommand/Add_Property_Integer.md`, `Add_Property_Double.md`
*   **布尔值**: `docs/references/ServerCommand/Add_Property_Boolean.md`
*   **枚举/下拉框**: `docs/references/ServerCommand/Add_Property_Enum.md`, `Add_Property_Dropdown.md`
*   **公式支持**: `docs/references/ServerCommand/Add_Property_Formula.md`
*   **数据源/连接**: `docs/references/ServerCommand/Add_Property_DataSource.md`, `Add_Property_DatabaseConnection.md`
*   **对象/列表**: `docs/references/ServerCommand/Add_Property_Object.md`, `Add_Property_ObjectList.md`

#### 设计器行为 (Designer)
*   **校验**: `docs/references/ServerCommand/Designer_Validation.md`
*   **动态可见性**: `docs/references/ServerCommand/Designer_Dynamic_Visibility.md`
*   **高级折叠**: `docs/references/ServerCommand/Designer_Advanced_Folding.md`

### 2.2 单元格类型 (CellType)
*   **基础结构**: `docs/references/CellType/Basic_Structure.md`
*   **生命周期**: `docs/references/CellType/Integration_Lifecycle.md`
*   **样式支持**: `docs/references/CellType/Support_Cell_Style.md`
*   **值处理**: `docs/references/CellType/Form_Support_Value.md`, `Form_Support_ValueChange.md`

#### UI 与交互
*   **设计器预览**: `docs/references/CellType/Designer_Preview.md`
*   **列表视图 (ListView)**: `docs/references/CellType/Integration_ListView.md`
*   **图片上传**: `docs/references/CellType/Integration_ImageUpload.md`
*   **右键菜单/操作**: `docs/references/CellType/Action_AdvancedOperations.md`

### 2.3 客户端命令 (ClientCommand)
*   **README**: `docs/references/ClientCommand/README.md`

### 2.4 服务端 API (ServerApi)
*   **README**: `docs/references/ServerApi/README.md`

### 2.5 中间件 (Middleware)
*   **README**: `docs/references/Middleware/README.md`

## 3. 通用功能与特性

*   **属性索引**: `docs/references/ServerCommand/Attribute_Index.md`
*   **搜索支持**: `docs/references/ServerCommand/Attribute_Search.md`
*   **序列化**: `docs/references/ServerCommand/Attribute_Serialization.md`
