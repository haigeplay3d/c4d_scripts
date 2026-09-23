# -*- coding: utf-8 -*-
"""RadialStretch 1.0 — 一键添加圆环径向拉伸。

选中一个可编辑的 XZ 平面圆环运行。创建原生 Formula 及自包含 Python
控制标签；不修改原始点，支持撤销。详细用法见同目录 README.md。
"""
import c4d

VERSION = "1.0"
MARKER = "Haige.RadialStretch.1"
BC_MARKER = 1059301
BC_INNER = 1059302
BC_OUTER = 1059303
BC_CENTER_X = 1059304
BC_CENTER_Z = 1059305
UD_INNER = 2
UD_OUTER = 3
UD_STRENGTH = 4
UD_RADIUS_INNER = 6
UD_RADIUS_OUTER = 7
UD_REBIND = 8
UD_STATUS = 9

# The same code is embedded in the tag and used by this installer.
# It has no imports from this file, filesystem access or scene-graph mutations.
_RUNTIME = r'''
import c4d
import math

def put(node, key, value):
    if node[key] != value:
        node[key] = value

def measure_source(source):
    if source is None or not source.CheckType(c4d.Opolygon):
        raise ValueError("请选择一个可编辑多边形圆环；参数对象请先转为可编辑对象。")
    points = source.GetAllPoints()
    if len(points) < 12:
        raise ValueError("点数不足，无法测量完整圆环。")
    if any(not all(math.isfinite(v) for v in (p.x,p.y,p.z)) for p in points):
        raise ValueError("模型含无效点坐标。")
    xmin,xmax = min(p.x for p in points),max(p.x for p in points)
    zmin,zmax = min(p.z for p in points),max(p.z for p in points)
    dx,dz = xmax-xmin,zmax-zmin
    if min(dx,dz) <= 1e-8 or abs(dx-dz)/max(dx,dz) > 0.05:
        raise ValueError("当前仅支持对象局部 XZ 平面的完整同心圆环。请检查模型方向或椭圆缩放。")
    cx,cz = (xmin+xmax)*0.5,(zmin+zmax)*0.5
    radii = [math.hypot(p.x-cx,p.z-cz) for p in points]
    ri,ro = min(radii),max(radii)
    if ri <= max(ro*1e-6,1e-8) or ro-ri <= max(ro*1e-6,1e-8):
        raise ValueError("未检测到有效内孔或圆环宽度。")
    sectors = {int((math.atan2(p.z-cz,p.x-cx)+math.pi)/(2*math.pi)*12)%12 for p in points}
    if len(sectors) != 12:
        raise ValueError("当前仅支持完整圆环，不支持扇形或局部弧段。")
    return ri,ro,cx,cz

def write_baseline(tag, values):
    ri,ro,cx,cz = values
    tag[BC_INNER],tag[BC_OUTER] = ri,ro
    tag[BC_CENTER_X],tag[BC_CENTER_Z] = cx,cz
    tag[c4d.ID_USERDATA,UD_RADIUS_INNER] = "%.3f cm" % ri
    tag[c4d.ID_USERDATA,UD_RADIUS_OUTER] = "%.3f cm" % ro

def update_controller(tag):
    deform = tag.GetObject()
    if deform is None or not deform.CheckType(c4d.Oformula):
        return
    ri,ro = tag[BC_INNER],tag[BC_OUTER]
    di = tag[c4d.ID_USERDATA,UD_INNER]
    do = tag[c4d.ID_USERDATA,UD_OUTER]
    strength = tag[c4d.ID_USERDATA,UD_STRENGTH]
    if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in (ri,ro,di,do,strength)):
        put(deform,c4d.FORMULAOBJECT_DLT,"0")
        put(tag,(c4d.ID_USERDATA,UD_STATUS),"参数无效，请重新添加控制器。")
        return
    strength = max(0.0,min(1.0,strength))
    inner,outer = ri+di*strength,ro+do*strength
    if ri <= 0 or ro <= ri or inner <= 1e-8 or outer-inner <= 1e-8:
        expression = "0"
        status = "范围无效：内半径须大于0，外半径须大于内半径。已恢复原形。"
    else:
        # Formula uses normalized coordinates: Size 200 means 1 = 100 cm.
        # repr preserves the measured baseline; the UI displays only 3 decimals.
        expression = "({s})*(({di})+(({do})-({di}))*(100*sqrt(x*x+z*z)-({ri}))/(({ro})-({ri})))/100".format(
            s=repr(strength),di=repr(di),do=repr(do),ri=repr(ri),ro=repr(ro))
        status = "目标内径 %.3f / 外径 %.3f cm（局部尺寸）" % (inner*2,outer*2)
    put(deform,c4d.FORMULAOBJECT_SIZE,c4d.Vector(200))
    put(deform,c4d.FORMULAOBJECT_EFFECT,c4d.FOEFFECT_CYLINDRICAL)
    put(deform,c4d.FORMULAOBJECT_DLT,expression)
    put(tag,(c4d.ID_USERDATA,UD_STATUS),status)

def rebind(tag, undo=True):
    deform = tag.GetObject()
    if deform is None or not deform.CheckType(c4d.Oformula):
        raise ValueError("控制标签需要保留在径向拉伸公式变形器上。")
    values = measure_source(deform.GetUp())
    document = tag.GetDocument()
    if undo and document:
        document.StartUndo()
        document.AddUndo(c4d.UNDOTYPE_CHANGE,tag)
        document.AddUndo(c4d.UNDOTYPE_CHANGE,deform)
    try:
        write_baseline(tag,values)
        deform.SetRelPos(c4d.Vector(values[2],0,values[3]))
        deform.SetRelRot(c4d.Vector())
        deform.SetRelScale(c4d.Vector(1))
        update_controller(tag)
    finally:
        if undo and document:
            document.EndUndo()

def main():
    update_controller(op)

def message(msg_type, data):
    # Some C4D versions deliver description commands through a notification.
    if msg_type == c4d.MSG_NOTIFY_EVENT and isinstance(data,dict):
        event = data.get("event_data",{})
        msg_type,data = event.get("msg_id"),event.get("msg_data")
    if msg_type != c4d.MSG_DESCRIPTION_COMMAND or not isinstance(data,dict):
        return True
    desc = data.get("id")
    if not isinstance(desc,c4d.DescID) or desc.GetDepth()<2:
        return True
    if desc[0].id != c4d.ID_USERDATA or desc[1].id != UD_REBIND:
        return True
    if not c4d.threading.GeIsMainThreadAndNoDrawThread():
        return True
    try:
        rebind(op)
    except ValueError as error:
        c4d.gui.MessageDialog(str(error))
    c4d.EventAdd()
    return True
'''

