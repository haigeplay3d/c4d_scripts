# 脚本总表

更新：2026-09-23。以下 13 项为用户已开发成果；编号仅供清单引用，不改文件名。功能依据本地源码整理，已开发不等于本轮完成运行验收。

| 编号 | 分类 | 中文用途 / 使用说明 | 脚本 | 验证状态 |
| --- | --- | --- | --- | --- |
| 001 | 对象与场景 | [对象名称注释](../c4d_scripts/AnnotationFromName/README.md) | `HG_AnnotationFromName.py` | 源码盘点；本轮未运行 |
| 002 | 对象与场景 | [删除空对象并保留子级](../c4d_scripts/DeleteNulls/README.md) | `HG_DeleteNulls.py` | C4D 2025.3.3 批次宿主用例通过 |
| 003 | 对象与场景 | [对象与标签随层着色](../c4d_scripts/TagsSameColor/README.md) | `HG_TagsSameColor.py` | 源码盘点；本轮未运行 |
| 004 | 坐标与尺寸 | [复制世界变换](../c4d_scripts/PositionWorldFollow/README.md) | `HG_PositionWorldFollow.py` | 源码盘点；本轮未运行 |
| 005 | 坐标与尺寸 | [按目标尺寸等比缩放](../c4d_scripts/FigureScale/README.md) | `HG_FigureScale.py` | C4D 2025.3.3 批次宿主用例通过 |
| 006 | 坐标与尺寸 | [坐标与角度取整](../c4d_scripts/RoundXYZ/README.md) | `HG_RoundXYZ.py` | C4D 2025.3.3 批次宿主用例通过 |
| 007 | 平面辅助 | [平面宽高比例锁定](../c4d_scripts/PlaneLockRatio/README.md) | `HG_PlaneLockRatio.py` | 源码盘点；本轮未运行 |
| 008 | 平面辅助 | [平面近似正方形分段](../c4d_scripts/SquareSegementsForPlane/README.md) | `HG_SquareSegementsForPlane.py` | 源码盘点；本轮未运行 |
| 009 | 变形与开关 | [切换变形器编辑器可见性](../c4d_scripts/DeformerToggle/README.md) | `HG_DeformerToggle.py` | 源码盘点；本轮未运行 |
| 010 | 变形与开关 | [圆环径向拉伸](../c4d_scripts/RadialStretch/README.md) | `HG_RadialStretch.py` | 既有 README 记载宿主验证 |
| 011 | 变形与开关 | [全场景关闭 Enabled](../c4d_scripts/C4D_BatchDisableBasicEnabled/README.md) | `HG_C4D_BatchDisableBasicEnabled.py` | 源码盘点；本轮未运行 |
| 012 | 材质 | [随机标准材质颜色](../c4d_scripts/RandomColorStandardMaterial/README.md) | `HG_RandomColorStandardMaterial.py` | 源码盘点；本轮未运行 |
| 013 | 个人设置 | [个人 C4D 偏好设置](../c4d_scripts/PresetsByHaigeC4D/README.md) | `HG_presetsbyhaigec4d.py` | 源码盘点；本轮未运行 |

## 版本范围

13 个已有工具现均纳入版本管理；其中新增纳入的三个工具见 [收录审查](additional-tools-review.md)。纳入 Git 不表示本轮已重新运行全部工具。

## 计数边界

根目录 `c4dpref.py` 含未定义的 `foo`、`prefs`，暂按历史草稿处理，不计入正式工具。该文件保留原位，未执行、未移动。

外部脚本目录可能有其他工具，不纳入本仓库 13 项计数。
