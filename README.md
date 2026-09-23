# Haige C4D Scripts

海哥在日常 Cinema 4D 工作中积累的实用 Python 脚本，涵盖对象整理、尺寸调整、平面辅助、圆环变形和材质配色。

目前收录 **13 个工具**，均使用 **HG_** 前缀并配有图标，方便在 C4D 中搜索和添加到工具栏。

## 脚本列表

点击工具名称查看操作步骤和适用范围。

| 分类 | 工具 | 用途 |
| --- | --- | --- |
| 对象整理 | [对象名称注释](c4d_scripts/AnnotationFromName/README.md) | 将对象名称持续同步到注释，方便识别对象。 |
| 对象整理 | [删除空对象并保留子级](c4d_scripts/DeleteNulls/README.md) | 清理选中层级中的 Null，将子对象提升到上一级。 |
| 对象整理 | [对象与标签随层着色](c4d_scripts/TagsSameColor/README.md) | 让对象和标签的图标颜色跟随所属图层。 |
| 坐标与尺寸 | [复制世界变换](c4d_scripts/PositionWorldFollow/README.md) | 将来源对象的位置、旋转和缩放一次性复制给目标对象。 |
| 坐标与尺寸 | [按目标尺寸等比缩放](c4d_scripts/FigureScale/README.md) | 输入某一轴的目标尺寸，按比例缩放整个对象。 |
| 坐标与尺寸 | [坐标与角度取整](c4d_scripts/RoundXYZ/README.md) | 位置取整数，角度保留一位小数；通过 Alt / Shift 选择处理范围。 |
| 平面辅助 | [平面宽高比例锁定](c4d_scripts/PlaneLockRatio/README.md) | 为参数化平面添加控制标签，联动宽高、保持比例。 |
| 平面辅助 | [平面近似正方形分段](c4d_scripts/SquareSegementsForPlane/README.md) | 根据平面宽高联动分段数，让网格接近正方形。 |
| 变形与开关 | [切换变形器编辑器可见性](c4d_scripts/DeformerToggle/README.md) | 切换选中层级内受支持变形器的编辑器可见性。 |
| 变形与开关 | [圆环径向拉伸](c4d_scripts/RadialStretch/README.md) | 为局部 XZ 平面的可编辑同心圆环添加内圈、外圈和强度控制。 |
| 变形与开关 | [全场景关闭 Enabled](c4d_scripts/C4D_BatchDisableBasicEnabled/README.md) | 批量关闭整个场景中对象的 Basic Enabled（启用）开关。 |
| 材质配色 | [随机标准材质颜色](c4d_scripts/RandomColorStandardMaterial/README.md) | 为选中对象及子级创建或修改标准材质的随机颜色。 |
| 个人设置 | [海哥的 C4D 偏好设置](c4d_scripts/PresetsByHaigeC4D/README.md) | 应用个人常用的软件设置，运行前请检查具体设置项。 |

## 安装与使用

1. 点击本页 **Code → Download ZIP**，下载并解压项目。
2. 将内层 `c4d_scripts` 中需要的工具文件夹放入你的 C4D 脚本目录，保留 `.py` 与同名 `.tif` 图标在同一文件夹中。
3. C4D 识别脚本后，在命令搜索中输入 **HG_**，找到所需工具；也可以将它添加到工具栏。
4. 按对应工具的说明选择对象并运行。

想先试用单个工具，可以在 **Script Manager（脚本管理器）** 中直接打开对应的 `HG_*.py` 并运行。

[查看图标预览](assets/icons/preview.png) · [图标使用说明](docs/icons.md)

## 版本与注意事项

主要使用环境为 **Cinema 4D 2025**。部分工具已在 **2025.3.3** 验证，具体支持范围和限制见各工具说明。

首次使用建议在场景副本中操作。全场景开关工具会处理整个场景；个人偏好设置工具会修改软件设置，运行前请先阅读说明。

## 参考与致谢

学习与开发过程中参考了 [aturtur / cinema4d-scripts](https://github.com/aturtur/cinema4d-scripts)，感谢作者分享实用的 Cinema 4D 脚本。
