#!/usr/bin/env python3
"""Read-only PPTX text, explicit font declarations and native object inventory.

--expected-text accepts {"slides": [{"text": "paragraph one\nparagraph two"}]}.
Slides can also be strings. Text comparison preserves punctuation and whitespace.
This does not render the deck or resolve inherited layout/master/theme properties.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def read_xml(archive, name):
    data = archive.read(name)
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError(f"DTD/entity declarations are unsupported: {name}")
    return ET.fromstring(data)


def paragraph_text(paragraph):
    chunks = []
    for node in paragraph.iter():
        if node.tag == f"{A}t":
            chunks.append(node.text or "")
        elif node.tag == f"{A}br":
            chunks.append("\n")
        elif node.tag == f"{A}tab":
            chunks.append("\t")
    return "".join(chunks)


def resolve_target(source, relationship):
    target = relationship.get('Target', '')
    uri = urlsplit(target)
    if relationship.get('TargetMode', 'Internal') != 'Internal' or not target or uri.scheme or uri.netloc or uri.query or '\\' in target:
        raise ValueError(f'unsafe or non-internal part target: {target}')
    path = unquote(uri.path)
    part = posixpath.normpath(path.lstrip('/') if path.startswith('/') else posixpath.join(posixpath.dirname(source), path))
    if not path or part in {'.', '..'} or part.startswith('../'):
        raise ValueError(f'unsafe part target: {target}')
    return part


def relationships_part(source):
    return posixpath.join(posixpath.dirname(source), '_rels', posixpath.basename(source) + '.rels')


def audit(deck: Path, expected=None, min_font_size=None, allowed_fonts=None):
    issues, slides = [], []
    allowed = set(allowed_fonts or [])
    expected_slides = None
    if expected is not None:
        if not isinstance(expected, dict) or not isinstance(expected.get('slides'), list):
            raise ValueError('expected text must be an object with a slides array')
        expected_slides = []
        for item in expected['slides']:
            text = item.get('text') if isinstance(item, dict) else item
            if not isinstance(text, str):
                raise ValueError('each expected slide must be a string or an object with a text string')
            expected_slides.append(text)
    if min_font_size is not None and min_font_size <= 0:
        raise ValueError('minimum font size must be positive')
    with zipfile.ZipFile(deck) as archive:
        members = archive.infolist()
        if len(members) > 5000 or sum(m.file_size for m in members) > 512 * 1024 * 1024 or any(m.file_size > 100 * 1024 * 1024 for m in members):
            raise ValueError('archive exceeds inspection size limits')
        root_relationships = read_xml(archive, '_rels/.rels')
        office = [rel for rel in root_relationships.findall(f'{PR}Relationship') if rel.get('Type', '').endswith('/officeDocument')]
        if len(office) != 1:
            raise ValueError('expected exactly one root officeDocument relationship')
        presentation_part = resolve_target('', office[0])
        presentation = read_xml(archive, presentation_part)
        if presentation.tag != f'{P}presentation':
            raise ValueError('officeDocument target must have a presentation XML root')
        relationships = read_xml(archive, relationships_part(presentation_part))
        targets = {rel.get('Id'): rel for rel in relationships.findall(f'{PR}Relationship')}
        ordered = presentation.findall(f'.//{P}sldId')
        if expected_slides is not None and len(expected_slides) != len(ordered):
            issues.append({'check': 'source_slide_count', 'expected': len(expected_slides), 'actual': len(ordered)})
        for number, item in enumerate(ordered, 1):
            rel = targets.get(item.get(f'{R}id'))
            if rel is None or not rel.get('Type', '').endswith('/slide'):
                raise ValueError(f'slide {number} has no internal relationship')
            part = resolve_target(presentation_part, rel)
            root = read_xml(archive, part)
            text = '\n'.join(paragraph_text(p) for p in root.iter(f'{A}p'))
            native = {
                'shapes': len(list(root.iter(f'{P}sp'))),
                'text_shapes': sum(sp.find(f'{P}txBody') is not None for sp in root.iter(f'{P}sp')),
                'pictures': len(list(root.iter(f'{P}pic'))),
                'groups': len(list(root.iter(f'{P}grpSp'))),
                'connectors': len(list(root.iter(f'{P}cxnSp'))),
                'graphic_frames': len(list(root.iter(f'{P}graphicFrame'))),
                'tables': len(list(root.iter(f'{A}tbl'))),
            }
            declarations = []
            for properties in root.iter():
                if properties.tag not in {f'{A}rPr', f'{A}defRPr', f'{A}endParaRPr'}:
                    continue
                size = int(properties.get('sz')) / 100 if properties.get('sz') else None
                fonts = sorted({node.get('typeface') for node in properties if node.tag in {f'{A}latin', f'{A}ea', f'{A}cs'} and node.get('typeface')})
                declarations.append({'property_kind': properties.tag.split('}')[-1], 'size_pt': size, 'fonts': fonts})
                if size is not None and min_font_size is not None and size < min_font_size:
                    issues.append({'slide': number, 'check': 'min_font_size', 'size_pt': size, 'minimum_pt': min_font_size})
                for font in fonts:
                    if allowed and not font.startswith('+') and font not in allowed:
                        issues.append({'slide': number, 'check': 'allowed_font', 'font': font})
            text_runs = list(root.iter(f'{A}r')) + list(root.iter(f'{A}fld'))
            explicit_size_runs, explicit_font_runs = 0, 0
            for run in text_runs:
                props = run.find(f'{A}rPr')
                if props is not None:
                    explicit_size_runs += props.get('sz') is not None
                    explicit_font_runs += any(node.get('typeface') and not node.get('typeface').startswith('+') for node in props if node.tag in {f'{A}latin', f'{A}ea', f'{A}cs'})
            coverage = 'not_applicable' if not text_runs else 'complete_explicit_runs' if explicit_size_runs == explicit_font_runs == len(text_runs) else 'partial' if explicit_size_runs or explicit_font_runs else 'unresolved'
            result = {'slide': number, 'part': part, 'text': text, 'native_objects': native,
                      'explicit_font_declarations': declarations,
                      'runs_without_explicit_size': len(text_runs) - explicit_size_runs,
                      'font_coverage': {'status': coverage, 'text_runs': len(text_runs), 'runs_with_explicit_size': explicit_size_runs, 'runs_with_explicit_font_name': explicit_font_runs}}
            if expected_slides is not None:
                expected_text = expected_slides[number - 1] if number <= len(expected_slides) else None
                result['source_text_match'] = text == expected_text
                result['expected_text'] = expected_text
                if not result['source_text_match']:
                    issues.append({'slide': number, 'check': 'source_text', 'message': 'extracted text differs from the exact source'})
            slides.append(result)
    return {'deck': str(deck), 'ok': not issues, 'slides': slides, 'issues': issues,
            'ok_scope': 'no issues found in requested exact text and explicit slide declarations; unresolved inherited fonts are not a typography pass',
            'font_check_scope': 'explicit_slide_declarations_only',
            'parameters': {'min_font_size': min_font_size, 'allowed_fonts': sorted(allowed)},
            'limitations': [
                'Only explicit slide XML font declarations are checked; inherited layout/master/theme fonts and sizes are unresolved.',
                'Native object counts describe OOXML structure, not a guarantee of practical editability; pictures can contain flattened text.',
                'Installed fonts, actual rendering, overflow, occlusion, reading order and visual fidelity are not verified.',
                'Text extraction follows XML shape/paragraph order and excludes notes, chart text, embedded objects and image OCR.'
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck', type=Path)
    parser.add_argument('--expected-text', type=Path)
    parser.add_argument('--min-font-size', type=float)
    parser.add_argument('--allowed-font', action='append', default=[])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.output and args.output.resolve() in {args.deck.resolve(), args.expected_text.resolve() if args.expected_text else None}:
            raise ValueError('output must not overwrite an input')
        expected = json.loads(args.expected_text.read_text(encoding='utf-8')) if args.expected_text else None
        report = audit(args.deck, expected, args.min_font_size, args.allowed_font)
        payload = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding='utf-8')
        print(payload, end='')
        return 0 if report['ok'] else 1
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
