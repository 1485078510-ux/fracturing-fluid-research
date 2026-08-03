#!/usr/bin/env python3
"""Fix reference list: add missing article numbers, DOIs, and formatting."""

from docx import Document

doc = Document('四氧化三铁环氧树脂拟合/ESP-T_final.docx')

# Map: search key in reference text → replacement text
# Each fix adds missing article number (and optionally DOI)
FIXES = [
    # [8] Barati 2014 — add article 40735
    (
        "J Appl Polym Sci, 2014, 131(16).",
        "J Appl Polym Sci, 2014, 131(16): 40735."
    ),
    # [12] Silva 2019 — add article 106269
    (
        "Journal of Petroleum Science and Engineering, 2019, 182.",
        "Journal of Petroleum Science and Engineering, 2019, 182: 106269."
    ),
    # [15] Zhao 2020 — add article 107048
    (
        "Journal of Petroleum Science and Engineering, 2020, 190.",
        "Journal of Petroleum Science and Engineering, 2020, 190: 107048."
    ),
    # [16] Zhou 2022 — add article 109645
    (
        "Journal of Petroleum Science and Engineering, 2022, 208.",
        "Journal of Petroleum Science and Engineering, 2022, 208: 109645."
    ),
    # [18] Li N 2023 — add article 211782
    (
        "Geoenergy Science and Engineering, 2023, 227.",
        "Geoenergy Science and Engineering, 2023, 227: 211782."
    ),
    # [19] Gong Z 2024 — add article 130945
    (
        "Fuel, 2024, 364.",
        "Fuel, 2024, 364: 130945."
    ),
    # [22] Guo X 2024 — add article 111525
    (
        "Journal of Energy Storage, 2024, 88.",
        "Journal of Energy Storage, 2024, 88: 111525."
    ),
    # [25] Sabins 2021 — add SPE number 204374
    (
        "[C]. SPE International Conference on Oilfield Chemistry, 2021.",
        "[C]. SPE-204374-MS, SPE International Conference on Oilfield Chemistry, The Woodlands, Texas, 2021."
    ),
    # [28] Gong Z 2024 — add article 133085
    (
        "Colloids and Surfaces A: Physicochemical and Engineering Aspects, 2024, 683.",
        "Colloids and Surfaces A: Physicochemical and Engineering Aspects, 2024, 683: 133085."
    ),
    # [1] Chong 2016 — "1633-52" -> clearer "1633-1652"
    (
        "Applied Energy, 2016, 162: 1633-52.",
        "Applied Energy, 2016, 162: 1633-1652."
    ),
    # [2] Montgomery 2005 — "155-75" -> "155-175"
    (
        "AAPG Bull, 2005, 89(2): 155-75.",
        "AAPG Bull, 2005, 89(2): 155-175."
    ),
]

fixed_count = 0
for i, p in enumerate(doc.paragraphs):
    for search, replace in FIXES:
        if search in p.text:
            for run in p.runs:
                if search in run.text:
                    run.text = run.text.replace(search, replace)
                    print(f'  [{i}] Fixed: {search[:60]}...')
                    fixed_count += 1
                    break
            else:
                # Text might be split across runs; reconstruct
                full = p.text
                if search in full:
                    full = full.replace(search, replace)
                    for run in p.runs:
                        run.text = ''
                    p.runs[0].text = full
                    print(f'  [{i}] Fixed (full-para): {search[:60]}...')
                    fixed_count += 1

# Save to new file (in case original is locked)
out = '四氧化三铁环氧树脂拟合/ESP-T_参考文献修正.docx'
doc.save(out)
print(f'\n{fixed_count} references fixed.')
print(f'Saved to: {out}')
print('Please close Word, then rename to ESP-T_final.docx')