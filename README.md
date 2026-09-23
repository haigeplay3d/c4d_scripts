# Haige C4D Scripts

面向日常 Cinema 4D 工作流的个人 Python 脚本集。当前版本纳入 10 个工具；本地另有 3 个已有工具待单独纳入。长期目标是围绕实际制作需求逐步完善到 100 个。

## 从这里开始

- [脚本总表：中文功能、分类与使用说明](docs/script-catalog.md)
- [安装与运行](docs/installation.md)
- [100 个脚本开发路线](docs/roadmap.md)
- [待复查问题与验收清单](docs/quality-backlog.md)
- [维护与接手](docs/maintenance.md)
- [本轮整理记录](docs/organization-2026-09-23.md)
- [第一批修复与宿主验收](docs/batch1-hardening.md)
- [阶段提交范围](docs/batch1-commit-scope.md)

## 项目结构

```text
c4d_scripts/       每个工具一个目录，保留现有名称与位置
  工具名称/        Python 脚本、使用说明及必要配套资源
docs/             总表、安装、路线和维护记录
pngforgithub/      项目展示图片
c4dpref.py         历史设置草稿，不作为正式工具入口
```

脚本源码是功能事实源；总表是查找入口；每个脚本的 README 记录具体用法和限制。当前整理以 C4D 2025 为基线，不能据此推断所有脚本兼容所有版本。

## 项目与参考

- 本项目：[haigeplay3d/c4d_scripts](https://github.com/haigeplay3d/c4d_scripts)
- 参考项目：[aturtur/cinema4d-scripts](https://github.com/aturtur/cinema4d-scripts)

参考项目用于学习组织与实现思路；引用外部代码时单独核对许可并保留来源。本轮没有复制参考仓库代码，也没有替项目选择新的许可证。
