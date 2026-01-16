# API 速查表 (API Cheatsheet)

## IDataAccess
通过 `context.DataAccess` 访问。

- `ExecuteNonQuery(string sql, object parameters)`: 执行 UPDATE, INSERT, 或 DELETE 语句。
- `ExecuteScalar(string sql, object parameters)`: 返回第一行第一列的值。
- `GetTableData(string tableName)`: 获取指定表的数据。
- `AddTableData(string tableName, Dictionary<string, object> data)`: 向表中插入一行数据。
- `UpdateTableData(string tableName, Dictionary<string, object> data, string whereClause, object parameters)`: 更新数据行。

## IUserInfo
通过 `context.UserInfo` 访问。

- `Name`: 当前用户的用户名。
- `Role`: 分配给当前用户的角色列表。
- `Email`: 当前用户的电子邮件地址。
- `TenantId`: 租户标识符（用于多租户应用）。

## IGenerateContext
- `EvaluateFormulaAsync(object propertyValue)`: 计算属性值，该属性可能包含公式或直接值。
- `Log`: 访问服务器端记录器 (logger)。
