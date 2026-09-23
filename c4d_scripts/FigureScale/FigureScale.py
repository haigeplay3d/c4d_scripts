import c4d
import math

def get_object_size(obj):
    """World lengths of local bounding-box axes, including parent/frozen scale.

    These are not world-axis-aligned bounds or deformed-cache dimensions.
    """
    rad = obj.GetRad()
    matrix = obj.GetMg()
    return (2 * rad.x * matrix.v1.GetLength(),
            2 * rad.y * matrix.v2.GetLength(),
            2 * rad.z * matrix.v3.GetLength())


class FigureScaleDialog(c4d.gui.GeDialog):
    IDC_SOURCE_X = 1000
    IDC_SOURCE_Y = 1001
    IDC_SOURCE_Z = 1002

    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.last_input_value = None
        self.last_input_id = None

    def CreateLayout(self):
        self.SetTitle("FigureScale")

        # 第一行：SourceX 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceX")
        self.AddEditNumberArrows(self.IDC_SOURCE_X, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_X, self.size_x, min=0, step=0.1)

        # 第二行：SourceY 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceY")
        self.AddEditNumberArrows(self.IDC_SOURCE_Y, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_Y, self.size_y, min=0, step=0.1)

        # 第三行：SourceZ 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceZ")
        self.AddEditNumberArrows(self.IDC_SOURCE_Z, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_Z, self.size_z, min=0, step=0.1)

        # 第四行：OK 和 Cancel 按钮
        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)

        return True

    def Command(self, id, msg):
        if id == c4d.DLG_OK:
            if self.last_input_id == self.IDC_SOURCE_X:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_X)
            elif self.last_input_id == self.IDC_SOURCE_Y:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_Y)
            elif self.last_input_id == self.IDC_SOURCE_Z:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_Z)
            else:
                # 如果没有明确的最后输入框，按顺序检查
                if self.IsEnabled(self.IDC_SOURCE_X):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_X)
                elif self.IsEnabled(self.IDC_SOURCE_Y):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_Y)
                elif self.IsEnabled(self.IDC_SOURCE_Z):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_Z)

            self.Close()
        elif id == c4d.DLG_CANCEL:
            self.last_input_value = None
            self.Close()
        elif id in [self.IDC_SOURCE_X, self.IDC_SOURCE_Y, self.IDC_SOURCE_Z]:
            self.last_input_id = id
        return True

def main():
    # 获取当前活动文档
    doc = c4d.documents.GetActiveDocument()

    if doc is None:
        return

    # 获取当前选择的物体列表
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    # 如果没有选择物体，则不执行任何操作
    if not selected_objects:
        return

    # 如果选择了多个物体，提示用户只选择一个物体
    if len(selected_objects) > 1:
        c4d.gui.MessageDialog("请确保只选择一个物体。")
        return

    # 获取选择的物体
    obj = selected_objects[0]

    # 获取物体当前的尺寸
    x, y, z = get_object_size(obj)

    # 创建并打开对话框
    dlg = FigureScaleDialog(x, y, z)
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=200, defaulth=150)

    # 获取最后输入的值
    new_value = dlg.last_input_value

    if new_value is None:
        # 用户没有任何输入，直接返回
        return

    # 判断最后输入的值是否和原来的值相同
    original_value = None
    if dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_X:
        original_value = x
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Y:
        original_value = y
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Z:
        original_value = z

    if original_value is None or new_value == original_value:
        # 没有有效输入或者最后输入的值和原来的值相同，不做操作
        return

    # Only the edited axis is a divisor: a plane can scale by either nonzero axis.
    if not math.isfinite(original_value) or original_value <= 0:
        c4d.gui.MessageDialog("该轴尺寸为零或无效，请选择一个非零尺寸轴。")
        return
    if not math.isfinite(new_value) or new_value <= 0:
        c4d.gui.MessageDialog("目标尺寸必须是大于零的有限数值。")
        return
    ratio = new_value / original_value
    current_scale = obj.GetRelScale()
    new_scale = current_scale * ratio
    if not all(math.isfinite(v) for v in (new_scale.x, new_scale.y, new_scale.z)):
        c4d.gui.MessageDialog("缩放结果超出有效范围，未修改对象。")
        return
    c4d.StopAllThreads()
    doc.StartUndo()
    try:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetRelScale(new_scale)
    finally:
        doc.EndUndo()

    # 更新场景
    c4d.EventAdd()

if __name__ == "__main__":
    main()