# HG_ 脚本名称迁移

2026-09-23：13 个正式工具入口及配套 TIF 同时加 `HG_` 前缀。目录名、场景内已有标签名、控制标记及运行代码不变。测试脚本、图标生成器和历史草稿不属于正式工具，不加前缀。

| 原文件名 | 新文件名 |
| --- | --- |
| `AnnotationFromName.py` | `HG_AnnotationFromName.py` |
| `C4D_BatchDisableBasicEnabled.py` | `HG_C4D_BatchDisableBasicEnabled.py` |
| `DeformerToggle.py` | `HG_DeformerToggle.py` |
| `DeleteNulls.py` | `HG_DeleteNulls.py` |
| `FigureScale.py` | `HG_FigureScale.py` |
| `PlaneLockRatio.py` | `HG_PlaneLockRatio.py` |
| `PositionWorldFollow.py` | `HG_PositionWorldFollow.py` |
| `presetsbyhaigec4d.py` | `HG_presetsbyhaigec4d.py` |
| `RadialStretch.py` | `HG_RadialStretch.py` |
| `RandomColorStandardMaterial.py` | `HG_RandomColorStandardMaterial.py` |
| `RoundXYZ.py` | `HG_RoundXYZ.py` |
| `SquareSegementsForPlane.py` | `HG_SquareSegementsForPlane.py` |
| `TagsSameColor.py` | `HG_TagsSameColor.py` |

所有 TIF 跟随同名改名。SVG/PNG 源图沿用资产名称，总览显示 HG_ 命令名；生成器输出 HG_ 同名 TIF，manifest 对应新路径。

## C4D 使用与回退

保存当前工作后，必要时重启 C4D 重新发现脚本，再搜索 HG_。已有工具栏按钮和快捷键若关联失效，需要从新脚本重新关联；本次不自动修改用户布局或快捷键。不要把旧名脚本再复制回加载目录，以免重复。

[完整26项映射与原文件哈希](hg-prefix-migration.json) 可用于核对或反向改名；反向改名前先检查旧路径没有新文件，避免覆盖。此前宿主报告保留原路径和原始哈希作为历史证据，没有伪造新版验收。

## 验证范围

本轮核对13个Python入口内容哈希不变、13个同名图标、图标生成器可重建、测试加载新路径、文档相对链接；不宣称C4D新命令发现或工具栏迁移已实测。

原有 TagsSameColor 工作区修改随文件改名完整保留；提交仅移动其已提交版本，不把既有代码差异混入改名提交。

十角色审核：产品=HG_方便查找；项目=仅正式入口；技术=目录不变；C4D=旧快捷入口可能需重绑；开发=源码字节不变；诊断=保留映射和历史验收；QA=新路径测试及图标配对；发布=仅本地提交；文档=当前入口同步；安全=先备份，无旧名覆盖。自审：文件迁移可交付，宿主发现待确认。
