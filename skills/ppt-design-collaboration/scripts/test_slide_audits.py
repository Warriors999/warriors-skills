import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tool = load('reference_audit', 'slide-reference-audit.py')

    def image(self, name, size):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', size, 'white').save(path)
        return path

    def test_rejects_aspect_change(self):
        with self.assertRaisesRegex(ValueError, 'aspect'):
            self.tool.compare(self.image('a.png', (160, 90)), self.image('b.png', (100, 100)), self.root / 'out', 12)

    def test_resolution_change_is_explicit_and_reported(self):
        a, b = self.image('a.png', (160, 90)), self.image('b.png', (320, 180))
        with self.assertRaisesRegex(ValueError, 'normalize-resolution'):
            self.tool.compare(a, b, self.root / 'out', 12)
        result = self.tool.compare(a, b, self.root / 'out', 12, normalize_resolution=True)
        self.assertEqual(result['approved_original_size_px'], [160, 90])
        self.assertEqual(result['rendered_original_size_px'], [320, 180])
        self.assertTrue(result['resolution_normalized'])

    def test_audits_and_comparisons_do_not_overwrite_other_inputs(self):
        a, b, c = self.image('one/image.png', (60, 40)), self.image('two/image.png', (60, 40)), self.image('one/image.jpg', (60, 40))
        results = [self.tool.audit(p, self.root / 'audit', 3, 2) for p in (a, b, c)]
        self.assertEqual(len({r['json'] for r in results}), 3)
        results = [self.tool.compare(a, p, self.root / 'compare', 12) for p in (b, c)]
        self.assertEqual(len({r['json'] for r in results}), 2)
        self.assertTrue(all(Path(r['json']).exists() for r in results))


class PptxAuditTests(unittest.TestCase):
    def test_text_fonts_and_editability_without_render_claims(self):
        tool = load('pptx_audit', 'pptx-content-audit.py')
        with tempfile.TemporaryDirectory() as folder:
            deck = Path(folder) / 'test.pptx'
            with zipfile.ZipFile(deck, 'w') as z:
                z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="root" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>')
                z.writestr('ppt/presentation.xml', '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>')
                z.writestr('ppt/_rels/presentation.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/></Relationships>')
                z.writestr('ppt/slides/slide2.xml', '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:rPr sz="1800"><a:latin typeface="Arial"/></a:rPr><a:t>Hello, world!</a:t></a:r></a:p></p:txBody></p:sp><p:pic/></p:spTree></p:cSld></p:sld>')
            report = tool.audit(deck, expected={'slides': [{'text': 'Hello world!'}]}, min_font_size=20, allowed_fonts=['Other'])
            slide = report['slides'][0]
            self.assertEqual(slide['text'], 'Hello, world!')
            self.assertFalse(slide['source_text_match'])
            self.assertEqual(slide['native_objects']['text_shapes'], 1)
            self.assertEqual(slide['native_objects']['pictures'], 1)
            self.assertTrue(any(i['check'] == 'min_font_size' for i in report['issues']))
            self.assertTrue(any(i['check'] == 'allowed_font' for i in report['issues']))
            self.assertIn('inherited', ' '.join(report['limitations']))
            matched = tool.audit(deck, expected={'slides': ['Hello, world!']}, min_font_size=18, allowed_fonts=['Arial'])
            self.assertTrue(matched['ok'])
            self.assertTrue(matched['slides'][0]['source_text_match'])
            mismatch = tool.audit(deck, expected={'slides': []})
            self.assertTrue(any(i['check'] == 'source_slide_count' for i in mismatch['issues']))
            source = Path(folder) / 'source.json'
            source.write_text(json.dumps({'slides': ['Hello, world!']}), encoding='utf-8')
            output = Path(folder) / 'report.json'
            command = [sys.executable, str(Path(__file__).with_name('pptx-content-audit.py')), str(deck), '--expected-text', str(source), '--min-font-size', '18', '--allowed-font', 'Arial', '--output', str(output)]
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout), json.loads(output.read_text()))
            failed = subprocess.run(command + ['--min-font-size', '24'], capture_output=True, text=True)
            self.assertEqual(failed.returncode, 1)
            relocated = Path(folder) / 'relocated.pptx'
            with zipfile.ZipFile(deck) as old, zipfile.ZipFile(relocated, 'w') as new:
                for name in old.namelist():
                    new.writestr(name.replace('ppt/', 'decks/').replace('presentation.xml', 'main.xml'), old.read(name).replace(b'ppt/', b'decks/').replace(b'presentation.xml', b'main.xml'))
            self.assertTrue(tool.audit(relocated, expected={'slides': ['Hello, world!']})['ok'])
            self.assertEqual(tool.audit(deck)['slides'][0]['font_coverage']['status'], 'complete_explicit_runs')

    def test_inherited_fonts_are_reported_unresolved(self):
        tool = load('pptx_audit', 'pptx-content-audit.py')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'inherited.pptx'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="root" Type="x/officeDocument" Target="ppt/presentation.xml"/></Relationships>')
                z.writestr('ppt/presentation.xml', '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:sldIdLst><p:sldId id="256" r:id="slide"/></p:sldIdLst></p:presentation>')
                z.writestr('ppt/_rels/presentation.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="slide" Type="x/slide" Target="slides/page.xml"/></Relationships>')
                z.writestr('ppt/slides/page.xml', '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:grpSp><p:sp><p:txBody><a:p><a:r><a:t>Grouped, text!</a:t></a:r></a:p></p:txBody></p:sp></p:grpSp></p:spTree></p:cSld></p:sld>')
            report = tool.audit(path, min_font_size=20, allowed_fonts=['Arial'])
            self.assertEqual(report['slides'][0]['text'], 'Grouped, text!')
            self.assertEqual(report['slides'][0]['native_objects']['text_shapes'], 1)
            self.assertEqual(report['slides'][0]['font_coverage']['status'], 'unresolved')
            self.assertEqual(report['font_check_scope'], 'explicit_slide_declarations_only')
            wrong_root = Path(folder) / 'wrong-root.pptx'
            with zipfile.ZipFile(path) as old, zipfile.ZipFile(wrong_root, 'w') as new:
                for name in old.namelist():
                    value = old.read(name)
                    if name == '_rels/.rels':
                        value = value.replace(b'ppt/presentation.xml', b'ppt/slides/page.xml')
                    new.writestr(name, value)
            with self.assertRaisesRegex(ValueError, 'presentation'):
                tool.audit(wrong_root)


if __name__ == '__main__':
    unittest.main()
