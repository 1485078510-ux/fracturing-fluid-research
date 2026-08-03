"""Verify and polish introduction for scientific accuracy and logic."""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def collapse_and_set(p, text):
    ref_rpr = None
    first_r = p.find(f'.//{{{W}}}r')
    if first_r is not None: ref_rpr = first_r.find(f'{{{W}}}rPr')
    for child in list(p):
        if child.tag.split('}')[-1] != 'pPr': p.remove(child)
    r = etree.SubElement(p, f'{{{W}}}r')
    if ref_rpr: r.append(deepcopy(ref_rpr))
    else:
        rpr = etree.SubElement(r, f'{{{W}}}rPr')
        etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text

with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}
root = etree.fromstring(all_files['word/document.xml'])
all_p = root.findall(f'.//{{{W}}}p')
fixes = []

# --- FIX 1: P3 - "beaker" -> "well-mixed vessel", split final sentence ---
for p in all_p:
    t = pt(p).strip()
    if 'characterizes release in a beaker' in t:
        new_p3 = (
            "The question that remains unanswered, and that this paper addresses, is "
            "whether a tracer proppant can deliver more than qualitative confirmation "
            "of stage activity: can it quantify how much each stage is producing, "
            "using only the shape of the tracer breakthrough curve (BTC) measured at "
            "the wellhead? Answering this question requires solving two distinct "
            "problems. The first is the release problem: at what rate does the tracer "
            "leave the proppant matrix? All existing tracer proppant studies address "
            "this through batch experiments fitted to the Korsmeyer-Peppas (K-P) "
            "power law, C/C0 = K t^n [28-30]. The K-P model classifies the release "
            "mechanism (Fickian diffusion for n <= 0.43, anomalous transport for "
            "0.43 < n < 0.85, or Case-II relaxation for n >= 0.85) and yields the "
            "temperature-dependent rate constant K. These are valuable descriptors "
            "of the release process, but they are obtained in a well-mixed vessel "
            "with no spatial coordinate and no flow field. The K-P model can "
            "quantify how fast the tracer leaves the carrier; it cannot predict "
            "the concentration that will be observed at a sampling point meters "
            "downstream, after the released tracer has traversed the proppant pack "
            "and production tubing. The transport step (advection, dispersion, and "
            "the convolution of sustained release with flow) is simply absent from "
            "the model."
        )
        collapse_and_set(p, new_p3)
        fixes.append("P3: beaker->well-mixed vessel, split final sentence")
        break

# --- FIX 2: P5 - split deconvolution sentence ---
for p in all_p:
    t = pt(p).strip()
    if 'A related class of methods expresses the BTC as the convolution' in t:
        new_p5 = (
            "The classical physics-based approach fits an analytical solution of the "
            "one-dimensional advection-dispersion equation (ADE), dC/dt + v dC/dx = "
            "D d2C/dx2, to the observed BTC. Van Genuchten and Alves [31] compiled "
            "analytical solutions for a comprehensive set of initial and boundary "
            "conditions (instantaneous pulses, finite-duration injections, and "
            "continuous sources), and these remain the standard reference. By least-"
            "squares fitting of the appropriate solution to the observed concentration "
            "history, one recovers the transport parameters: velocity v, dispersivity "
            "alpha, and, by extension, the volumetric flow rate Q and the swept pore "
            "volume. Shook et al. [32] advanced this paradigm from curve fitting to "
            "moment analysis: by integrating the BTC to compute its temporal moments, "
            "their method extracts swept volume, sweep efficiency, and remaining oil "
            "saturation directly, without requiring a numerical reservoir simulator. "
            "This is a significant practical advance, but one that still treats the "
            "tracer source as a completed, known injection. A related class of "
            "methods expresses the BTC as the convolution of the injection history "
            "with a tracer transfer function (a kernel characterized by pore volume, "
            "Peclet number, and a dispersion correction factor) and recovers the "
            "kernel via parametric or nonparametric deconvolution; expressing the "
            "convolution in terms of cumulative flow rather than clock time renders "
            "these methods robust to variable production rates. Fontalvo et al. [16] "
            "underscored that model selection is not a matter of convenience: applying "
            "a physically inappropriate transport model to partitioning tracer data "
            "can systematically overestimate or underestimate remaining oil "
            "saturation, with direct financial consequences for field-development "
            "decisions."
        )
        collapse_and_set(p, new_p5)
        fixes.append("P5: split deconvolution sentence")
        break

