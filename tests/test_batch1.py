"""Logic regressions using a minimal C4D boundary double, NOT host acceptance.

Run: python -B -m unittest discover -s tests -v
"""
import math
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __mul__(self, n):
        return Vector(self.x*n, self.y*n, self.z*n)

    def GetLength(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)


class Obj:
    def __init__(self, name='obj', kind=1, parent=None):
        self.name, self.kind, self.parent = name, kind, parent
        self.children = []
        if parent:
            parent.children.append(self)
        self.rad = Vector(5, 10, 15)
        self.scale = Vector(1, 1, 1)
        self.pos = Vector(1.2, 2.6, -3.1)
        self.rot = Vector(*(math.radians(v) for v in (10.26, 20.24, -30.26)))
        self.mg = types.SimpleNamespace(v1=Vector(1,0,0), v2=Vector(0,1,0), v3=Vector(0,0,1))
    def GetRad(self): return self.rad
    def GetMg(self): return self.mg
    def SetMg(self, m): self.mg = m
    def GetRelScale(self): return self.scale
    def SetRelScale(self, s): self.scale = s
    def GetAbsPos(self): return self.pos
    def SetAbsPos(self, p): self.pos = p
    def GetAbsRot(self): return self.rot
    def SetAbsRot(self, p): self.rot = p
    def GetType(self): return self.kind
    def GetUp(self): return self.parent
    def GetChildren(self): return list(self.children)
    def GetDown(self): return self.children[0] if self.children else None
    def GetNext(self):
        if not self.parent: return None
        siblings = self.parent.children
        i = siblings.index(self)+1
        return siblings[i] if i < len(siblings) else None
    def Remove(self):
        if self.parent: self.parent.children.remove(self)
        self.parent = None
    def InsertAfter(self, other):
        self.Remove()
        self.parent = other.parent
        self.parent.children.insert(self.parent.children.index(other)+1, self)


class Doc:
    def __init__(self, selected):
        self.selected, self.events = selected, []
    def GetActiveObjects(self, flags): return self.selected
    def StartUndo(self): self.events.append('start')
    def EndUndo(self): self.events.append('end')
    def AddUndo(self, kind, obj): self.events.append((kind, obj.name))


def load(name, doc, keys=0, input_ok=True):
    c = types.ModuleType('c4d')
    for i, k in enumerate(('GETACTIVEOBJECTFLAGS_0','GETACTIVEOBJECTFLAGS_CHILDREN',
                         'GETACTIVEOBJECTFLAGS_SELECTIONORDER','UNDOTYPE_CHANGE',
                         'UNDOTYPE_DELETE','UNDOTYPE_HIERARCHY_PSR','BFM_INPUT_KEYBOARD',
                         'BFM_INPUT_CHANNEL','BFM_INPUT_QUALIFIER','DLG_TYPE_MODAL')):
        setattr(c, k, i+10)
    c.UNDOTYPE_DELETEOBJ = c.UNDOTYPE_DELETE
    c.Onull, c.QALT, c.QSHIFT = 0, 1, 2
    c.Vector, c.BaseContainer = Vector, dict
    c.EventAdd = c.StopAllThreads = lambda: None
    def get_input(a,b,bc):
        bc[c.BFM_INPUT_QUALIFIER] = keys
        return input_ok
    c.gui = types.SimpleNamespace(GeDialog=object, MessageDialog=lambda s: None, GetInputState=get_input)
    c.documents = types.SimpleNamespace(GetActiveDocument=lambda: doc)
    sys.modules['c4d'] = c
    ns = {'__name__':'test_subject','doc':doc}
    p=ROOT/'c4d_scripts'/name/(name+'.py')
    exec(compile(p.read_text(encoding='utf-8-sig'),str(p),'exec'),ns)
    return ns, c


