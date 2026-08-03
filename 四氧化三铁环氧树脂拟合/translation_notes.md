# Translation Notes — ESP-T Paper

## Source Information
- **Source file:** ESP-T_final.docx (DOCX format)
- **Extraction:** python-docx text extraction via `scripts/office.py`
- **Status:** Complete text extraction, **no page-level layout**, **no figure/table images**
- **Date:** 2026-06-14

## Extraction Notes

### What's available
- ✅ Full body text (Abstract, Introduction, Experiments, Results & Discussion, Conclusions)
- ✅ All references (29 citations)
- ✅ All table data (extracted as text from DOCX)
- ✅ All equations (described in text form)
- ✅ Figure/table captions and references

### What's missing
- ❌ Page numbers — DOCX has no fixed pagination
- ❌ Figure/table images — embedded images in DOCX not extracted as separate assets
- ❌ Real-time page-to-paragraph mapping

### Translation confidence
- **High confidence** on all technical content. Terminology consistent with petroleum engineering standards (SY/T 6376-2008, SY/T 5107-2016).
- **Terminology decisions:**
  - "tracer proppant" → 示踪支撑剂 (industry standard)
  - "production allocation" → 分段产量监测 (context-appropriate, not literal "产量分配")
  - "anomalous transport" → 非Fick异常传输 (preserved technical precision)
  - "water-resistant, oil-permeable" → 阻水亲油 (concise Chinese idiom)

## Draft Mode
This is a complete reader artifact. The only limitations are:
1. No figure/table images (visual assets embedded in DOCX not available as standalone files)
2. No page-level anchors (block-level S001-S029 anchors used instead)

## Notes for Advisor Presentation
The most presentation-worthy data points are in blocks:
- **S005**: Research gap identification
- **S017-S020**: Key performance data (thermal, WCA, permeability)
- **S023**: Core ADE model results (R²=0.9939, erfc 47%)
- **S025**: Limitations (to pre-empt advisor questions)