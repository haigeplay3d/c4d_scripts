import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def prefs(id):
    """获取指定 ID 的偏好设置插件节点"""
    return c4d.plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

def main() -> None:
    # 用户界面
    prefs(465001620)[c4d.PREF_INTERFACE_LANGUAGE] = 1            # 1: 中文
    prefs(465001620)[c4d.PREF_INTERFACE_EXTERNALHELP] = True     # 使用外部浏览器查看帮助
    prefs(465001620)[c4d.PREF_INTERFACE_INSERTAT] = 1  # 插入对象于: 前一个
    prefs(465001620)[c4d.PREF_INTERFACE_PASTEAT] = 1  # 粘贴对象于: 前一个
    # 导航
    prefs(440000091)[c4d.PREF_NAVIGATION_SYNCVIEWS] = True # 同步正交视口: 开启
    # 视窗显示
    prefs(465001625)[c4d.PREF_VIEW_EDGE_POINTS] = True     # 边模式中的点: 开启
    prefs(465001625)[c4d.PREF_VIEW_OUTLINES] = False   # 轮廓: 关闭
    prefs(465001625)[c4d.PREF_VIEW_SEL_BOUNDINGBOXSELECTION] = False # 边界框: 关闭
    # 文件
    prefs(465001626)[c4d.PREF_FILE_ASSETS_LINK] = 1 # 链接资产: 绝对路径.  1:绝对路径.
    prefs(465001626)[c4d.PREF_FILE_RENDER_OVERWRITE_DEFAULT] = 3 # 渲染输出行为: 跳过现有文件（仅染缺失文件）.

    # --- 插件路径设置 ---

    # ----------------------------

    # 单位
    # 拾色器
    prefs(465001627)[c4d.PREF_UNITS_COLORMODE_REMEMBER_LAST_LAYOUT] = True # 记住上一次布局: 开启
    prefs(465001627)[c4d.PREF_UNITS_COLORMODE_HEX] = True # 十六进制颜色: 开启
    prefs(465001627)[c4d.PREF_UNITS_COLORMODE_SWATCHES] = True # 色块: 开启
    prefs(465001627)[c4d.PREF_UNITS_COLORMODE_SWATCHES_SHOWNAMES] = True # 显示组名称: 开启
    # 内存
    prefs(465001628)[c4d.PREF_MEMORY_UNDO] = 100 # 撤销深度: 100
    # 通讯
    prefs(465001629)[c4d.PREF_COMMUNICATION_QUICKSTART_DIALOG] = False # 启动时打开Cinema 4D对话框: 关闭
    prefs(465001629)[c4d.PREF_COMMUNICATION_BUGREPORTS] = False # 允许错误报告: 关闭
    # 材质
    prefs(465001635)[c4d.PREF_MM_DEFAULT_MATERIAL] = 13015 # 默认材质: 标准
    # 资产浏览器
    # c4d.PREF_BROWSER_DOWNLOAD_LOCATION
    # 导入/导出
    prefs(465001638)[c4d.PREF_IMEXPORT_NODESPACE] = 1 # 导入/目标: 标准渲染器

    c4d.EventAdd() # 刷新界面使设置生效

if __name__ == '__main__':
    main()