# --- FIX 3: P7 - split final consequence sentence ---
for p in all_p:
    t = pt(p).strip()
    if 'qualitative diagnostic tools: they can confirm' in t:
        new_p7 = (
            "A single structural premise runs through every method described above, "
            "from peak-time estimation through CTRW to full numerical inversion: the "
            "tracer source is treated as a known input. Whether it is a Dirac delta "
            "pulse, a finite-duration injection of measured concentration, or a "
            "continuous source of prescribed strength, the source function is an "
            "experimental boundary condition; the inverse problem is to estimate the "
            "transport parameters given that known source. A tracer proppant does "
            "not satisfy this premise. The tracer is not injected as a discrete "
            "event; it is released continuously from a polymeric matrix at a rate "
            "governed by matrix diffusion and polymer relaxation (the very processes "
            "characterized by K-P kinetics), and this release evolves throughout the "
            "production period. The BTC measured at the wellhead is therefore the "
            "convolution of two unknown functions: a release rate governed by matrix-"
            "diffusion kinetics, and a transport operator governed by advection and "
            "dispersion. Neither function is known independently, and both must be "
            "recovered from the shape of a single concentration history. To our "
            "knowledge, this coupled release-transport inverse problem has not been "
            "addressed in the literature. Its practical consequence is that existing "
            "tracer proppants, despite their operational advantages of single-"
            "placement longevity and freedom from downhole instrumentation, remain "
            "qualitative tools: they can confirm which stages are producing but "
            "cannot answer the quantitative question that operators and reservoir "
            "engineers need answered."
        )
        collapse_and_set(p, new_p7)
        fixes.append("P7: split consequence sentence")
        break

# --- FIX 4: P9 - "independent" -> "complementary" ---
for p in all_p:
    t = pt(p).strip()
    if 'Four independent lines of evidence support the model' in t:
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and 'Four independent lines of evidence' in te.text:
                    te.text = te.text.replace(
                        'Four independent lines of evidence support the model.',
                        'Four complementary lines of evidence support the model.'
                    )
                    fixes.append("P9: independent -> complementary")
                    break
        break

# --- FIX 5: P6 - tighten CTRW description ---
for p in all_p:
    t = pt(p).strip()
    if 'CTRW has been applied to tracer tests in fractured and heterogeneous' in t:
        # Already fixed in previous pass! Skip.
        pass
    elif 'CTRW has been successfully applied to tracer tests' in t:
        old_ctrw = (
            "CTRW has been successfully applied to tracer tests in fractured "
            "crystalline rock and heterogeneous carbonate reservoirs, and the "
            "beta parameter has been linked quantitatively to fracture network "
            "topology, specifically, fracture orientation relative to the mean "
            "flow direction."
        )
        new_ctrw = (
            "CTRW has been applied to tracer tests in fractured and heterogeneous "
            "reservoirs, with the beta parameter linked quantitatively to fracture "
            "network characteristics."
        )
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and old_ctrw in te.text:
                    te.text = te.text.replace(old_ctrw, new_ctrw)
                    fixes.append("P6: tightened CTRW description")
                    break
        break

# --- FIX 6: P1 - replace em dash in monitoring list ---
for p in all_p:
    t = pt(p).strip()
    if 'Tracer-based diagnostics circumvent these limitations' in t:
        # Replace em dash before "they require no downhole tools"
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and 'limitations—they require' in te.text:
                    te.text = te.text.replace(
                        'limitations—they require',
                        'limitations: they require'
                    )
                    fixes.append("P1: em dash -> colon")
                    break
        break

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(doc_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

# Verify refs
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
ref_start = next(i for i,p in enumerate(all_p2) if pt(p).strip()=='References')
refs = []
for i, p in enumerate(all_p2):
    if i >= ref_start: break
    for m in re.finditer(r'\[([\d,\-–\s]+)\]', pt(p)):
        for part in re.split(r',', m.group(1)):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1):
                    if n not in refs: refs.append(n)
            elif part.isdigit() and int(part) not in refs:
                refs.append(int(part))

print(f"REFS: {len(refs)}, seq={all(refs[i]<=refs[i+1] for i in range(len(refs)-1))}")
if len(refs) < 41:
    print(f"Missing: {sorted(set(range(1,42))-set(refs))}")
print(f"Fixes ({len(fixes)}):")
for f in fixes:
    print(f"  - {f}")
