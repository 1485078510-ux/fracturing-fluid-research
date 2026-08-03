# -*- coding: utf-8 -*-
"""Encode .drawio XML to diagrams.net viewer URL (correct raw deflate encoding)."""
import sys, io, zlib, base64, urllib.parse, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def encode_drawio_url(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    # encodeURIComponent equivalent: percent-encode, preserving unreserved chars
    encoded_xml = urllib.parse.quote(xml_str, safe="~()*!.'")
    # Raw deflate (wbits=-15 = no zlib header, matching JS pako.deflateRaw)
    co = zlib.compressobj(wbits=-15)
    compressed = co.compress(encoded_xml.encode('utf-8'))
    compressed += co.flush()
    # Standard base64
    b64 = base64.b64encode(compressed).decode('ascii')
    url = f"https://viewer.diagrams.net/?lightbox=1&edit=_blank#R{b64}"
    return url

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python drawio_url.py <file.drawio> [...]")
        sys.exit(1)
    for fp in sys.argv[1:]:
        if not os.path.exists(fp):
            print(f"Not found: {fp}")
            continue
        url = encode_drawio_url(fp)
        name = os.path.basename(fp)
        print(f"\n{name}:")
        print(url)