_NAMES = ("BC_MARKER","BC_INNER","BC_OUTER","BC_CENTER_X","BC_CENTER_Z",
          "UD_INNER","UD_OUTER","UD_STRENGTH","UD_RADIUS_INNER",
          "UD_RADIUS_OUTER","UD_REBIND","UD_STATUS")
CONTROLLER_CODE = "# RadialStretch embedded controller 1.0\n" + "\n".join(
    "%s = %r" % (name,globals()[name]) for name in _NAMES) + "\n" + _RUNTIME
_runtime = {}
exec(compile(CONTROLLER_CODE,"RadialStretch controller","exec"),_runtime)

def find_rig(source):
    for child in source.GetChildren():
        if child.CheckType(c4d.Oformula):
            for tag in child.GetTags():
                if tag.CheckType(c4d.Tpython) and tag[BC_MARKER] == MARKER:
                    return child,tag
    return None,None

def _add_data(tag,dtype,name,group=None,default=None,**options):
    bc = c4d.GetCustomDataTypeDefault(dtype)
    bc[c4d.DESC_NAME] = name
    if group is not None:
        bc[c4d.DESC_PARENTGROUP] = group
    for key,value in options.items():
        bc[getattr(c4d,key)] = value
    desc = tag.AddUserData(bc)
    if default is not None:
        tag[desc] = default
    return desc

