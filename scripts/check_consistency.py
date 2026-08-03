"""Check body text paragraphs for consistency with revised Introduction."""
from docx import Document

doc = Document(r"c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件\ESP-T_Final_4-revised.docx")

targets = [
    'These kinetic parameters provide',
    'Taken together, these results establish',
    'conventional ADE-based tracer',
    'model is validated through physical',
    'inverse problem',
    'bridging the gap',
    'coupled release-transport',
    'reverses this logic',
    'shift from descriptive to predictive',
]

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    for t in targets:
        if t.lower() in text.lower():
            print(f'[{i}] Found "{t}":')
            print(f'    {text[:300]}')
            print()
            break
