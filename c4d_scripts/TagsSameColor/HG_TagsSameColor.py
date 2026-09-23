import c4d
from c4d import documents, plugins

def main():
    # 获取当前对象
    obj = doc.GetActiveObject()

    # 检测当前对象是否存在
    if obj is None:
        return

    # 检测当前对象是否有一个名为 TagsSameColor 的 Python Tag
    tags = obj.GetTags()
    for tag in tags:
        if tag.GetName() == "TagsSameColor" and tag.GetType() == c4d.Tpython:
            return  # 已经有 TagsSameColor 的 Python Tag，不执行任何操作

    # 创建一个新的 Python Tag
    python_tag = obj.MakeTag(c4d.Tpython)
    if python_tag is None:
        return

    # 设置 Python Tag 的名称
    python_tag.SetName("TagsSameColor")

    # 在 Python Tag 的代码容器中输入代码 "x"
    code = """
import c4d

def main():
    # 获取当前Python标签所在的对象
    obj = op.GetObject()

    if obj is not None:
        # 获取对象的层
        layer = obj.GetLayerObject(doc)

        if layer is not None:
            # 获取层的颜色
            layer_color = layer[c4d.ID_LAYER_COLOR]

            # 把对象的Icon Color 模式改为custom
            obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE]=c4d.ID_BASEOBJECT_USECOLOR_AUTOMATIC

            # 把对象的icon color等于层的颜色
            obj[c4d.ID_BASELIST_ICON_COLOR] = layer_color
            obj[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS  # 设置Icon Color模式为custom

            # 遍历所有标签
            tags = obj.GetTags()
            for tag in tags:
                # tag()[1041670] = True 勾选Icon Color
                tag[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = True

                # 把所有标签的icon color等于层的颜色
                tag[c4d.ID_BASELIST_ICON_COLOR] = layer_color

            c4d.EventAdd()
        else:
            print("The object is not assigned to any layer.")
    else:
        print("No object found.")

# 自动执行
main()
"""
    python_tag[c4d.TPYTHON_CODE] = code

    # 更新 Cinema 4D 界面
    c4d.EventAdd()

if __name__ == '__main__':
    main()