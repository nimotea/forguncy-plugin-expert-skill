🚀 第一阶段：技能改造与发布
这个阶段的目标是把你的现有技能，改造成符合 npx skills 标准并成功发布。

第1步：项目初始化与结构重组（1小时）
首先，你需要一个符合工具预期的项目结构。npx skills 和社区工具 build-skill 都基于“一个仓库可以包含多个技能”的包管理模式 。

推荐使用 build-skill 快速生成标准模板：

bash
# 在你想创建项目的目录下运行
npx build-skill
按照提示输入你的组织/品牌名、第一个技能的名称和描述。它会自动帮你生成一个功能完备的仓库骨架 。

生成的结构大概是这样 ：

text
你的品牌-skills/
├── .github/workflows/        # 后面会用的自动化CI
├── scripts/                  # 辅助脚本 (添加、同步技能)
├── skills/                   # 核心目录，存放所有技能
│   └── 你的技能名/            # 你的第一个技能
│       ├── SKILL.md           # 技能核心文件 (核心!)
│       └── .claude-plugin/    # (可选) 特定平台的配置
├── README.md                  # 仓库的说明文档
└── LICENSE                    # 开源许可证 (如 MIT)
迁移你的技能：

把你现有的技能内容（描述、步骤、示例等）填充到 skills/你的技能名/SKILL.md 文件中 。

SKILL.md 的核心是开头的 YAML 信息，必须包含 name 和 description 。

markdown
---
name: your-unique-skill-name   # 全局唯一，用连字符
description: >                 # 非常重要！这里要写清楚技能是做什么的，以及在什么场景下触发。
  详细描述你的技能功能，例如："从PDF文件中提取文本和表格数据，当用户询问'分析PDF'、'提取表格'时使用。"
---

# 你的技能名称
这里是具体的指令内容...
第2步：核心文件完善与验证（2小时）
这是最关键的一步，确保你的技能能被正确识别和使用。

撰写 README.md：为你的仓库写一个好的人类可读的文档。说明你的技能包是做什么的，包含哪些技能。更重要的是，在醒目的位置提供一行安装命令给用户 ：

bash
npx skills add 你的GitHub用户名/你的仓库名
选择许可证：在根目录添加 LICENSE 文件（如 MIT），明确你的技能可以如何被使用 。

本地验证：在发布前，先在本地模拟用户安装，确保一切正常。

bash
# 在你的项目根目录上一级执行
npx skills add ./你的品牌-skills --skill 你的技能名 --list   # 先列出看看能否找到
npx skills add ./你的品牌-skills --skill 你的技能名          # 实际安装测试
如果安装成功，说明你的结构和 SKILL.md 都是有效的 。

第3步：发布到GitHub并正式“发布”（30分钟）
npx skills 的“发布”就是让你的代码公开可用。

创建GitHub仓库：在 GitHub 上新建一个仓库，名字最好和你本地的项目文件夹名一致（例如 your-brand-skills）。

推送代码：

bash
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
打好版本标签：由于 npx skills 不支持按语义化版本安装，但为了你自己和用户（他们可以手动切）的方便，强烈建议为每次重要发布创建一个 Git 标签 。

bash
git tag v1.0.0
git push origin v1.0.0
至此，你的技能就算正式发布了！任何用户都可以通过 npx skills add 你的用户名/你的仓库名 来安装