# create_construction_reference_final.py
# Creates an Excel workbook with two sheets: Arabic and English construction reference tables.
# Usage:
#   pip install pandas openpyxl
#   python create_construction_reference_final.py

from pathlib import Path
import pandas as pd

out_path = Path("construction_reference_final.xlsx")

# Arabic rows: [Category, ItemKey, ItemName_ar, CSI_Division, TypicalActivities, DefaultUnit, DefaultDepth, Notes]
arabic_rows = [
    # Concrete works
    ["أعمال الخرسانة","CONC_FOOT_ISO_PLAIN","قواعد منفصلة - عادية","Division 03 — Cast-in-Place Concrete (03 30)",
     "شدة بسيطة، صب الخرسانة، اهتزاز، معالجة/curing","م³","400-600 mm",""],
    ["أعمال الخرسانة","CONC_FOOT_ISO_REINF","قواعد منفصلة - مسلحة","Division 03 — 03 10 / 03 20 / 03 30",
     "قوالب قواعد، تسليح (مشاة/قضبان)، وصب، معالجة","م³","600-1000 mm",""],
    ["أعمال الخرسانة","CONC_FOOT_STRIP_PLAIN","قواعد شريطية - عادية","Division 03 — Cast-in-Place Concrete (03 30)",
     "قوالب شرائط، صب متواصل، تشبيكات وصلات","م³","حسب المقطع",""],
    ["أعمال الخرسانة","CONC_FOOT_STRIP_REINF","قواعد شريطية - مسلحة","Division 03 — 03 10 / 03 20 / 03 30",
     "قوالب، سلال تسليح شرائطي، رباطات، صب","م³","حسب التصميم",""],
    ["أعمال الخرسانة","CONC_RAFT_PLAIN","لبشة - عادية","Division 03 — Cast-in-Place Concrete (03 30)",
     "شدة حواف، صب لبشة كبيرة، تقسيم مجزأ ومفاصل","م² / م³","300-600 mm",""],
    ["أعمال الخرسانة","CONC_RAFT_REINF","لبشة - مسلحة","Division 03 — 03 10 / 03 20 / 03 30",
     "شبكات تسليح علوية وسفلية، دعامات، صب متدرج، معالجة","م² / م³","300-600 mm",""],
    ["أعمال الخرسانة","CONC_TIE_BEAM","سملات / كمرات أرضية","Division 03 — Cast-in-Place Concrete (03 30)",
     "قوالب كمرات، تسليح رئيسي واغلاق، صب وربط بالقواعد","RM / م³","حسب التصميم",""],
    ["أعمال الخرسانة","CONC_COLUMN","أعمدة خرسانية","Division 03 — 03 10 / 03 20 / 03 30",
     "قوالب أعمدة، قضبان رأسية، تقوية وصلات، صب وتجهيز رأس العمود","Each","ارتفاع حسب التصميم",""],
    ["أعمال الخرسانة","CONC_SLAB_GRADE","بلاطة على التربة (Slab on grade)","Division 03 — Cast-in-Place Concrete (03 30)",
     "إعداد قاعدة، قوالب حواف، شبك تسليح، حواجز بخار، صب وتسوية","م² / م³","120-200 mm",""],
    ["أعمال الخرسانة","CONC_SLAB_SUSP","بلاطات أدوار (Suspended slabs)","Division 03 — Cast-in-Place Concrete (03 30)",
     "شدة مؤقتة ودعائم، تسليح شبكي/قضبان، صب، مفاصل تحكم، معالجة","م² / م³","سماكة حسب التصميم",""],
    ["أعمال الخرسانة","CONC_FORMWORK_GEN","شدة عامة (Formwork)","Division 03 — 03 10 00",
     "توريد وتركيب القوالب (خشب/فولاذ)، الدعامات، إزالة الشدة بحسب الترتيب","م² / count","",""],
    ["أعمال الخرسانة","CONC_REINF_GEN","تسليح عامة (Reinforcing)","Division 03 — 03 20 00",
     "توريد وتثبيت حديد التسليح، قطع/ثني، كراسي دعم، تلاحم وشدات ربط","KG / TON","",""],
    ["أعمال الخرسانة","CONC_CAST_GEN","صب وخرسانة (Casting & Curing)","Division 03 — 03 30 00",
     "توريد الخرسانة، ضخ/نقل، اهتزاز، تشطيب، معالجة وعلاج (curing)","م³","",""],
    # Earthworks
    ["الأعمال الترابية","EARTH_TOPSOIL","تجريف / إزالة طبقة سطحية","Division 02 — Site Work",
     "إزالة الطبقة العضوية، تخزين مؤقت (stockpile)، حماية عناصر الموقع","م³ / م²","",""],
    ["الأعمال الترابية","EARTH_EXCAV","حفر للقواعد","Division 02 — Excavation & Trenching",
     "حفر كتل أو خنادق، سحب التربة، تسوية منحدرات، نقل مخلفات","م³","",""],
    ["الأعمال الترابية","EARTH_SHORING","سند جوانب الحفر (Shoring)","Division 02 — Temporary shoring",
     "تركيب sheet piles، soldier piles، دعم خشبي/حديدي، braces","assembly","",""],
    ["الأعمال الترابية","EARTH_BACKFILL","ردم ودمك (Backfill & Compaction)","Division 02 — Backfill",
     "ردم طبقات من التربة أو مواد مرخصة، دمك بالطبقات واجراء اختبارات Compaction","م³","",""],
    ["الأعمال الترابية","EARTH_GRADING","تسوية / Grading","Division 02 — Grading",
     "تسوية الموقع، توازن قطع/ردم، proof roll والتنعيم النهائي","م² / م³","",""],
    # Dewatering
    ["أعمال النزح","DEWATER_SURF","نزح سطحي (Surface drainage)","Division 02 / 33 — Site utilities",
     "قنوات مؤقتة، مدخلات تحويل مياه، حفر مصارف مؤقتة، برك ترسيب","LM / م²","",""],
    ["أعمال النزح","DEWATER_SUB","نزح جوفي (Dewatering)","Division 02 — Dewatering systems",
     "نظام wellpoint، دوامات تجميع (sumps)، مضخات، تصريف لمواقع ترسيب","system / day","",""],
    ["أعمال النزح","DEWATER_STORM","شبكات تصريف مياه الأمطار","Division 33",
     "مد مواسير تصريف، فتحات manhole، نقاط تصريف، وصلات بالمجاري","RM / manhole","",""],
    # Waterproofing
    ["أعمال العزل","WATER_FOUND","عزل قواعد (Foundation waterproofing)","Division 07 — Waterproofing",
     "طبقات بيتومين torch-on، طلاءات اسمنتية، صفائح بنتونيت، لوح حماية","م²","",""],
    ["أعمال العزل","WATER_WETAREA","عزل الحمامات (Wet area waterproofing)","Division 07 — Waterproofing",
     "مستحضرات سائلة، شرائح عزل تحت البلاط، pond test","م²","",""],
    ["أعمال العزل","WATER_ROOF","عزل الأسطح (Roof waterproofing)","Division 07 — Roofing",
     "أنظمة torch-on أو single-ply أو سائل PU، تنظيم ميل وتصريف","م²","",""],
    ["أعمال العزل","WATER_POOL","عزل خزانات/أحواض (Tanking / Pools)","Division 07 / 03",
     "تغليف بالبطانة، طلاءات إيبوكسية، طلاءات اسمنتية مرنة","م²","",""],
    # Finishes
    ["التشطيبات","FIN_PLASTER","محارة داخلية/خارجية (Plaster / Render)","Division 09 — Plaster & Gypsum",
     "طبقة أولية وخاتمة، تسوية، صنفرة وتجهيز للدهان","م²","10-20 mm",""],
    ["التشطيبات","FIN_PAINT","دهانات داخلية","Division 09 — Painting",
     "برايمر، معجون، طبقتين نهائيتين، تجفيف وفحص الجودة","م²","",""],
    ["التشطيبات","FIN_TILE","بلاط سيراميك/بورسلان (Tiling)","Division 09 — Tiling",
     "إعداد السطح، لاصق بلاط، تركيب، حشوات وتساوي","م²","",""],
    ["التشطيبات","FIN_STONE","رخام/جرانيت (Stone finishes)","Division 09 — Stone",
     "قص وتركيب، تلميع، حشوات مفاصل ومثبتات خاصة","م²","",""],
    ["التشطيبات","FIN_FLOOR_WOOD","أرضيات خشبية / باركيه","Division 09 — Wood Flooring",
     "تحضير الأرضية، تركيب لامينيت/باركيه بنظام لاصق أو عائم","م²","",""],
    # Supplementary/Ceilings
    ["أعمال تكميلية","CEIL_SUSP_GYP","أسقف معلقة جبسون / شبكة","Division 09 — Ceilings",
     "تركيب هيكل معلق، قضبان تعليق، بلاطات جبس/لوحات، فتحات وصول","م²","",""],
    ["أعمال تكميلية","CEIL_ACOUSTIC","أسقف مستعارة صوتية","Division 09 — Ceilings",
     "شبكة تعليق، تركيب بلاطات عازلة صوتية، تشطيب الحواف","م²","",""],
    # Plumbing
    ["السباكة","PLUMB_WATER","تمديدات مياه باردة/ساخنة","Division 22 — Plumbing",
     "مد مواسير PVC/Cu/PEX، صمامات، وصلات، اختبار ضغط","RM","",""],
    ["السباكة","PLUMB_SAN","صرف صحي داخلي","Division 22 — Sanitary Piping",
     "أكوام صرف، فخاخ، فتحات تهوية، وصل للصرف الخارجي","RM / fixture","",""],
    ["السباكة","PLUMB_STORM_EXT","شبكات تصريف خارجية","Division 33 / 22",
     "قنوات صرف، manholes، مواسير أمطار، توصيل لنظام الصرف العام","RM / manhole","",""],
    ["السباكة","PLUMB_FIX","تجهيزات صحية (Fixtures)","Division 22 — Plumbing Fixtures",
     "تركيب أحواض، مراحيض، شاور، إحكام مانع للتسريب، اختبار","each","",""]
]