def _add_controls(tag,ri,ro):
    group = _add_data(tag,c4d.DTYPE_GROUP,"径向拉伸",DESC_TITLEBAR=True,DESC_DEFAULT=True)
    span = max(ro-ri,1.0)
    for name in ("内圈偏移","外圈偏移"):
        _add_data(tag,c4d.DTYPE_REAL,name,group,0.0,
                  DESC_CUSTOMGUI=c4d.CUSTOMGUI_REALSLIDER,
                  DESC_UNIT=c4d.DESC_UNIT_METER,DESC_STEP=0.1,
                  DESC_MIN=-1e10,DESC_MAX=1e10,
                  DESC_MINSLIDER=-span,DESC_MAXSLIDER=span)
    _add_data(tag,c4d.DTYPE_REAL,"整体强度",group,1.0,
              DESC_CUSTOMGUI=c4d.CUSTOMGUI_REALSLIDER,
              DESC_UNIT=c4d.DESC_UNIT_PERCENT,DESC_MIN=0.0,DESC_MAX=1.0,
              DESC_MINSLIDER=0.0,DESC_MAXSLIDER=1.0,DESC_STEP=0.01)
    baseline = _add_data(tag,c4d.DTYPE_GROUP,"原始尺寸",DESC_TITLEBAR=True,DESC_DEFAULT=True)
    for name in ("原始内半径","原始外半径"):
        _add_data(tag,c4d.DTYPE_STRING,name,baseline,"",
                  DESC_CUSTOMGUI=c4d.CUSTOMGUI_STATICTEXT,DESC_ANIMATE=c4d.DESC_ANIMATE_OFF)
    button = _add_data(tag,c4d.DTYPE_BUTTON,"重新读取原始半径",baseline,
                       DESC_CUSTOMGUI=c4d.CUSTOMGUI_BUTTON,
                       DESC_ANIMATE=c4d.DESC_ANIMATE_OFF)
    assert button[1].id == UD_REBIND
    _add_data(tag,c4d.DTYPE_STRING,"状态",baseline,"",
              DESC_CUSTOMGUI=c4d.CUSTOMGUI_STATICTEXT,DESC_ANIMATE=c4d.DESC_ANIMATE_OFF)
    _add_data(tag,c4d.DTYPE_STRING,"用法",baseline,"正数向外，负数向内；偏移0即固定该圈。",
              DESC_CUSTOMGUI=c4d.CUSTOMGUI_STATICTEXT,DESC_ANIMATE=c4d.DESC_ANIMATE_OFF)

def create_rig(document,source):
    """Return (native Formula, embedded controller tag, was_created)."""
    ri,ro,cx,cz = _runtime["measure_source"](source)
    existing,controller = find_rig(source)
    if existing is not None:
        return existing,controller,False
    for child in source.GetChildren():
        if child.GetInfo() & c4d.OBJECT_MODIFIER and child[c4d.ID_BASEOBJECT_GENERATOR_FLAG]:
            raise ValueError("此对象已有启用的变形器。请先在原始模型副本上添加径向拉伸，避免叠加变形。")
    deform = c4d.BaseObject(c4d.Oformula)
    deform.SetName("径向拉伸")
    deform.SetRelPos(c4d.Vector(cx,0,cz))
    tag = c4d.BaseTag(c4d.Tpython)
    tag.SetName("径向拉伸控制")
    tag[BC_MARKER] = MARKER
    _add_controls(tag,ri,ro)
    _runtime["write_baseline"](tag,(ri,ro,cx,cz))
    tag[c4d.TPYTHON_CODE] = CONTROLLER_CODE
    priority = c4d.PriorityData()
    priority.SetPriorityValue(c4d.PRIORITYVALUE_MODE,c4d.CYCLE_EXPRESSION)
    priority.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY,0)
    tag[c4d.EXPRESSION_PRIORITY] = priority
    deform.InsertTag(tag)
    _runtime["update_controller"](tag)
    document.StartUndo()
    try:
        deform.InsertUnder(source)
        document.AddUndo(c4d.UNDOTYPE_NEWOBJ,deform)
    finally:
        document.EndUndo()
    return deform,tag,True

def main():
    document = c4d.documents.GetActiveDocument()
    if document is None:
        return
    selected_tag = document.GetActiveTag()
    if selected_tag and selected_tag.CheckType(c4d.Tpython) and selected_tag[BC_MARKER] == MARKER:
        document.SetActiveTag(selected_tag,c4d.SELECTION_NEW)
        c4d.EventAdd()
        return
    selected = document.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if len(selected) != 1:
        c4d.gui.MessageDialog("请只选择一个可编辑的圆环模型，然后运行径向拉伸。")
        return
    source = selected[0]
    if source.CheckType(c4d.Oformula):
        for tag in source.GetTags():
            if tag.CheckType(c4d.Tpython) and tag[BC_MARKER] == MARKER:
                document.SetActiveTag(tag,c4d.SELECTION_NEW)
                c4d.EventAdd()
                return
    try:
        c4d.StopAllThreads()
        deform,tag,created = create_rig(document,source)
    except ValueError as error:
        c4d.gui.MessageDialog(str(error))
        return
    document.SetActiveTag(tag,c4d.SELECTION_NEW)
    c4d.EventAdd()

if __name__ == "__main__":
    main()
