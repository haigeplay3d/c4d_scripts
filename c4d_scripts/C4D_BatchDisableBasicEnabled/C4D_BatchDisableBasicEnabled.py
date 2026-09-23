import c4d
from c4d import documents, gui

def get_all_objects(op, lst):
    """递归遍历获取文档中所有物体（包括子级）"""
    while op:
        lst.append(op)
        get_all_objects(op.GetDown(), lst)
        op = op.GetNext()
    return lst

def main():
    doc = documents.GetActiveDocument()
    if not doc:
        gui.MessageDialog("未找到活动文档，请打开一个 .c4d 文件后重试。")
        return

    # 收集所有物体
    all_objects = []
    get_all_objects(doc.GetFirstObject(), all_objects)

    # 开启 Undo 支持
    doc.StartUndo()
    closed_count = 0

    for obj in all_objects:
        # 检查并关闭 Basic 属性下的 Enabled 开关 (c4d.ID_BASEOBJECT_GENERATOR_FLAG)
        if obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG]:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False
            closed_count += 1

    doc.EndUndo()

    # 刷新视图并提示
    c4d.EventAdd()
    gui.MessageDialog(f"✅ 操作完成！已成功关闭 {closed_count} 个物体的 Basic Enabled 开关。\n\n支持 Ctrl+Z 撤销。")
    print(f"[SOP日志] 已关闭 {closed_count} 个物体的 Enabled 开关")

if __name__ == '__main__':
    main()