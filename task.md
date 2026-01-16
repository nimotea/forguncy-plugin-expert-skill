# Role: AI Engineering Architect
# Task: Scaffold a "Forguncy Plugin Development Skill" Package
# Context: 
I am building a standardized "Skill" for Claude Code/AI Agents to assist developers in creating plugins for "Forguncy" (a low-code platform based on .NET). 
I need you to generate the file structure and content for this Skill package.

# Requirement:
Please generate the code and file content for the following directory structure. 
Ensure the C# code is production-ready, follows .NET standards, and adheres to Forguncy SDK patterns.

## Target Directory Structure:
/forguncy-plugin-skill
├── SKILL.md                  (The instruction manual for the AI)
├── templates/
│   ├── ServerCommand.cs.txt  (C# template for server-side logic)
│   ├── CellType.cs.txt       (C# template for frontend cell registration)
│   └── Plugin.csproj.txt     (Standard .NET Project file)
└── docs/
    ├── SDK_BestPractices.md  (Rules about DataAccess, Logging, etc.)
    └── API_Cheatsheet.md     (Quick reference for IGenerateContext, etc.)

---

## Content Specifications:

### 1. File: SKILL.md
- Define the role as "Forguncy Plugin Expert".
- Define a strict workflow: Analyze Request -> Choose Template -> Apply Logic -> Review against Docs.
- Add specific constraints: 
  - "Always use `ExecutionResult` for returns."
  - "Properties must have `[DisplayName]`."
  - "Do not use `Console.WriteLine`."

### 2. File: templates/ServerCommand.cs.txt
- Create a C# class inheriting from `Command`.
- Include necessary `using` statements (GrapeCity.Forguncy.ServerApi, etc.).
- Add a sample property with `[DisplayName]` and `[FormulaProperty]`.
- Implement a robust `Execute` method with `try-catch`.
- Use `context.EvaluateFormulaAsync` for the property in the template.

### 3. File: templates/Plugin.csproj.txt
- A standard SDK-style project file for .NET 6.0 or .NET Standard 2.0.
- Include placeholders for NuGet package references (`GrapeCity.Forguncy.ServerApi`).

### 4. File: docs/SDK_BestPractices.md
- Explain how to use `IGenerateContext`.
- Explain `context.DataAccess` vs `new SqlConnection` (Forbid the latter).
- Explain how to handle user parameters safely.

### 5. File: docs/API_Cheatsheet.md
- List common methods for `IDataAccess` (GetTableData, ExecuteNonQuery).
- List common methods for `IUserInfo` (Name, Role).

---

# Action:
Please output the content of each file in code blocks so I can copy-paste them directly or run a script to create them.