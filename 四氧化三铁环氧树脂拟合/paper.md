# ESP-T 论文双语对照阅读

**Title (Original):** Epoxy Resin Microspheres Encapsulating Oleophilic Fe₃O₄ Nanoparticles as Tracer Proppants for Production Allocation

**Title (中文):** 环氧树脂微球包覆亲油性Fe₃O₄纳米颗粒作为示踪支撑剂用于分段产量监测

**Source:** ESP-T_final.docx (extracted text, no page-level layout available)
**Type:** Materials / Engineering paper (property-to-mechanism / design-to-performance arc)
**Date of reading:** 2026-06-14

---

## 章节索引

1. [Abstract](#abstract) — 摘要
2. [1 Introduction](#1-introduction) — 引言
3. [2 Experiments](#2-experiments) — 实验部分
4. [3 Results and Discussion](#3-results-and-discussion) — 结果与讨论
5. [4 Conclusions](#4-conclusions) — 结论
6. [References](#references) — 参考文献
7. [术语表](#术语表-terminology-table)
8. [汇报要点 (Critical Reading Notes)](#汇报要点-critical-reading-notes)

---

## Abstract

<a id="S001"></a>
**Source:** Abstract ¶1

**Original:**
Per-interval production monitoring is essential for evaluating stimulation effectiveness in unconventional reservoirs, yet existing tracer technologies lack durable oil-phase monitoring capability. Here we report an oleophilic tracer proppant (ESP-T) fabricated by encapsulating stearic acid-modified nano-Fe₃O₄ (nano-Fe₃O₄@SA) within an epoxy resin matrix via emulsion polymerization. ESP-T exhibits sphericity exceeding 0.9, maintains structural integrity up to 357.27 °C, and the incorporation of nano-Fe₃O₄@SA raises the water contact angle from 72.3° to 104.6°, yielding a water-resistant, oil-permeable transport characteristic. Tracer release at 30–120 °C follows the Korsmeyer–Peppas model (R² > 0.90) with diffusion exponents of 0.45–0.85, indicating synergistic Fickian diffusion and Case-II relaxation. A piecewise advection–dispersion model with tanh blending achieves R² = 0.9939 for single-phase breakthrough curves, and under steady-state two-phase flow, tracer flux quantitatively tracks oil-phase production rates. ESP-T thus integrates fracture propping with long-term production monitoring, offering a dual-function platform for unconventional reservoir management.

**中文:**
分段产量监测对评价非常规储层增产效果至关重要，但现有示踪技术缺乏持久的油相监测能力。本文报道了一种亲油性示踪支撑剂（ESP-T），通过乳液聚合将硬脂酸改性的纳米Fe₃O₄（nano-Fe₃O₄@SA）包覆于环氧树脂基体中。ESP-T圆球度超过0.9，在357.27 °C下保持结构完整，加入nano-Fe₃O₄@SA后水接触角从72.3°提升至104.6°，呈现出阻水亲油的传输特性。在30–120 °C下示踪剂释放遵循Korsmeyer–Peppas模型（R² > 0.90），扩散指数为0.45–0.85，表明Fick扩散与Case-II松弛协同作用。基于tanh平滑过渡的分段对流-弥散模型对单相突破曲线拟合R² = 0.9939，在稳态两相流条件下示踪剂通量可定量追踪油相产量。ESP-T因此将裂缝支撑与长期产量监测集于一体，为非常规储层管理提供了双功能平台。

**Keywords:** Unconventional oil and gas reservoirs; Hydraulic fracturing; Tracer proppant; Epoxy resin; Fe₃O₄ nanoparticles; Oil production monitoring; Release kinetics

**关键词：** 非常规油气藏；水力压裂；示踪支撑剂；环氧树脂；Fe₃O₄纳米颗粒；产油监测；释放动力学

---

## 1 Introduction

<a id="S002"></a>
**Source:** Section 1 ¶1

**Original:**
Sustained growth in global energy demand has positioned unconventional oil and gas resources at the center of contemporary petroleum development [1-5]. These resources now account for a more than 50% of the world's total hydrocarbon reserves [6,7], and their efficient development is critical to global energy security. Hydraulic fracturing, the core stimulation technology for unconventional reservoirs, creates artificial fractures that enhance hydrocarbon seepage pathways and substantially boost productivity in low-permeability and tight formations [8].

**中文:**
全球能源需求的持续增长已将非常规油气资源置于当代石油开发的核心位置[1-5]。这类资源目前占全球油气剩余可采储量50%以上[6,7]，其高效开发对全球能源安全至关重要。水力压裂作为非常规储层的核心增产技术，通过制造人工裂缝增强油气渗流通道，大幅提高低渗透和致密地层的产能[8]。

---

<a id="S003"></a>
**Source:** Section 1 ¶2

**Original:**
However, the oil production contribution of each fractured interval varies markedly post-stimulation, and interval productivity declines at varying rates as field development proceeds [9]. Accurate, per-interval production monitoring is therefore essential: it supplies the data needed for reservoir productivity assessment and guides subsequent development strategy optimization, ultimately improving the overall hydrocarbon recovery factor.

**中文:**
然而，压裂后各段产油贡献差异显著，且各段产量随开发推进以不同速率衰减[9]。因此，精确的分段产量监测至关重要：它提供储层产能评价所需数据，指导后续开发策略优化，最终提高整体油气采收率。

---

<a id="S004"></a>
**Source:** Section 1 ¶3

**Original:**
Conventional oil-soluble tracers suffer from poor compatibility with fracturing fluid injection and limited long-term monitoring capability [10-14]. Tracer proppants, composite materials that integrate fracture propping and tracer functions, address these limitations by immobilizing tracers within a solid carrier, enabling long-term dynamic monitoring upon co-injection with fracturing fluids and eliminating the need for separate tracer injection. Zhao et al. [15] coated rhodamine 6G onto polyvinyl alcohol-modified ceramic particles via solvent evaporation to retard aqueous release. Zhou et al. [16] encapsulated carbon quantum dots in polyvinyl alcohol-coated ceramic particles for controlled release. Malyavko et al. [17] employed monodisperse microspheres doped with fluorescent semiconductor nanocrystals functionalized with gas-philic, oleophilic, and hydrophilic polymer coatings to acquire phase-specific production data. Li et al. [18] encapsulated rare-earth element tracers with ammonium polymethacrylate to elucidate slow-release mechanisms. Gong et al. [19] embedded tracers into polystyrene (PS) microspheres via suspension polymerization and investigated their controlled-release behavior.

**中文:**
传统油溶性示踪剂与压裂液注入兼容性差，长期监测能力有限[10-14]。示踪支撑剂是将裂缝支撑与示踪功能集于一体的复合材料，通过将示踪剂固定于固体载体中，可在随压裂液共注入后实现长期动态监测，无需单独注入示踪剂。Zhao等人[15]通过溶剂蒸发将罗丹明6G涂覆于聚乙烯醇改性陶瓷颗粒表面以延缓水相释放。Zhou等人[16]将碳量子点包覆于聚乙烯醇涂层的陶瓷颗粒中实现控释。Malyavko等人[17]采用掺杂荧光半导体纳米晶的单分散微球，通过亲气、亲油和亲水聚合物涂层功能化以获取分相产量数据。Li等人[18]用聚甲基丙烯酸铵包覆稀土元素示踪剂阐明缓释机理。Gong等人[19]通过悬浮聚合将示踪剂嵌入聚苯乙烯(PS)微球中并研究其控释行为。

---

<a id="S005"></a>
**Source:** Section 1 ¶4 — **核心段落：指出研究空白 (Gap)**

**Original:**
Despite these advances, conventional coated tracer proppants face persistent challenges: high density impedes transport in fracturing fluids; monitoring ceases once the polymer coating dissolves; and pure PS microspheres exhibit inadequate mechanical strength and thermal stability [20-23]. Epoxy resin, a high-performance polymer with exceptional mechanical strength, thermal stability, and chemical resistance, offers a compelling alternative. Coating proppants with epoxy resin substantially reduces crush rate, improves compressive strength and acid resistance, and retains low-density advantages [24,25]. However, coating-based approaches remain constrained by uneven coverage, interfacial debonding risks, and complex multi-step preparation. Direct synthesis of epoxy resin microspheres as proppant matrices overcomes these limitations by enabling low-density tailoring, nanoparticle modification, and in-situ tracer encapsulation within a single synthetic step. Li et al. [26] explored the release of water-soluble tracers from epoxy resin in aqueous media. Wei et al. [27] encapsulated water-soluble tracers in epoxy matrices to locate water-producing intervals. However, the use of epoxy resin as an oleophilic release matrix for oil-phase production monitoring remains unexplored.

**中文:**
尽管取得了这些进展，传统涂层型示踪支撑剂仍面临持续挑战：高密度阻碍压裂液输送；聚合物涂层一旦溶解监测即终止；纯PS微球机械强度和热稳定性不足[20-23]。环氧树脂作为一种高性能聚合物，具有优异的机械强度、热稳定性和耐化学性，提供了有力的替代方案。用环氧树脂涂覆支撑剂可显著降低破碎率、提高抗压强度和耐酸性，并保持低密度优势[24,25]。然而，涂覆方法仍受限于覆盖不均匀、界面脱粘风险和多步骤制备复杂性。直接合成环氧树脂微球作为支撑剂基体，可在单步合成中实现低密度调控、纳米颗粒改性和原位示踪包覆，从而克服这些限制。Li等人[26]探索了水溶性示踪剂从环氧树脂中的水相释放。Wei等人[27]将水溶性示踪剂包覆于环氧基体中定位产水层段。**然而，将环氧树脂作为亲油性释放基体用于油相产量监测的研究尚未见报道。**

---

<a id="S006"></a>
**Source:** Section 1 ¶5 — **本文研究目标**

**Original:**
Here we address this gap by designing and synthesizing an oleophilic Fe₃O₄/epoxy resin tracer proppant (ESP-T). Using epoxy resin as the matrix and stearic acid-modified nano-Fe₃O₄@SA as the oleophilic tracer, we achieve stable tracer-carrier integration via emulsion polymerization. We systematically characterize the microstructure, mechanical properties, thermal stability, wettability, and oil-water permeability of ESP-T; investigate its temperature-dependent tracer release behavior and kinetic mechanisms; and validate its oil production monitoring accuracy through single-phase and two-phase core displacement experiments. This work aims to establish a multifunctional proppant platform that combines low-density suspendability, high compressive resistance, and reliable tracing performance for hydraulic fracturing stimulation and long-term productivity monitoring in unconventional reservoirs.

**中文:**
本文针对这一空白，设计并合成了一种亲油性Fe₃O₄/环氧树脂示踪支撑剂（ESP-T）。以环氧树脂为基体、硬脂酸改性的nano-Fe₃O₄@SA为亲油示踪剂，通过乳液聚合实现示踪剂-载体稳定结合。系统表征了ESP-T的微观结构、力学性能、热稳定性、润湿性及油水渗透性；研究了其温度依赖的示踪释放行为及动力学机制；并通过单相和两相岩心驱替实验验证了其产油监测精度。本工作旨在构建一种兼具低密度悬浮性、高抗压强度和可靠示踪性能的多功能支撑剂平台，用于非常规储层水力压裂增产和长期产量监测。

---

## 2 Experiments

<a id="S007"></a>
**Source:** Section 2.1 — Materials

**Original:**
All chemical reagents used in the experiments were of analytical grade or industrial grade and used without further purification. Analytical Grade (AR) reagents, including ethanol (purity ≥99.7%), ferric chloride (FeCl₃, purity ≥99.0%), ferrous chloride tetrahydrate (FeCl₂·4H₂O, purity ≥99.0%), manganese chloride hexahydrate (MnCl₂·6H₂O, purity ≥99.0%), stearic acid (purity ≥99.5%) and silicon dioxide (SiO₂, purity ≥99.99%), were purchased from Chengdu Kelong Chemical Co., Ltd. Industrial grade reagents included guar gum (purity 90%–95%), E51 epoxy resin, T31 curing agent, and hollow glass microspheres.

**中文:**
所有化学试剂均为分析纯或工业级，未经进一步纯化直接使用。分析纯试剂包括乙醇（纯度≥99.7%）、三氯化铁（FeCl₃，纯度≥99.0%）、四水氯化亚铁（FeCl₂·4H₂O，纯度≥99.0%）、六水氯化锰（MnCl₂·6H₂O，纯度≥99.0%）、硬脂酸（纯度≥99.5%）和二氧化硅（SiO₂，纯度≥99.99%），购自成都科龙化工有限公司。工业级试剂包括胍胶（纯度90%–95%）、E51环氧树脂、T31固化剂和空心玻璃微球。

---

<a id="S008"></a>
**Source:** Section 2.2 — Fabrication of nano-Fe₃O₄@SA

**Original:**
A clean three-necked flask was mounted in a thermostatic water bath and connected to nitrogen purge and mechanical stirring apparatuses. The flask was charged with 100 mL deionized water and heated to 80 °C. Upon reaching the target temperature, 2.703 g (0.01 mol) FeCl₃ was added, and the system was purged with nitrogen for 15 min, followed by the introduction of 1.15 g (0.058 mol) FeCl₂·4H₂O and 2×10⁻⁵ mol MnCl₂·6H₂O. After stirring for 10 min, 5.5 mL ammonia solution was rapidly added, and the reaction proceeded at pH 10 for 2 h. Upon completion, the resulting black suspension was transferred to an Erlenmeyer flask and magnetically separated, with the supernatant discarded. The precipitate was washed with anhydrous ethanol under sonication repeatedly until neutral pH, then collected. Finally, the precipitate was blended with an ethanolic stearic acid solution and subjected to sonication for oleophilic modification. After washing, the product was diluted to 100 mL and stored for subsequent use [28].

**中文:**
将洁净三口烧瓶安装于恒温水浴中，连接氮气吹扫和机械搅拌装置。加入100 mL去离子水，加热至80 °C。达到目标温度后加入2.703 g (0.01 mol) FeCl₃，氮气吹扫15 min，随后加入1.15 g (0.058 mol) FeCl₂·4H₂O和2×10⁻⁵ mol MnCl₂·6H₂O。搅拌10 min后迅速加入5.5 mL氨水，在pH 10条件下反应2 h。反应结束后将黑色悬浮液转移至锥形瓶进行磁分离，弃去上清液。沉淀用无水乙醇超声反复洗涤至中性pH后收集。最后将沉淀与硬脂酸乙醇溶液混合，超声进行亲油改性。洗涤后将产物稀释至100 mL，储存备用[28]。

> 📊 **Figure 2-1:** Schematic illustration for the preparation of stearic acid-modified metal-doped Fe₃O₄ nanoparticles *(Figure text only — visual asset not available from DOCX)*

---

<a id="S009"></a>
**Source:** Section 2.3 — Preparation of Epoxy Resin Microspheres and ESP-T

**Original:**
A SiO₂ aqueous dispersion was prepared by adding 0.3 g of 20 nm SiO₂ to 150 mL deionized water under stirring at 380 RPM. Separately, 0.9 g guar gum and 0.5 g of 45 μm SiO₂ were weighed. An epoxy pre-mixture consisting of 20 mL E51 epoxy resin, 6 g of Fe₃O₄-ethanol mixture, 1 g hollow glass microspheres, and 7 g T31 curing agent was homogenized by manual stirring for 3 min. The pre-mixture was transferred into the SiO₂ dispersion and agitated for 1 min to complete emulsification, followed by the addition of 45 μm SiO₂ and guar gum to stabilize the system. After microsphere formation, the product was cured at 50 °C for 1 h, rinsed with deionized water, and dried at 80 °C for 10 h. For pure epoxy microspheres, 6 g of pure ethanol replaced the Fe₃O₄-ethanol mixture and the guar gum dosage was 0.9 g.

**中文:**
将0.3 g 20 nm SiO₂加入150 mL去离子水中，在380 RPM搅拌下制备SiO₂水分散液。另称取0.9 g胍胶和0.5 g 45 μm SiO₂。将20 mL E51环氧树脂、6 g Fe₃O₄-乙醇混合物、1 g空心玻璃微球和7 g T31固化剂组成的环氧预混液手动搅拌3 min均化。将预混液转移至SiO₂分散液中搅拌1 min完成乳化，随后加入45 μm SiO₂和胍胶稳定体系。微球形成后将产物于50 °C固化1 h，去离子水冲洗，80 °C干燥10 h。纯环氧微球以6 g纯乙醇替代Fe₃O₄-乙醇混合物，胍胶用量为0.9 g。

> 📊 **Figure 2-2:** Schematic illustration for the preparation of Fe₃O₄-encapsulated epoxy resin proppants *(visual asset not available)*

---

<a id="S010"></a>
**Source:** Section 2.4 — Characterization Methods

**Original:**
The microstructure, elemental composition and distribution of neat epoxy resin microspheres and ESP-T were analyzed by scanning electron microscopy (SEM, ZEISS-Sigma 500). Samples were sputter-coated with a thin conductive metal layer under vacuum, mounted onto conductive adhesive tape, and observed at magnifications ranging from low power up to 50,000×. Characteristic X-rays were excited by a field-emission electron gun, and two-dimensional elemental mapping was performed over a selected region to visualize the distribution of Fe element in the proppants.

Surface morphology and particle dispersion were examined using an optical microscope (Leica DM2700P). Thermogravimetric analysis (TGA, TA Instruments Q500, USA) was conducted to evaluate the thermal stability of the two proppants. Tests were performed in an air atmosphere at a heating rate of 10 °C/min over 50–800 °C.

Water contact angle (WCA) measurements were carried out using a video optical contact angle analyzer (OCA20, Germany). Pressed proppant flakes were placed on the test stage, and a 5 μL droplet of deionized water was deposited onto the sample surface. Images were captured after droplet stabilization, and five replicate measurements were performed.

The physical and mechanical properties were comprehensively evaluated using roundness, sphericity, bulk density, apparent density, acid solubility, and crush rate. The oil–water conductivity of the proppants was indirectly assessed via filtration time: 2.0 g of proppant was loaded into a funnel blocked with 200-mesh screen, followed by 20 mL deionized water or dodecane, and the time required for complete permeation was recorded.

**中文:**
采用扫描电子显微镜（SEM，ZEISS-Sigma 500）分析纯环氧微球和ESP-T的微观结构、元素组成及分布。样品在真空下溅射镀导电金属膜，粘贴于导电胶带上，在低倍至50,000倍放大范围内观察。通过场发射电子枪激发特征X射线，在选定区域进行二维元素面扫描成像，可视化Fe元素在支撑剂中的分布。

采用光学显微镜（Leica DM2700P）观察两种支撑剂的表面形貌和颗粒分散性。热重分析（TGA，TA Instruments Q500，美国）在空气气氛中以10 °C/min升温速率、50–800 °C温度范围测试两种支撑剂的热稳定性。

水接触角（WCA）测量使用视频光学接触角分析仪（OCA20，德国）。将压制的支撑剂薄片置于测试台，滴加5 μL去离子水于样品表面，液滴稳定后采集图像，每个样品进行五次平行测量。

通过圆度、球度、体积密度、视密度、酸溶解度和破碎率综合评估支撑剂的物理力学性能及现场适用性。油-水导流能力通过过滤时间间接评价：将2.0 g支撑剂加入底部用200目筛网封堵的漏斗中，加入20 mL去离子水或十二烷，记录完全渗透所需时间。

---

<a id="S011"></a>
**Source:** Section 2.5 — Tracer Release Behavior

**Original:**
Glass vials containing 100 mL dodecane were placed in thermostatic oil baths set at 30 °C, 60 °C, 90 °C, and 120 °C, respectively, followed by the addition of 5 g of 40–70 mesh ESP-T. The vials were then hermetically sealed to prevent dodecane volatilization. Sampling was conducted at 12 h intervals, and the concentration of tracer-doped metal ions in the dodecane medium was quantified via inductively coupled plasma mass spectrometry (ICP-MS, PerkinElmer NexION 300X), from which the time-dependent tracer release curves were plotted.

**中文:**
将含100 mL十二烷的玻璃瓶分别置于设定为30 °C、60 °C、90 °C和120 °C的恒温油浴中，加入5 g 40–70目ESP-T。密封玻璃瓶以防十二烷挥发。每12 h取样，采用电感耦合等离子体质谱（ICP-MS，PerkinElmer NexION 300X）定量十二烷介质中掺杂金属示踪离子的浓度，绘制示踪剂释放时间曲线。

---

<a id="S012"></a>
**Source:** Section 2.6 — Oil Production Monitoring (Single-phase & Two-phase)

**Original:**
For single-phase monitoring: dodecane simulated crude oil. ESP-T was packed into a steel core, both ends sealed with 200-mesh screens, placed in a core holder with 5 MPa confining pressure. Dodecane was pumped at 5 mL/min until saturation, then shut in for 96 h for tracer release. Subsequently, dodecane was injected at 0.5 mL/min to displace the fluid, simulating oil production. Sampling was conducted at 4-min intervals (2 mL per sample, 20 sets total), with ICP-MS quantification.

For two-phase monitoring: dodecane and water were co-injected. Three oil–water ratios (4:1, 1:1, 1:4) and four total flow rates (0.1, 0.2, 0.3, 0.4 mL/min) were tested. Sampling at 5-min intervals (2 mL, 20 sets), recording the oil/water volume ratio and ICP-MS tracer concentration.

**中文:**
单相监测：十二烷模拟原油。将ESP-T填充于钢管中，两端以200目金属筛网密封，置于岩心夹持器中，施加5 MPa围压。以5 mL/min注入十二烷至饱和，然后闷井96 h使示踪剂充分释放。随后以0.5 mL/min注入十二烷驱替流体模拟产油。每4 min取样（2 mL/样，共20组），ICP-MS定量。

两相监测：十二烷与水共注入。测试三种油水体积比（4:1、1:1、1:4）和四种总两相流量（0.1、0.2、0.3、0.4 mL/min）。每5 min取样（2 mL，20组），记录油/水相体积比及ICP-MS示踪浓度。

> 📊 **Figure 2-4 & 2-5:** Schematic diagrams of single-phase and two-phase displacement apparatus *(visual assets not available)*

---

## 3 Results and Discussion

### 3.1 SEM Characterization

<a id="S013"></a>
**Source:** Section 3.1 ¶1 — SEM形貌

**Original:**
Figure 3-1 presents SEM micrographs of pure epoxy resin microspheres and ESP-T. At low magnification, both samples show excellent sphericity and high monodispersity, with uniform particle sizes and no inter-particle agglomeration, demonstrating the controllability of the suspension polymerization process. Well-formed spherical microspheres are reproducibly obtained both with and without nano-Fe₃O₄@SA incorporation. Comparing (a) and (d), pure epoxy microspheres feature a relatively smooth surface with minor particulate debris, whereas ESP-T microspheres exhibit a uniformly rough surface topography, confirming incorporation of the nanofiller and its pronounced effect on surface morphology.

**中文:**
图3-1展示了纯环氧微球和ESP-T的SEM图像。低倍下两种样品均呈现优异的球度和高单分散性，粒径均匀、无颗粒间团聚，证明了悬浮聚合过程的可控性。无论是否加入nano-Fe₃O₄@SA，均可重复获得形态良好的球形微球。对比(a)和(d)，纯环氧微球表面相对光滑、有少量颗粒碎屑，而ESP-T微球表面呈现均匀的粗糙形貌，证实了纳米填料的掺入及其对表面形貌的显著影响。

---

<a id="S014"></a>
**Source:** Section 3.1 ¶2 — 中倍形貌

**Original:**
At medium magnification, pure epoxy microspheres display subtle surface wrinkles and depressions, typical of thermosetting resins, arising primarily from volume shrinkage during epoxy curing. In contrast, ESP-T microspheres are uniformly covered with micro- and submicron-scale convex protrusions. These protrusions exist as well-dispersed island-like structures rather than large agglomerates, confirming that nano-Fe₃O₄@SA disperses as nanoclusters, not as individual nanoparticles, within the epoxy matrix. This morphology demonstrates that stearic acid surface modification effectively suppresses uncontrolled macroscopic phase separation, enabling nanoscale agglomeration with microscale uniformity.

**中文:**
中倍下，纯环氧微球呈现细微的表面褶皱和凹陷，这是热固性树脂的典型特征，主要源于环氧固化过程中的体积收缩。相比之下，ESP-T微球表面均匀覆盖微米和亚微米尺度的凸起结构。这些凸起以分散良好的岛状结构存在，而非大块团聚体，证实nano-Fe₃O₄@SA以纳米团簇形式（而非单颗粒）分散于环氧基体中。该形貌表明硬脂酸表面改性有效抑制了不可控的宏观相分离，实现了纳米尺度团聚与微米尺度均匀性的统一。

---

<a id="S015"></a>
**Source:** Section 3.1 ¶3 — 高倍形貌及界面结合

**Original:**
At high magnification, pure epoxy microspheres exhibit a dense yet undulating lava-like surface structure, a typical morphological feature of cross-linked epoxy polymer networks. In contrast, ESP-T microspheres display a debris-like surface structure, corresponding to stearic acid-wrapped nanoclusters. Notably, no distinct interfacial cracks are observed between these debris-like nanoclusters and the underlying epoxy matrix, with the nanofillers exhibiting an embedded bonding state rather than a simple surface-attached one. This observation indicates that the long alkyl chains of stearic acid form strong physical entanglement and hydrophobic interactions with epoxy resin molecular chains, yielding robust interfacial adhesion between the nanofillers and the epoxy matrix—direct evidence for the successful surface modification of the nanofiller.

**中文:**
高倍下，纯环氧微球呈现致密但起伏的熔岩状表面结构，这是交联环氧聚合物网络的典型形貌。相比之下，ESP-T微球呈现碎屑状表面结构，对应于硬脂酸包裹的纳米团簇。值得注意的是，这些碎屑状纳米团簇与底层环氧基体之间未观察到明显的界面裂缝，纳米填料呈现嵌入键合状态而非简单表面附着。这表明硬脂酸的长烷基链与环氧树脂分子链形成强物理缠结和疏水相互作用，在纳米填料与环氧基体之间产生坚固的界面粘合——这是纳米填料成功表面改性的直接证据。

---

<a id="S016"></a>
**Source:** Section 3.1 ¶4-5 — 形成机制推断与元素分布

**Original:**
These observations suggest the following formation mechanism: the hydrophobically modified nano-Fe₃O₄@SA nanoclusters are uniformly dispersed within epoxy resin droplets after emulsification; as the epoxy cross-linking reaction proceeds, a rigid polymer network forms and immobilizes the nanoclusters in place. During subsequent curing shrinkage, a portion of these nanoclusters is extruded toward the microsphere surface, producing the surface-enriched rough nanostructures. We note that this mechanism is inferred from post-cure microscopy and does not capture the real-time dynamics of nanocluster migration; in-situ characterization would be required to confirm the kinetic pathway.

SEM elemental mapping (Figure 3-2) visually illustrates the distribution of the primary Fe and Si elements within the proppant. The Fe elemental signal is dispersed throughout the entire proppant particle, demonstrating the presence of Fe-containing components in the particle's main matrix and serving as direct evidence for the successful encapsulation of nano-Fe₃O₄@SA within the epoxy resin matrix. Minor inhomogeneities in the Fe signal intensity across the particle indicate a slight non-uniformity in Fe distribution, attributed to distinct phase domains within the composite.

**中文:**
上述观察揭示了形成机制：疏水改性的nano-Fe₃O₄@SA纳米团簇在乳化后均匀分散于环氧树脂液滴中；随着环氧交联反应的进行，刚性聚合物网络形成并将纳米团簇固定在原位。在随后的固化收缩过程中，部分纳米团簇被挤出至微球表面，形成表面富集的粗糙纳米结构。需注意该机制基于固化后显微观察推断，未捕捉纳米团簇迁移的实时动力学过程；原位表征才能确认动力学路径。

SEM元素面扫描成像（图3-2）直观展示了主要Fe和Si元素在支撑剂中的分布。Fe元素信号遍布整个支撑剂颗粒，证明含Fe组分存在于颗粒主体基体中，是nano-Fe₃O₄@SA成功封装于环氧树脂基体中的直接证据。Fe信号强度在整个颗粒中的微小不均匀性表明复合物中存在明显相域导致的轻微Fe分布不均。

> 📊 **Figure 3-1:** SEM images of epoxy microspheres and ESP-T *(visual asset not available)*
> 📊 **Figure 3-2:** EDS Mapping images of Fe₃O₄@epoxy resin proppant *(visual asset not available)*

---

### 3.2 Thermal Stability

<a id="S017"></a>
**Source:** Section 3.2 — **关键性能数据**

**Original:**
As depicted in Figure 3-3, thermal analysis reveals three distinct decomposition stages. Stage 1 (50–350 °C): minor weight loss of 5.70%, attributed to removal of adsorbed surface water and residual ethanol. Stage 2 (350–400 °C): primary thermal decomposition, arising from cleavage of C–O–C and C–C bonds within the epoxy molecular chains and degradation of the cross-linked network. The DTG curve indicates a maximum weight-loss rate at 357.27 °C, with a mass loss of 72.5%. Stage 3 (>400 °C): residual mass stabilizes; remaining weight loss from oxidative combustion of carbonaceous residues. The final residue comprises hollow glass microspheres, thermally stable nano-Fe₃O₄@SA, and a minor carbonaceous fraction.

The DSC curve shows endothermic decomposition of the epoxy resin initiating at 332.41 °C, peaking at 357.27 °C, and completing at 371.58 °C. The total endothermic enthalpy of epoxy decomposition is 99.53 J/g.

The initial decomposition temperature of ESP-T is 357.27 °C, far higher than typical downhole oil–gas well temperatures (80–150 °C, up to 200 °C for deep wells), fully satisfying the thermal stability requirements for long‑term downhole service.

**中文:**
如图3-3，热分析揭示三个热分解阶段。第一阶段（50–350 °C）：微量失重5.70%，归因于吸附表面水和残余乙醇的脱除。第二阶段（350–400 °C）：主要热分解区，源自环氧分子链中C–O–C和C–C键断裂及交联网络降解。DTG曲线显示最大失重速率在357.27 °C，失重72.5%。第三阶段（>400 °C）：残余质量趋于稳定，剩余失重来自第二阶段的碳质残渣氧化燃烧。最终残渣包含空心玻璃微球、热稳定的nano-Fe₃O₄@SA及少量环氧分解碳质组分。

DSC曲线表征样品吸热和放热行为。环氧树脂分解的显著吸热峰起始于332.41 °C，峰值在357.27 °C（对应最大分解速率和最大吸热量），终止于371.58 °C。环氧分解总吸热焓为99.53 J/g。

ESP-T初始分解温度为357.27 °C，远高于典型油气井井下温度（80–150 °C，深井可达200 °C），完全满足长期井下服役的热稳定性要求。

> 📊 **Figure 3-3:** TGA/DTG and DSC curves *(visual asset not available)*

---

### 3.3 Water Contact Angle

<a id="S018"></a>
**Source:** Section 3.3 — **润湿性转变**

**Original:**
The average water contact angle of neat epoxy resin microspheres is 72.3°, indicative of a weakly hydrophilic surface (due to -OH groups on epoxy chains). In contrast, the average WCA of ESP-T reaches 104.6°, corresponding to a distinct hydrophobic surface—an increment of 32.3°. This transformation is attributed to the stearic acid modification: the carboxyl groups (-COOH) of stearic acid coordinate with surface hydroxyl groups of nano-Fe₃O₄@SA to form stable chemical bonds, while the long alkyl chains (-C₁₇H₃₅) orient outward from the epoxy matrix, constructing a hydrophobic film on the proppant surface. The surface enrichment of nano-Fe₃O₄@SA nanoclusters observed via SEM further enhances this hydrophobic effect through synergistic action of abundant hydrophobic alkyl chains drastically reducing surface free energy.

**中文:**
纯环氧微球平均水接触角为72.3°，表明弱亲水表面（环氧链上-OH基团与水分子形成氢键）。ESP-T平均WCA达到104.6°，呈现明显的疏水表面——提升了32.3°。该转变归因于硬脂酸改性：硬脂酸羧基(-COOH)与nano-Fe₃O₄@SA表面羟基配位形成稳定化学键，而长烷基链(-C₁₇H₃₅)向外定向排列，在支撑剂表面构建疏水膜。SEM观察到的nano-Fe₃O₄@SA纳米团簇表面富集通过丰富疏水烷基链的协同作用大幅降低表面自由能，进一步增强疏水效果。

> 📊 **Figure 3-4:** WCA comparison (72.3° → 104.6°) *(visual asset not available)*

---

### 3.4 Physical Properties

<a id="S019"></a>
**Source:** Section 3.4 — 密度与力学性能

**Original:**
The average bulk density and apparent density of pure epoxy microspheres are 0.6179 g/cm³ and 1.02 g/cm³; ESP-T are 0.646 g/cm³ and 1.072 g/cm³. Both proppants have bulk density lower than water (1 g/cm³), implying favorable suspension in water‑based fracturing fluids. ESP-T also meets key industry specifications: sphericity and roundness exceed 0.9 (Krumbien-Sloss chart [29]), acid solubility is 3.3% (≤ 5% standard), and the crush rate at 50 MPa is 2.9%, comparable to neat epoxy microspheres (2.6%).

**中文:**
纯环氧微球平均体积密度和视密度分别为0.6179 g/cm³和1.02 g/cm³；ESP-T分别为0.646 g/cm³和1.072 g/cm³。两种支撑剂体积密度均小于水（1 g/cm³），意味着可在水基压裂液中实现良好悬浮。ESP-T满足关键行业指标：球度和圆度超过0.9（Krumbien-Sloss图[29]），酸溶解度3.3%（≤5%标准），50 MPa下破碎率2.9%，与纯环氧微球（2.6%）相当。

---

### 3.5 Proppant Pack Conductivity (Oil-Water Permeability)

<a id="S020"></a>
**Source:** Section 3.5 — **阻水亲油的关键证据**

**Original:**
Proppant pack conductivity can be indirectly assessed via oil-water filtration time. The water filtration time of neat epoxy microspheres is 2 min 53 s, whereas that of ESP-T is 28 min 41 s. The hydrophobic surface of ESP-T impedes aqueous-phase spreading; water molecules must overcome the repulsive force of the hydrophobic surface, increasing flow resistance. Conversely, the oil filtration time of neat epoxy microspheres is 15 min 11 s versus 5 min 11 s for ESP-T. The hydrophobic surface is compatible with the oil phase, enabling rapid spreading within proppant pores and markedly reducing flow resistance. ESP-T thus exhibits a water-resistant, oil-permeable characteristic: in formations containing both phases, the proppant pack provides enhanced conductivity to oil, promoting rapid oil flow toward the wellbore, while the increased resistance to the aqueous phase helps mitigate water channeling and improve oil recovery.

**中文:**
通过油水过滤时间间接评估支撑剂充填层导流能力。纯环氧微球水过滤时间为2分53秒，而ESP-T为28分41秒。ESP-T的疏水表面阻碍水相铺展和流经粒间孔隙；水分子需克服疏水表面排斥力，增大流动阻力。相反，纯环氧微球油过滤时间为15分11秒，ESP-T仅为5分11秒。疏水表面与油相相容，使油在支撑剂孔隙内快速铺展，大幅降低流动阻力。ESP-T因此呈现阻水亲油特性：在含两相的地层中，支撑剂充填层为油提供增强导流能力促进油流向井筒，同时增加水相阻力有助于缓解水窜、提高原油采收率。



**Table 3-1 关键对比数据:**
| 指标 | ESP-T | 纯环氧微球 |
|------|-------|------------|
| 水通过时间 | 28分41秒 | 2分53秒 |
| 油通过时间 | 5分11秒 | 15分11秒 |

---

### 3.6 Tracer Release Behavior

<a id="S021"></a>
**Source:** Section 3.6 — 释放动力学 (K-P模型)

**Original:**
The release profiles at various temperatures are presented in Figure 3-7. The relative release concentration increases over time and with rising temperature, demonstrating that elevated temperature accelerates tracer release. The cumulative tracer release at 120 °C over 14 days remains detectable by ICP-MS, confirming its suitability for long-term stable monitoring.

The Korsmeyer–Peppas (K-P) model was used to fit the release curves: C/C₀ = K·tⁿ. For spherical carriers, n ≤ 0.43 = Fickian diffusion; 0.43 < n < 0.85 = anomalous transport (co-governed); n ≥ 0.85 = Case-II relaxation.

Fitting results (Table 3-2): n values all fall within 0.45–0.85 (30°C: 0.598, 60°C: 0.666, 90°C: 0.568, 120°C: 0.556), confirming anomalous transport governed by synergistic Fickian diffusion and Case-II relaxation. K increases systematically with temperature (0.055→0.196). R² > 0.94 for all temperatures. The model should not be extrapolated beyond the experimental timeframe (0-14 days).

**中文:**
不同温度释放曲线如图3-7所示。相对释放浓度随时间推移和温度升高而增大，表明升温加速示踪释放。120 °C下14天累积释放仍可被ICP-MS检出，确认其适用于长期稳定监测。

采用Korsmeyer–Peppas (K-P)模型拟合释放曲线：C/C₀=K·tⁿ。球形载体中n≤0.43为Fick扩散控制；0.43<n<0.85为非Fick异常传输（两种机制共同控制）；n≥0.85为Case-II松弛控制。

拟合结果（表3-2）：各温度n值均在0.45–0.85范围内（30°C: 0.598, 60°C: 0.666, 90°C: 0.568, 120°C: 0.556），确认异常传输机制——Fick扩散与Case-II松弛协同主导。K值随温度升高系统递增（0.055→0.196）。各温度R²均超过0.94。模型不应外推至实验时间范围外（0-14天）。



**Table 3-2 K-P模型拟合参数:**
| Temperature | R² | K | n |
|-------------|-----|--------|--------|
| 30°C | 0.9549 | 0.0554 | 0.5983 |
| 60°C | 0.9649 | 0.0818 | 0.6665 |
| 90°C | 0.9560 | 0.1134 | 0.5684 |
| 120°C | 0.9454 | 0.1964 | 0.5557 |

> 📊 **Figure 3-7:** Release curves and K-P model fitting *(visual asset not available)*

---

### 3.7 Oil Production Monitoring — **论文核心亮点**

<a id="S022"></a>
**Source:** Section 3.7 ¶1 — 单相流突破曲线

**Original:**
The tracer breakthrough curve was fitted using a piecewise advection–dispersion model with smooth tanh transition:

C(t) = cb + A·C_rise(t) + a·C_fall(t)

where C_rise captures the advective-dispersive transport of the tracer slug from the shut-in period (Gaussian form from ADE instantaneous slug injection solution), and C_fall describes the sustained release of residual nano-Fe₃O₄@SA from the epoxy matrix (erfc tail from ADE continuous-source solution). The two regimes are blended via tanh weighting, producing a smooth, physically continuous breakthrough curve.

**中文:**
采用基于tanh平滑过渡的分段对流-弥散模型拟合示踪突破曲线：

C(t) = cb + A·C_rise(t) + a·C_fall(t)

其中C_rise捕捉关井期间示踪剂团的对流-弥散传输（ADE瞬时脉冲解的Gaussian形式），C_fall描述残余nano-Fe₃O₄@SA从环氧基体中的持续释放（ADE连续源解的erfc拖尾）。两阶段通过tanh权重函数平滑过渡，生成物理连续的突破曲线。

---

<a id="S023"></a>
**Source:** Section 3.7 ¶2 — **模型拟合核心数据 (⭐汇报重点)**

**Original:**
The fitted curve is shown in Figure 3-8(b) and the fitted parameters are listed in Table 3-3. The model achieves R² = 0.9939 and RMSE = 0.0210, with residuals randomly distributed within ±2σ across the full time range. The fitted flow rate (0.46 mL·min⁻¹) agrees closely with the pump-set rate (0.5 mL·min⁻¹), relative error 8%; and the mean residence time (MRT = 37.4 min) matches the convective travel time (x/v = 38.6 min, ratio 0.967). The Peclet number Pe = x/α = 0.934 (≈1) indicates a transitional transport regime in which advection and dispersion are comparable, consistent with the gradual release expected from a matrix-diffusion-controlled source. Integration of the fitted C_rise and C_fall components separately over the experimental duration shows that **47% of the integrated tracer signal originates from the erfc tailing component**. This dominant contribution of sustained matrix-diffusion-controlled release—nearly half the total detected signal—provides quantitative confirmation that the non-Fickian mechanism identified in Section 3.6 governs tracer transport under flow conditions.

**中文:**
拟合曲线见图3-8(b)，拟合参数见表3-3。模型R² = 0.9939，RMSE = 0.0210，全时间范围内残差随机分布于±2σ以内。拟合流量（0.46 mL·min⁻¹）与泵设流量（0.5 mL·min⁻¹）吻合良好（相对误差8%）；平均停留时间（MRT = 37.4 min）与对流传输时间（x/v = 38.6 min，比值0.967）一致。Peclet数Pe = x/α = 0.934（≈1），表明过渡传输状态——对流与弥散相当，与基质扩散控制源预期的渐进释放一致。对拟合C_rise和C_fall分量分别积分得出：**erfc拖尾分量贡献了总示踪信号的47%**。这种基质扩散控制持续释放的主导贡献——几乎占检测总信号的一半——定量证实了第3.6节中识别的非Fick机制在流动条件下主导示踪传输，为ESP-T长期产量监测建立了物理基础。



**Table 3-3 分段ADE模型拟合参数与推导传输性质:**
| 参数 | 数值 | 单位 |
|------|------|------|
| R² | 0.9939 | — |
| RMSE | 0.0210 | — |
| 拟合流量 Q | 0.46 | mL·min⁻¹ |
| 泵设流量 | 0.50 | mL·min⁻¹ |
| 平均流速 v | 2.59 | cm·min⁻¹ |
| 纵向弥散度 α | 107.1 | cm |
| 平均停留时间 MRT | 37.4 | min |
| 对流传输时间 x/v | 38.6 | min |
| Erfc拖尾信号占比 | 47 | % |

---

<a id="S024"></a>
**Source:** Section 3.7 ¶3 — 两相流监测

**Original:**
During steady-state two-phase production, tracer concentration decreases with increasing total two-phase flow rate (dilution effect), with negligible dependence on oil-water ratio (OWR). To quantify the single-interval oil flow rate, tracer flux (FO) was introduced — the mass of tracer passing through the wellhead sampling point per unit time.

Figure 3-9(b) shows that FO increases with OWR but is independent of total two-phase flow rate. At constant OWR, contact area between ESP-T and oil remains unchanged → FO stays constant. Increasing OWR expands oil-phase contact area → higher FO.

Figure 3-9(c) compares normalized FO with actual oil-phase flow rate at different OWRs. The normalized FO was calibrated against steady-state FO during single-phase oil displacement (3.187 μg/min). The results demonstrate close agreement between FO and actual oil-phase flow rate across all OWRs tested. Thus, under steady-state two-phase flow conditions, the oil-phase flow rate in the labeled interval can be quantified from the FO variation curve when total two-phase flow rate is constant.

**中文:**
稳态两相生产期间，示踪剂浓度随总两相流量增大而降低（稀释效应），与油水比关系不大。为量化单段油相流量，引入示踪剂通量FO——单位时间通过井口采样点的示踪剂质量。

图3-9(b)显示FO随油水比增加而增大，但与总两相流量无关。恒定油水比下ESP-T与油相接触面积不变→FO保持恒定。增大油水比→扩大油相接触面积→FO升高。

图3-9(c)对比了不同油水比下归一化FO与实际油相流量（以单相油驱替稳态FO=3.187 μg/min标定）。结果证明在各测试油水比下FO与实际油相流量高度吻合。因此，在稳态两相流条件下，恒定总两相流量时可通过FO变化曲线量化标记层段的油相流量。

---

<a id="S025"></a>
**Source:** Section 3.7 ¶4 — **局限性说明 (局限性/Limitations)**

**Original:**
Several limitations should be noted. First, the piecewise ADE model assumes a single fractured interval and uniform proppant-pack properties; multi-interval interactions and pack heterogeneity may introduce deviations in field applications. Second, the tracer flux calibration relies on steady-state flow; during transient flow regimes (e.g., well start-up, shut-in, or rapid drawdown), the relationship between FO and oil-phase flow rate may not hold. Third, the laboratory-scale validation used dodecane as a model oil; crude oil compositional effects (asphaltene adsorption, viscosity variation) on tracer release kinetics require further investigation. Fourth, at temperatures exceeding 120 °C or in the presence of aggressive formation fluids (high salinity, CO₂, H₂S), the long-term chemical stability of the epoxy matrix and the integrity of stearic acid surface modification warrant additional evaluation. These limitations delineate the current applicability envelope.

**中文:**
需注意以下局限性：第一，分段ADE模型假设单裂缝段及均匀支撑剂充填层性质；多段相互作用及充填层非均质性在矿场应用中可能带来偏差。第二，示踪剂通量标定依赖稳态流动；在瞬变流态下（如开井、关井或快速降压），FO与油相流量之间的关系可能不成立。第三，实验室验证使用十二烷作为模型油；原油组分效应（沥青质吸附、粘度变化）对示踪剂释放动力学的影响需进一步研究。第四，在超过120 °C或存在强腐蚀性地层流体（高矿化度、CO₂、H₂S）的条件下，环氧基体的长期化学稳定性及硬脂酸表面改性的完整性需要额外评估。这些局限性界定了当前适用性范围。

> 📊 **Figure 3-8:** Tracer breakthrough curves and model fitting *(visual asset not available)*
> 📊 **Figure 3-9:** Two-phase flow monitoring results *(visual asset not available)*

---

## 4 Conclusions

<a id="S026"></a>
**Source:** Section 4 ¶1 — 合成与形貌

**Original:**
We synthesized oleophilic nano-Fe₃O₄@SA nanoparticles via coprecipitation with stearic acid modification and fabricated ESP-T via emulsion polymerization. SEM, elemental mapping, and optical microscopy confirmed uniform dispersion of nano-Fe₃O₄@SA as nanoclusters within the epoxy matrix. ESP-T exhibits sphericity and roundness exceeding 0.9, meeting industrial proppant molding standards.

**中文:**
通过共沉淀-硬脂酸改性合成了亲油性nano-Fe₃O₄@SA纳米颗粒，并通过乳液聚合制备了ESP-T。SEM、元素面扫描和光学显微镜证实nano-Fe₃O₄@SA以纳米团簇形式均匀分散于环氧基体中。ESP-T球度和圆度超过0.9，满足工业支撑剂成型标准。

---

<a id="S027"></a>
**Source:** Section 4 ¶2 — 物理力学热性能

**Original:**
ESP-T demonstrates strong physical, mechanical, and thermal performance: bulk density of 0.646 g·cm⁻³ for favorable suspension; apparent density of 1.072 g·cm⁻³ indicating compact internal packing; crush rate of 2.9% at 50 MPa; acid solubility of 3.3% (≤ 5% standard); and an initial decomposition temperature of 357.27 °C, far exceeding typical downhole conditions (80–200 °C). The water contact angle increases from 72.3° to 104.6°, and the oil filtration time of 5 min 11 s is 66.1% shorter than that of pure epoxy microspheres, validating the water-resistant, oil-permeable transport characteristic.

**中文:**
ESP-T展现出优异的物理、力学和热性能：体积密度0.646 g·cm⁻³有利于悬浮；视密度1.072 g·cm⁻³表明致密内部填充；50 MPa破碎率2.9%；酸溶解度3.3%（≤5%标准）；初始分解温度357.27 °C远超典型井下条件（80–200 °C）。水接触角从72.3°增至104.6°，油过滤时间5分11秒比纯环氧微球缩短66.1%，验证了阻水亲油的传输特性。

---

<a id="S028"></a>
**Source:** Section 4 ¶3 — 释放动力学与监测模型

**Original:**
Tracer release from ESP-T at 30–120 °C follows the Korsmeyer–Peppas model (R² > 0.90; diffusion exponent n = 0.45–0.85), governed by synergistic Fickian diffusion and Case-II relaxation. Cumulative Fe release at 120 °C exceeds 2.0 mg·L⁻¹ over 14 days, meeting ICP-MS detection limits. A piecewise advection–dispersion model with smooth tanh transition achieves R² = 0.9939; the fitted flow rate (0.46 mL·min⁻¹) closely matches the pump-set rate (0.5 mL·min⁻¹, relative error 8%); MRT (37.4 min) agrees with convective travel time (38.6 min, ratio 0.967). The erfc tailing component accounts for **47%** of the integrated tracer signal, confirming matrix-diffusion-controlled release as the dominant mechanism sustaining long-term monitoring. Under steady-state two-phase flow, tracer flux effectively quantifies per-interval oil-phase production rates across varying OWRs.

**中文:**
ESP-T在30–120 °C下的示踪释放遵循Korsmeyer–Peppas模型（R²>0.90；扩散指数n=0.45–0.85），由Fick扩散与Case-II松弛协同主导。120 °C下14天Fe累积释放超过2.0 mg·L⁻¹，满足ICP-MS检测限。基于tanh平滑过渡的分段对流-弥散模型R²=0.9939；拟合流量（0.46 mL·min⁻¹）与泵设流量（0.5 mL·min⁻¹）高度吻合（相对误差8%）；MRT（37.4 min）与对流传输时间（38.6 min，比值0.967）一致。erfc拖尾分量贡献**47%**的总示踪信号，确认基质扩散控制释放是维持长期监测的主导机制。在稳态两相流条件下，示踪剂通量可有效量化不同油水比下各段产油量。

---

<a id="S029"></a>
**Source:** Section 4 ¶4 — 总结与展望

**Original:**
In summary, ESP-T integrates fracture propping and long-term production monitoring into a single proppant material, suitable for acid fracturing, deep-well, and high-pressure applications. The combination of favorable mechanical properties, thermal stability, and reliable tracer performance makes ESP-T a promising platform for optimizing stimulation strategies and enhancing oil recovery in unconventional reservoirs. We emphasize that the current validation is limited to laboratory-scale single-interval experiments with model fluids; field-scale trials under multi-interval, multiphase conditions are necessary to establish the operational reliability and economic viability of ESP-T-based production monitoring.

**中文:**
总而言之，ESP-T将裂缝支撑与长期产量监测集成于单一支撑剂材料，适用于酸化压裂、深井和高压应用。优异的力学性能、热稳定性与可靠示踪性能的结合，使ESP-T成为优化增产策略、提高非常规储层原油采收率的潜力平台。我们强调当前验证仅限于实验室规模单段实验与模型流体；需要在多段、多相条件下开展矿场规模试验，以确立ESP-T-based产量监测的作业可靠性和经济可行性。

---

## References

完整参考文献列表 (共29篇)，包括 Chong 2016 [1], Montgomery 2005 [2], IEA 2024 [6], Barati 2014 [8], Zhao 2020 [15], Zhou 2022 [16], Gong 2024 [19], Li 2023 [18] 等。

---

## 术语表 (Terminology Table)

| English Term | 中文术语 | Notes |
|-------------|---------|-------|
| ESP-T | 亲油性示踪支撑剂 | Epoxy resin microSpheres with oleophilic Tracer |
| nano-Fe₃O₄@SA | 硬脂酸改性纳米四氧化三铁 | Stearic acid-modified nano-Fe₃O₄ |
| Korsmeyer–Peppas model | K-P释放动力学模型 | Power-law release model |
| Fickian diffusion | Fick扩散 | Concentration-gradient-driven transport |
| Case-II relaxation | Case-II松弛 | Polymer swelling-driven release |
| Anomalous transport | 非Fick异常传输 | n = 0.45–0.85 |
| ADE | 对流-弥散方程 | Advection-Dispersion Equation |
| tanh blending | tanh平滑过渡 | Hyperbolic tangent weighting function |
| Peclet number | Peclet数 | Advection/dispersion ratio |
| MRT | 平均停留时间 | Mean Residence Time |
| WCA | 水接触角 | Water Contact Angle |
| OWR | 油水比 | Oil-Water Ratio |
| FO | 示踪剂通量 | Tracer flux (mass/time) |
| ICP-MS | 电感耦合等离子体质谱 | Inductively Coupled Plasma Mass Spectrometry |

---

## 汇报要点 (Critical Reading Notes)

### 论文亮点 (Strengths)
1. **明确的创新空白**：首次将环氧树脂作为亲油性释放基体用于油相产量监测（S005-S006）
2. **"阻水亲油"设计**：WCA从72.3°→104.6°，油通过时间缩短66%，物理原理清晰（S018, S020）
3. **ADE分段模型R²=0.9939**：拟合精度极高，且有物理意义（erfc拖尾占47%信号）（S023）
4. **完整的材料-释放-监测链条**：从材料合成→释放动力学→现场模拟验证，逻辑自洽

### 关键数据 (Key Numbers for Presentation)
- 357.27 °C — 初始分解温度（远超井下需求）
- 104.6° — 水接触角（疏水）
- 0.646 g/cm³ — 体积密度（<水，可悬浮）
- n = 0.45–0.85 — 非Fick异常传输
- R² = 0.9939 — ADE模型拟合精度
- **47%** — erfc拖尾信号占比（长期监测的物理基础）

### 汇报时需主动提出的局限 (Limitations to Discuss)
1. 单段假设 → 多段矿场需验证
2. 稳态假设 → 瞬变工况不适用
3. 十二烷模拟油 → 真实原油影响未知
4. >120 °C / 腐蚀流体 → 长期稳定性待评
5. 形成机制为SEM推断 → 缺乏原位表征

### 导师可能追问 (Anticipated Questions)
- "成本/工业化可行性？"
- "与Gong 2024的PS微球相比具体优势？"
- "Mn掺杂的作用是什么？"
- "矿场试验计划？"
- "47%的erfc贡献 — 这是好是坏？"（答：证明了长期监测的物理基础，但暗示了信号持续释放对即时检测的挑战）