class Regressions(unittest.TestCase):
    def figure(self, obj, axis=1000, target=20):
        d=Doc([obj]); ns,c=load('FigureScale',d)
        base=ns['FigureScaleDialog']
        class Dialog:
            IDC_SOURCE_X, IDC_SOURCE_Y, IDC_SOURCE_Z = 1000,1001,1002
            def __init__(self,*args): self.last_input_id, self.last_input_value = axis,target
            def Open(self,*args,**kwargs): pass
        ns['FigureScaleDialog']=Dialog
        ns['main']()
        return d

    def test_figure_plane_nonzero_axis_scales_without_dividing_zero(self):
        o=Obj();o.rad=Vector(5,0,10)
        d=self.figure(o)
        self.assertEqual((o.scale.x,o.scale.y,o.scale.z),(2,2,2))
        self.assertEqual((d.events[0],d.events[-1]),('start','end'))

    def test_figure_uses_existing_world_axis_scale(self):
        o=Obj();o.scale=Vector(2,3,4)
        o.mg.v1=Vector(6,0,0)  # parent X scale 3, object X scale 2
        self.figure(o,target=120)
        self.assertEqual((o.scale.x,o.scale.y,o.scale.z),(4,6,8))

    def test_figure_zero_source_rejected(self):
        o=Obj();o.rad=Vector(0,1,1)
        d=self.figure(o)
        self.assertEqual(o.scale.x,1)
        self.assertEqual(d.events,[])

    def test_figure_bad_targets_rejected(self):
        for value in (0,-1,float('nan'),float('inf')):
            o=Obj();d=self.figure(o,target=value)
            self.assertEqual(o.scale.x,1)
            self.assertEqual(d.events,[])

    def test_figure_cancel_and_unchanged_do_not_open_undo(self):
        for target in (None,10):
            o=Obj();d=self.figure(o,target=target)
            self.assertEqual(o.scale.x,1)
            self.assertEqual(d.events,[])

    def test_figure_preserves_mirror_scale(self):
        o=Obj();o.scale=Vector(-2,1,1);o.mg.v1=Vector(-2,0,0)
        self.figure(o,target=40)
        self.assertEqual((o.scale.x,o.scale.y,o.scale.z),(-4,2,2))

    def test_round_input_failure_defaults_to_position(self):
        o=Obj();d=Doc([o]);ns,c=load('RoundXYZ',d,input_ok=False)
        ns['main']()
        self.assertEqual((o.pos.x,o.pos.y,o.pos.z),(1,3,-3))

    def test_round_modes(self):
        for keys in (0,1,2,3):
            o=Obj();d=Doc([o]);ns,c=load('RoundXYZ',d,keys)
            ns['main']()
            self.assertAlmostEqual(o.pos.x,1.2 if keys==1 else 1)
            self.assertAlmostEqual(math.degrees(o.rot.x),10.26 if keys==0 else 10.3)
            self.assertEqual((d.events[0],d.events[-1]),('start','end'))

    def test_round_exception_still_closes_undo(self):
        o=Obj();d=Doc([o]);ns,c=load('RoundXYZ',d)
        def fail(value): raise RuntimeError('injected write failure')
        o.SetAbsPos=fail
        with self.assertRaises(RuntimeError): ns['main']()
        self.assertEqual(d.events[-1],'end')

    def test_empty_selection_does_not_modify_document(self):
        for name in ('FigureScale','RoundXYZ','DeleteNulls'):
            d=Doc([]);ns,c=load(name,d);ns['main']()
            self.assertEqual(d.events,[])

    def test_delete_preserves_order_and_world_matrices(self):
        root=Obj('root');n=Obj('null',0,root)
        children=[Obj(x,1,n) for x in ('a','b','c')]
        matrices=[c.GetMg() for c in children]
        d=Doc([n]);ns,c=load('DeleteNulls',d);ns['main']()
        self.assertEqual([o.name for o in root.children],['a','b','c'])
        self.assertEqual([o.GetMg() for o in root.children],matrices)

    def test_delete_nested_parent_child_selection_once(self):
        root=Obj('root');n=Obj('n',0,root);inner=Obj('inner',0,n)
        Obj('a',1,inner);Obj('b',1,n);Obj('outside',1,root)
        d=Doc([inner,n]);ns,c=load('DeleteNulls',d);ns['main']()
        self.assertEqual([o.name for o in root.children],['a','b','outside'])
        deleted=[x[1] for x in d.events if isinstance(x,tuple) and x[0]==c.UNDOTYPE_DELETEOBJ]
        self.assertEqual(sorted(deleted),['inner','n'])

    def test_delete_selected_parent_processed_once(self):
        root=Obj('root');n=Obj('n',0,root);inner=Obj('inner',0,n)
        Obj('a',1,inner)
        d=Doc([n,inner]);ns,c=load('DeleteNulls',d);ns['main']()
        deleted=[x[1] for x in d.events if isinstance(x,tuple) and x[0]==c.UNDOTYPE_DELETEOBJ]
        self.assertEqual(sorted(deleted),['inner','n'])

    def test_delete_empty_null_and_keep_unselected_sibling(self):
        root=Obj('root');n=Obj('n',0,root);other=Obj('other',0,root)
        d=Doc([n]);ns,c=load('DeleteNulls',d);ns['main']()
        self.assertEqual(root.children,[other])


if __name__ == '__main__':
    unittest.main()