# English rows: [Category, ItemKey, ItemName_en, CSI_Division, TypicalActivities, DefaultUnit, DefaultDepth, Notes]
english_rows = [
    # Concrete works
    ["Concrete works","CONC_FOOT_ISO_PLAIN","Isolated footings - plain","Division 03 — Cast-in-Place Concrete (03 30)",
     "Simple pad formwork, concrete placement, vibration, curing","CUM","400-600 mm",""],
    ["Concrete works","CONC_FOOT_ISO_REINF","Isolated footings - reinforced","Division 03 — 03 10 / 03 20 / 03 30",
     "Footing formwork, reinforcement mats / bars, concrete placement, curing","CUM","600-1000 mm",""],
    ["Concrete works","CONC_FOOT_STRIP_PLAIN","Strip footings - plain","Division 03 — Cast-in-Place Concrete (03 30)",
     "Continuous strip formwork, continuous pour, jointing","CUM","Varies (section)",""],
    ["Concrete works","CONC_FOOT_STRIP_REINF","Strip footings - reinforced","Division 03 — 03 10 / 03 20 / 03 30",
     "Formwork, strip reinforcement cages, staged casting if needed","CUM","Varies",""],
    ["Concrete works","CONC_RAFT_PLAIN","Raft / Mat foundation - plain","Division 03 — Cast-in-Place Concrete (03 30)",
     "Edge formwork, large slab pour, joints and cutting","SQM / CUM","300-600 mm",""],
    ["Concrete works","CONC_RAFT_REINF","Raft / Mat foundation - reinforced","Division 03 — 03 10 / 03 20 / 03 30",
     "Top & bottom reinforcement mats, staged casting, curing","SQM / CUM","300-600 mm",""],
    ["Concrete works","CONC_TIE_BEAM","Tie beams / Ground beams","Division 03 — Cast-in-Place Concrete (03 30)",
     "Beam formwork, stirrups & main bars, cast and tie to footings","RM / CUM","Depth per design",""],
    ["Concrete works","CONC_COLUMN","Concrete columns","Division 03 — 03 10 / 03 20 / 03 30",
     "Column formwork, vertical reinforcement, casting, base connections","Each","Height per design",""],
    ["Concrete works","CONC_SLAB_GRADE","Slab on grade","Division 03 — Cast-in-Place Concrete (03 30)",
     "Edge forms, mesh reinforcement, vapor barrier, pour & finishing","SQM / CUM","120-200 mm",""],
    ["Concrete works","CONC_SLAB_SUSP","Suspended floor slabs","Division 03 — Cast-in-Place Concrete (03 30)",
     "Formwork + props, reinforcement, curing, control joints","SQM / CUM","Thickness per design",""],
    ["Concrete works","CONC_FORMWORK_GEN","Formwork - general","Division 03 — 03 10 00",
     "Supply & install plywood/steel forms, shoring, stripping sequence","SQM / count","",""],
    ["Concrete works","CONC_REINF_GEN","Reinforcing - general","Division 03 — 03 20 00",
     "Supply & fixing of rebar, cutting / bending, chairs, lapping","KG / TON","",""],
    ["Concrete works","CONC_CAST_GEN","Casting & curing - general","Division 03 — 03 30 00",
     "Concrete supply, placement/pumping, vibration, finishing, curing","CUM","",""],
    # Earthworks
    ["Earthworks","EARTH_TOPSOIL","Topsoil stripping","Division 02 — Site Work",
     "Remove organic layer, stockpile, protect vegetation","CUM / SQM","",""],
    ["Earthworks","EARTH_EXCAV","Excavation for foundations","Division 02 — Excavation & Trenching",
     "Bulk and trench excavation, slope benching, disposal","CUM","",""],
    ["Earthworks","EARTH_SHORING","Shoring / trench support","Division 02 — Temporary shoring",
     "Install sheet piles, soldier piles, timber shoring, bracing","assembly","",""],
    ["Earthworks","EARTH_BACKFILL","Backfill & compaction","Division 02 — Backfill",
     "Layered backfill, compaction, compaction testing","CUM","",""],
    ["Earthworks","EARTH_GRADING","Grading / site leveling","Division 02 — Grading",
     "Cut & fill balance, fine grading, proof roll","SQM / CUM","",""],
    # Dewatering
    ["Dewatering","DEWATER_SURF","Surface drainage / runoff control","Division 02 / 33 — Site utilities",
     "Temporary channels, diversion, settling pits","LM / SQM","",""],
    ["Dewatering","DEWATER_SUB","Dewatering / groundwater control","Division 02 — Dewatering systems",
     "Wellpoint systems, sumps, pumps, discharge management","system / day","",""],
    ["Dewatering","DEWATER_STORM","Stormwater drainage systems","Division 33",
     "Pipes, manholes, outfalls, connections","RM / manhole","",""],
    # Waterproofing
    ["Waterproofing","WATER_FOUND","Foundation waterproofing","Division 07 — Waterproofing",
     "Torch-on bitumen, cementitious coatings, bentonite, protection board","SQM","",""],
    ["Waterproofing","WATER_WETAREA","Wet area waterproofing (bathrooms)","Division 07 — Waterproofing",
     "Liquid membranes, sheet membranes, pond test","SQM","",""],
    ["Waterproofing","WATER_ROOF","Roof waterproofing","Division 07 — Roofing",
     "Torch-on, single-ply membranes, liquid applied PU","SQM","",""],
    ["Waterproofing","WATER_POOL","Tank/pool waterproofing","Division 07 / 03",
     "Cementitious tanking, PVC liners, epoxy coatings","SQM","",""],
    # Finishes
    ["Finishes","FIN_PLASTER","Plaster / render","Division 09 — Plaster & Gypsum",
     "Rough coat, finish coat, curing, sanding","SQM","10-20 mm",""],
    ["Finishes","FIN_PAINT","Interior painting","Division 09 — Painting",
     "Primer, putty, 2 coats finish","SQM","",""],
    ["Finishes","FIN_TILE","Tiling (ceramic/porcelain)","Division 09 — Tiling",
     "Tile adhesive, grout, leveling, waterproofing under tile if wet area","SQM","",""],
    ["Finishes","FIN_STONE","Stone finishes (marble/granite)","Division 09 — Stone",
     "Cut & fix, polishing, jointing","SQM","",""],
    ["Finishes","FIN_FLOOR_WOOD","Wood flooring / parquet","Division 09 — Wood Flooring",
     "Subfloor preparation, adhesive/floating installation","SQM","",""],
    # Ceilings
    ["Supplementary works","CEIL_SUSP_GYP","Suspended gypsum ceilings (grid)","Division 09 — Ceilings",
     "Install framework, hangers, gypsum tiles, access panels","SQM","",""],
    ["Supplementary works","CEIL_ACOUSTIC","Acoustic suspended ceilings","Division 09 — Ceilings",
     "Grid installation, acoustic tiles, trims","SQM","",""],
    # Plumbing
    ["Plumbing","PLUMB_WATER","Water supply piping (hot/cold)","Division 22 — Plumbing",
     "Lay pipes (PVC/Cu/PEX), valves, fittings, pressure testing","RM","",""],
    ["Plumbing","PLUMB_SAN","Sanitary waste & vent piping","Division 22 — Sanitary Piping",
     "Stacks, traps, vents, connection to sewer","RM / fixture","",""],
    ["Plumbing","PLUMB_STORM_EXT","External storm drainage networks","Division 33 / 22",
     "Pipes, manholes, gullies, outfalls","RM / manhole","",""],
    ["Plumbing","PLUMB_FIX","Plumbing fixtures installation","Division 22 — Plumbing Fixtures",
     "Install WC, basin, shower, sealing and testing","each","",""]
]

# Convert to DataFrames
df_ar = pd.DataFrame(arabic_rows, columns=["Category","ItemKey","ItemName_ar","CSI_Division","TypicalActivities","DefaultUnit","DefaultDepth","Notes"])
df_en = pd.DataFrame(english_rows, columns=["Category","ItemKey","ItemName_en","CSI_Division","TypicalActivities","DefaultUnit","DefaultDepth","Notes"])

# Save Excel file
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    df_ar.to_excel(writer, sheet_name="Arabic", index=False)
    df_en.to_excel(writer, sheet_name="English", index=False)

print("Excel created at:", out_path.resolve())
