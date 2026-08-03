#!/usr/bin/env python3
"""Encode .drawio XML files as diagrams.net browser URLs (no CLI needed)."""
import zlib
import base64
import os

output_dir = r'c:\Users\郝\Desktop\claude\荧光压裂液'

files = [
    'fig1_core_shell_structure.drawio',
    'fig2_process_flow.drawio',
    'fig3_method_flowchart.drawio',
]

for fname in files:
    fpath = os.path.join(output_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        xml = f.read()

    # Encode: deflate → base64 (URL-safe) → URL encode
    compressed = zlib.compress(xml.encode('utf-8'), level=9)[2:-4]  # raw deflate
    b64 = base64.b64encode(compressed).decode('ascii')
    url_encoded = b64.replace('+', '-').replace('/', '_')
    url = f'https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title={fname}#R{url_encoded}'
    print(f'\n{fname}:')
    print(url)