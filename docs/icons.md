# 统一脚本图标

2026-09-23：按用户要求将 13 个工具全部改为统一简洁图标。原创几何绘制，无第三方图标素材。

![图标预览](../assets/icons/preview.png)

## 文件位置

- 每个运行脚本旁放置完全同名的 `.tif`，128×128、RGBA、透明背景、无压缩。
- `presetsbyhaigec4d.py` 使用小写同名 `presetsbyhaigec4d.tif`。
- [SVG 与 PNG 源文件目录](../assets/icons) 保存各图标和总览；manifest.json 保存脚本对应关系及 SHA256。
- 蓝灰为主体轮廓，青色表示主要对象，橙色表示动作或关键状态；不在小图标内放长文字。

## C4D 使用

C4D 的用户脚本支持同目录、同名 TIF。若运行中的 Script Manager 尚未显示新图标，可对相应脚本使用 File → Load Icon… 选择同目录 TIF。不要为刷新图标关闭未保存工程。工具栏中的旧按钮是否即时刷新，需要在本机界面确认。

来源：[Maxon 用户脚本图标说明](https://help.maxon.net/c4d/2026/en-us/Content/html/43049.html)、[C4D 2025 Script Manager 的 Load Icon](https://help.maxon.net/c4d/2025/en-us/Content/html/5896.html)。同名 TIF 规则引用的是已核实的 2026 页面，2025 页面确认支持加载位图与 Alpha；本轮未执行 C4D 2025 自动发现实测。

## 重建

使用普通 Python，不在 C4D 中执行生成器：

```powershell
python -m pip install -r tools/requirements-icons.txt
python tools/build_icons.py
```

生成器会覆盖这 13 个已声明的 SVG、PNG、TIF 及预览，不修改 Python 工具源码。绘制采用统一几何描述同时输出 SVG 与栅格。生成器同时更新 manifest 中的对应关系与哈希。

## 验证与回退

已核对 13/13 同名配对、尺寸、透明通道、TIF/PNG 像素一致性，并查看深浅背景的 64px/32px 预览。尚未确认 C4D 内真实显示或刷新情况。

旧版已跟踪图标可从前一个提交提取；本机另有修改前备份，未删除历史记录。此次图标替换是用户明确要求的全套重做；既有 pngforgithub 图片删除、Learn 文件删除及 TagsSameColor.py 修改不混入图标提交。

十角色复审：产品=13个功能可辨识；项目=与脚本收录分开；技术=可重建矢量/栅格；C4D=同名TIF，宿主显示待验收；开发=原有功能不变；诊断=配对与透明度核验；QA=13/13资产检查与视觉预览；发布=本地Git不推送；文档=README预览与说明；安全=旧图标备份、不关闭宿主。自审：文件交付完成，宿主显示状态未宣称通过。
