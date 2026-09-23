import c4d

def delete_empty_nulls(obj, doc):
    if obj is None:
        return

    # 先递归处理子对象
    child = obj.GetDown()
    while child:
        next_child = child.GetNext()
        delete_empty_nulls(child, doc)
        child = next_child

    # 检查当前对象是否为Null类型
    if obj.GetType() == c4d.Onull:
        # 检查是否有子对象
        if obj.GetDown() is None:
            # 没有子对象，直接删除
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
            obj.Remove()
        else:
            # 有子对象，删除但不包括子对象
            child = obj.GetDown()
            # 保存子对象的全局矩阵
            child_matrices = {}
            while child:
                child_matrices[child] = child.GetMg()
                child = child.GetNext()

            child = obj.GetDown()
            # 将子对象移动到父对象下
            predecessor = obj
            while child:
                next_child = child.GetNext()
                doc.AddUndo(c4d.UNDOTYPE_HIERARCHY_PSR, child)
                child.Remove()
                child.InsertAfter(predecessor)
                # 恢复子对象的全局矩阵
                child.SetMg(child_matrices[child])
                predecessor = child
                child = next_child

            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
            obj.Remove()


def main():
    doc = c4d.documents.GetActiveDocument()
    if doc is None:
        return

    # 获取所选对象
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    # Snapshot topmost selected roots before any removal. A selected descendant
    # is already covered by its selected ancestor, regardless of selection order.
    roots = []
    for obj in selected_objects:
        parent = obj.GetUp()
        while parent is not None and parent not in selected_objects:
            parent = parent.GetUp()
        if parent is None and obj not in roots:
            roots.append(obj)
    if not roots:
        return

    c4d.StopAllThreads()
    doc.StartUndo()
    try:
        for obj in roots:
            delete_empty_nulls(obj, doc)
    finally:
        doc.EndUndo()

    # 更新Cinema 4D界面
    c4d.EventAdd()


if __name__ == "__main__":
    main()
