"""Run in C4D Script Manager or c4dpy. Creates only detached test documents.

No user scene is opened, saved, activated or modified. Results go to Console.
The numeric FigureScale dialog is replaced with fixed test input; visual layout
and real keyboard events still need manual acceptance.
"""
import c4d
import math
from pathlib import Path
import types
import traceback
import json
import hashlib
import tempfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TEST_REVISION = 'batch1-r3-hg-prefix'
DIAGNOSTICS = []


def live_object(doc, name, phase):
    """Resolve from the current scene after Undo/Redo, not a retained wrapper."""
    obj = doc.SearchObject(name)
    assert obj is not None, ('Object missing after ' + phase, name)
    def xyz(v):
        return [v.x, v.y, v.z]
    entry = {'phase': phase, 'name': name,
             'position': xyz(obj.GetAbsPos()), 'rotation': xyz(obj.GetAbsRot()),
             'scale': xyz(obj.GetRelScale())}
    DIAGNOSTICS.append(entry)
    print('LIVE:', entry)
    return obj


class Proxy:
    def __init__(self, original, **overrides):
        self.original, self.overrides = original, overrides
    def __getattr__(self, key):
        return self.overrides[key] if key in self.overrides else getattr(self.original, key)


def load(name, doc, keys=0, input_ok=True):
    path = ROOT / 'c4d_scripts' / name / ('HG_' + name + '.py')
    ns = {'__name__': 'host_test_subject', 'doc': doc}
    exec(compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec'), ns)
    def get_input(device, channel, bc):
        bc[c4d.BFM_INPUT_QUALIFIER] = keys
        return input_ok
    messages = []
    ns['c4d'] = Proxy(c4d,
        documents=Proxy(c4d.documents, GetActiveDocument=lambda: doc),
        gui=Proxy(c4d.gui, GetInputState=get_input, MessageDialog=messages.append),
        EventAdd=lambda: None)
    return ns, messages


def vec_close(a, b):
    assert (a-b).GetLength() < 1e-7, (a, b)


def matrix_close(a, b):
    for key in ('off', 'v1', 'v2', 'v3'):
        vec_close(getattr(a, key), getattr(b, key))


def add(doc, name, kind=c4d.Ocube, parent=None):
    obj = c4d.BaseObject(kind)
    obj.SetName(name)
    doc.InsertObject(obj, parent=parent, pred=parent.GetDown() if parent else None)
    return obj


def select(doc, objects):
    for i, obj in enumerate(objects):
        doc.SetActiveObject(obj, c4d.SELECTION_NEW if i == 0 else c4d.SELECTION_ADD)


def figure_case():
    doc = c4d.documents.BaseDocument()
    try:
        parent = add(doc, 'parent', c4d.Onull)
        parent.SetRelScale(c4d.Vector(3, 2, 4))
        parent.SetRelRot(c4d.Vector(.2, .3, .1))
        obj = add(doc, 'plane', c4d.Oplane, parent)
        obj[c4d.PRIM_PLANE_WIDTH] = 10
        obj[c4d.PRIM_PLANE_HEIGHT] = 20
        obj.SetRelScale(c4d.Vector(2, 3, 4))
        obj.Message(c4d.MSG_UPDATE)
        doc.ExecutePasses(None, True, True, True, c4d.BUILDFLAGS_NONE)
        select(doc, [obj])
        ns, messages = load('FigureScale', doc)
        size = ns['get_object_size'](obj)
        assert abs(size[0]-60) < 1e-6, size
        old_scale = obj.GetRelScale()
        class Input:
            IDC_SOURCE_X, IDC_SOURCE_Y, IDC_SOURCE_Z = 1000, 1001, 1002
            def __init__(self, *args):
                self.last_input_id, self.last_input_value = 1000, 120
            def Open(self, *args, **kwargs): pass
        ns['FigureScaleDialog'] = Input
        ns['main']()
        assert not messages, messages
        vec_close(obj.GetRelScale(), c4d.Vector(4, 6, 8))
        assert abs(ns['get_object_size'](obj)[0]-120) < 1e-6
        assert doc.DoUndo()
        obj = live_object(doc, 'plane', 'FigureScale undo')
        vec_close(obj.GetRelScale(), old_scale)
        assert doc.DoRedo()
        obj = live_object(doc, 'plane', 'FigureScale redo')
        vec_close(obj.GetRelScale(), c4d.Vector(4, 6, 8))
    finally:
        doc.Flush()


def round_case(keys=0, input_ok=True):
    doc = c4d.documents.BaseDocument()
    try:
        obj = add(doc, 'rounded')
        original = c4d.Vector(1.2, 2.6, -3.1)
        rotation = c4d.Vector(*[math.radians(x) for x in (10.26, 20.24, -30.26)])
        obj.SetAbsPos(original)
        obj.SetAbsRot(rotation)
        select(doc, [obj])
        ns, _ = load('RoundXYZ', doc, keys, input_ok)
        ns['main']()
        want_pos = original if input_ok and keys == c4d.QALT else c4d.Vector(1, 3, -3)
        want_rot = rotation if not input_ok or keys == 0 else c4d.Vector(*[math.radians(x) for x in (10.3, 20.2, -30.3)])
        vec_close(obj.GetAbsPos(), want_pos)
        vec_close(obj.GetAbsRot(), want_rot)
        assert doc.DoUndo()
        obj = live_object(doc, 'rounded', 'RoundXYZ undo')
        vec_close(obj.GetAbsPos(), original)
        vec_close(obj.GetAbsRot(), rotation)
        assert doc.DoRedo()
        obj = live_object(doc, 'rounded', 'RoundXYZ redo')
        vec_close(obj.GetAbsPos(), want_pos)
        vec_close(obj.GetAbsRot(), want_rot)
    finally:
        doc.Flush()


def snapshot(doc):
    result = []
    def walk(obj, prefix):
        while obj:
            path = prefix + '/' + obj.GetName()
            result.append((path, obj.GetMg()))
            walk(obj.GetDown(), path)
            obj = obj.GetNext()
    walk(doc.GetFirstObject(), '')
    return result


def same_snapshot(a, b):
    assert [x[0] for x in a] == [x[0] for x in b], ([x[0] for x in a], [x[0] for x in b])
    for x, y in zip(a, b): matrix_close(x[1], y[1])


def delete_case():
    doc = c4d.documents.BaseDocument()
    try:
        root = add(doc, 'root', c4d.Ocube)
        root.SetRelPos(c4d.Vector(10, 20, 30))
        root.SetRelRot(c4d.Vector(.2, .3, .1))
        n = add(doc, 'null', c4d.Onull, root)
        n.SetRelPos(c4d.Vector(4, 5, 6))
        n.SetRelScale(c4d.Vector(2))
        a = add(doc, 'a', c4d.Ocube, n)
        inner = add(doc, 'inner', c4d.Onull, n)
        inner.InsertAfter(a)
        b = add(doc, 'b', c4d.Ocube, inner)
        c = add(doc, 'c', c4d.Ocube, n)
        c.InsertAfter(inner)
        for i, obj in enumerate((a,b,c)):
            obj.SetRelPos(c4d.Vector(i+1, i+2, i+3))
        select(doc, [inner, n])
        before = snapshot(doc)
        matrices = {obj.GetName(): obj.GetMg() for obj in (a,b,c)}
        ns, _ = load('DeleteNulls', doc)
        ns['main']()
        assert [obj.GetName() for obj in root.GetChildren()] == ['a','b','c']
        for obj in root.GetChildren(): matrix_close(obj.GetMg(), matrices[obj.GetName()])
        after = snapshot(doc)
        assert doc.DoUndo()
        same_snapshot(snapshot(doc), before)
        assert doc.DoRedo()
        same_snapshot(snapshot(doc), after)
    finally:
        doc.Flush()


def main():
    DIAGNOSTICS.clear()
    cases = [('FigureScale parent scale / plane / Undo / Redo', figure_case),
             ('DeleteNulls nested order / world matrix / Undo / Redo', delete_case)]
    for label, keys, ok in [('default',0,True), ('Alt',c4d.QALT,True),
                            ('Shift',c4d.QSHIFT,True), ('input failure',0,False)]:
        cases.append(('RoundXYZ '+label, lambda k=keys,o=ok: round_case(k,o)))
    failures = []
    results = []
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    print('BATCH1 HOST TEST; C4D VERSION:', c4d.GetC4DVersion(), 'REVISION:', TEST_REVISION)
    for label, run in cases:
        try:
            run()
            print('PASS:',label)
            results.append({'case': label, 'passed': True})
        except Exception:
            failures.append(label)
            print('FAIL:',label)
            trace = traceback.format_exc()
            print(trace)
            results.append({'case': label, 'passed': False, 'traceback': trace})
    print('RESULT:', len(cases)-len(failures), '/', len(cases))
    # Local timestamped reports survive closing the console. They are not saved
    # into the public source repository and contain no user scene contents.
    try:
        folder = Path(tempfile.gettempdir()) / 'c4d-scripts-host-tests'
        folder.mkdir(parents=True, exist_ok=True)
        report_path = folder / ('batch1-' + stamp + '.json')
        paths = [Path(__file__).resolve()] + [
            ROOT / 'c4d_scripts' / name / ('HG_' + name + '.py')
            for name in ('FigureScale', 'RoundXYZ', 'DeleteNulls')]
        hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        report = {'revision': TEST_REVISION, 'time': stamp,
                  'c4d_version': c4d.GetC4DVersion(), 'results': results,
                  'passed': len(cases)-len(failures), 'total': len(cases),
                  'diagnostics': DIAGNOSTICS, 'disk_source_sha256': hashes}
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print('REPORT:', report_path)
    except Exception:
        print('REPORT WRITE FAILED:')
        traceback.print_exc()
    if failures:
        raise AssertionError(failures)


if __name__ == '__main__':
    main()
