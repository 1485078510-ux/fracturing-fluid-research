# -*- coding: utf-8 -*-
"""Clean up old manuscript versions and intermediate files."""
import os, glob

SUBMIT = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'
FIT = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合'
ROOT = r'c:\Users\郝\Desktop\claude'

deleted_count = 0

def rm(f):
    global deleted_count
    if os.path.exists(f):
        os.remove(f)
        deleted_count += 1
        print(f'  DEL: {os.path.basename(f)}')

# ===== Clean ESP-T_投稿文件 =====
print('=== Cleaning ESP-T_投稿文件 ===')
remove_patterns = [
    'ESP-T_v2_manuscript*', 'ESP-T_v3_manuscript*', 'ESP-T_v4_*',
    'ESP-T_Revised_*', 'ESP-T_Final_v[2-5]*', 'ESP-T_Final_merged*',
    'ESP-T_Final_submit*', 'ESP-T_Final_NewIntro*', 'ESP-T_Final_3-revised*',
    'ESP-T_Final_4-intro*', 'ESP-T_Final.docx', 'ESP-T_Final_CN.docx',
    'Supplementary_Material_new*', 'Supplementary_Material_trimmed*',
    'Reference_Verification*',
    'Cover_Letter*', 'Coverletter*',
    '*25081373691*', 'BTC_fitting.csv',
    'apply_review_fixes.py', 'fix_results.py', 'rewrite_intro.py',
]
for pat in remove_patterns:
    for f in glob.glob(os.path.join(SUBMIT, pat)):
        rm(f)

print(f'\nRemaining in ESP-T_投稿文件:')
for f in sorted(os.listdir(SUBMIT)):
    print(f'  {f}')

# ===== Clean fitting directory =====
print('\n=== Cleaning fitting directory ===')
remove_patterns_fit = [
    'fit_solute_v[23].py',      # old wrong-geometry fits
    'fit_btc_raw.py',            # intermediate raw data fit
    'fit_corrected_v2.py',       # intermediate wide-bounds fit
    'revise_v3.py',              # intermediate revision
    'fix_v3.py',                 # intermediate fix
    'fix_v3_final.py',           # intermediate fix
    'rebuild_v4.py',             # v4 builder (superseded by v5)
    'rewrite_intro_v4.py',       # intermediate intro rewrite
    # Old one-off fix scripts
    'add_section35.py', 'add_supp_details.py', 'add_tables.py',
    'apply_all_revisions.py', 'apply_other_fixes.py', 'balance_stats_eng.py',
    'build_final.py', 'convert_to_docx.py', 'cover_letter.py',
    'embed_supp_figures.py', 'export_results.py',
    'final_fix_s37.py', 'final_fixes.py', 'final_rebuild.py',
    'fix_crossrefs.py', 'fix_equations.py',
    'gen_supp_docx.py', 'generate_fuel_figures.py', 'generate_supplementary.py',
    'insert_figures.py', 'minimal_edit.py',
    'polish_full.py', 'polish_language.py',
    'rebuild_final.py', 'rebuild_supp_final.py',
    'reference_verification.py', 'renumber_refs.py',
    'restructure_section37.py', 'reviewer_fixes.py',
    'revise_manuscript.py', 'rewrite_37_38.py', 'rewrite_section34.py',
    'safe_rebuild.py', 'supp_logical.py',
    'translate_cn.py', 'translate_final.py', 'translate_full.py',
    'update_plot.py',
]
for pat in remove_patterns_fit:
    for f in glob.glob(os.path.join(FIT, pat)):
        rm(f)

print(f'\nRemaining Python scripts in fitting directory:')
for f in sorted(os.listdir(FIT)):
    if f.endswith('.py'):
        print(f'  {f}')

# ===== Clean root directory one-off scripts =====
print('\n=== Cleaning root directory one-off scripts ===')
root_patterns = [
    'add_ade_fo_link.py', 'add_detail_slides.py', 'add_final_details.py',
    'add_refs_final.py', 'add_toa_comparison.py', 'add_twophase.py',
    'apply_all_improvements.py', 'build_ppt.py', 'build_ppt_final.py',
    'build_ppt_full.py', 'content_review.py', 'enhance_ppt.py',
    'figs_final.py', 'final2_figs.py', 'final_add_refs.py',
    'final_audit.py', 'final_check.py', 'final_figs.py', 'final_fix.py',
    'final_intro.py', 'final_polish.py', 'final_refs.py', 'final_topfigs.py',
    'finalize_submit.py', 'fix_all_symbols.py', 'fix_cite_order.py',
    'fix_crossrefs.py', 'fix_figures.py', 'fix_formula_subscripts.py',
    'fix_refs.py', 'fix_twophase.py', 'generate_figures.py',
    'generate_paper.py', 'insert_figures.py', 'integrate_symbols.py',
    'merge_docs.py', 'morandi_figs.py', 'nature_figs.py',
    'origin_check.py', 'origin_final.py', 'origin_go.py',
    'origin_plot.py', 'origin_test.py', 'polish_figs.py',
    'polish_format.py', 'precise_cites.py', 'rebuild_all.py',
    'rebuild_all_refs.py', 'rebuild_ppt_improved.py', 'rebuild_sections.py',
    'reformat_sections.py', 'refs_done.py', 'regenerate_all_figs.py',
    'renumber_all.py', 'restore_all_refs.py', 'restore_citations.py',
    'revise_manuscript.py', 'rewrite_cover.py', 'rewrite_intro.py',
    'rewrite_intro_final.py',
]
for pat in root_patterns:
    f = os.path.join(ROOT, pat)
    if os.path.exists(f):
        rm(f)

# Also clean old DOCX in root
root_docx = [
    'ESP-T_Final.docx', 'ESP-T_Final_CN.docx', 'ESP-T_Final_v5_final.docx',
    'ESP-T_Supplementary_Material.docx',
]
for fname in root_docx:
    f = os.path.join(ROOT, fname)
    if os.path.exists(f):
        rm(f)

# Clean _dump, _exact, _src, _tables
for fname in ['_dump.txt', '_exact.txt', '_src.txt', '_tables.txt']:
    f = os.path.join(ROOT, fname)
    if os.path.exists(f):
        rm(f)

print(f'\n=== TOTAL DELETED: {deleted_count} files ===')
