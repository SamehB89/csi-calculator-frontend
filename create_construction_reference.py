from pathlib import Path
import pandas as pd

out_path = Path("construction_reference.xlsx")

# Arabic rows (Category, ItemKey, ItemName_ar, CSI_Division, TypicalActivities, DefaultUnit, DefaultDepth, Notes)
rows_ar = [
    # Concrete works
    ["أعمال الخرسانة","CONC_FOOT_ISO_PLAIN","قواعد منفصلة - عادية","Division 03 — Cast-in-Place Concrete (03 30)","شدة بسيطة / صب الخرسانة / معالجة وCuring","م³","400-600 mm",""],
    ["أعمال الخرسانة","CONC_FOOT_ISO_REINF","قواعد منفصلة - مسلحة","Division 03 — 03 10 / 03 20 / 03 30","شدة قواعد، وضع تسليح (مات/أعمدة ربط)، صب، معالجة","م³","600-1000 mm",""],
    ["أعمال الخرسانة","CONC_FOOT_STRIP_PLAIN","قواعد شريطية - عادية","Division 03 — Cast-in-Place Concrete (03 30)","قوالب شريطية، صب مستمر، jointing","م³","حسب المقطع",""],
    ["أعمال الخرسانة","CONC_FOOT_STRIP_REINF","قواعد شريطية - مسلحة","Division 03 — 03 10 / 03 20 / 03 30","شدة، تسليح شرائطي، صب","م³","حسب التصميم",""],
    ["أعمال الخرسانة","CONC_RAFT_PLAIN","لبشة - عادية","Division 03 — Cast-in-Place Concrete (03 30)","شدة حواف، صب لبشة بسماكة كبيرة، تقطيع مفاصل","م² / م³","300-600 mm",""],
    ["أعمال الخرسانة","CONC_RAFT_REINF","لبشة - مسلحة","Division 03 — 03 10 / 03 20 / 03 30","شبكات تسليح علوية وسفلية، صب متتابع، معالجة","م² / م³","300-600 mm",""],
    ["أعمال الخرسانة","CONC_TIE_BEAM","سملات / كمرات أرضية","Division 03 — Cast-in-Place Concrete (03 30)","شدة كمرات، تسليح (stirrups, main bars)، صب وتوصيل بالقواعد","RM / م³","حسب التصميم",""],
    ["أعمال الخرسانة","CONC_COLUMN","أعمدة خرسانية","Division 03 — 03 10 / 03 20 / 03 30","قوالب عمود، وضع حديد عمودي، صب، تشذيب وربط","Each","Height per design",""],
    ["أعمال الخرسانة","CONC_SLAB_GRADE","بلاطة على التربة (Slab on grade)","Division 03 — Cast-in-Place Concrete (03 30)","شدة حواف، تسليح شبكي، vapor barrier، صب وتسوية، joints","م² / م³","120-200 mm",""],
    ["أعمال الخرسانة","CONC_SLAB_SUSP","بلاطات أدوار (Suspended slabs)","Division 03 — Cast-in-Place Concrete (03 30)","شدة + props، تسليح شبكي/قضبان، صب، curing","م² / م³","Thickness per design",""],
    ["أعمال الخرسانة","CONC_FORMWORK_GEN","شدة عامة (Formwork)","Division 03 — 03 10 00","توريد وتركيب قوالب خشب/فولاذ، shores، فك الشدة","م² / count","",""],
    ["أعمال الخرسانة","CONC_REINF_GEN","تسليح عامة (Reinforcing)","Division 03 — 03 20 00","توفير وتثبيت حديد تسليح، قطع وثني، chairs، lap splices","KG / TON","",""],
    ["أعمال الخرسانة","CONC_CAST_GEN","صب وخرسانة (Casting & Curing)","Division 03 — 03 30 00","توريد خرسانة، نقل/ضخ، اهتزاز، finishing، curing","م³","",""],
    # Earthworks
    ["الأعمال الترابية","EARTH_TOPSOIL","تجريف / إزالة طبقة سطحية","Division 02 — Site Work","إزالة الطبقة العضوية، stockpile، حماية نباتات","م³ / م²","",""],
    ["الأعمال الترابية","EARTH_EXCAV","حفر للقواعد","Division 02 — Excavation & Trenching","Bulk/trench excavation، slope benching، disposal","م³","",""],
    ["الأعمال الترابية","EARTH_SHORING","سند جوانب الحفر (Shoring)","Division 02 — Temporary shoring","sheet piles، soldier piles، timber shoring، bracing","assembly","",""],
    ["الأعمال الترابية","EARTH_BACKFILL","ردم ودمك (Backfill & Compaction)","Division 02 — Backfill","Layered backfill، compaction، اختبار compaction","م³","",""],
    ["الأعمال الترابية","EARTH_GRADING","تسوية / Grading","Division 02 — Grading","cut & fill balance، fine grading، proof roll","م² / م³","",""],
    # Dewatering
    ["أعمال النزح","DEWATER_SURF","نزح سطحي (Surface drainage)","Division 02 / 33 — Site utilities","قنوات مؤقتة، تحويل مياه السطح، settling pits","RM / م²","",""],
    ["أعمال النزح","DEWATER_SUB","نزح جوفي (Dewatering)","Division 02 — Dewatering systems","wellpoint systems، sumps، pumps","system / day","",""],
    ["أعمال النزح","DEWATER_STORM","شبكات تصريف مياه الأمطار","Division 33","مواسير، manholes، outfalls، connections","RM / manhole","",""],
    # Waterproofing
    ["أعمال العزل","WATER_FOUND","عزل قواعد (Foundation waterproofing)","Division 07 — Waterproofing","Torch-on bitumen، cementitious coatings، bentonite، protection board","م²","",""],
    ["أعمال العزل","WATER_WETAREA","عزل الحمامات (Wet area waterproofing)","Division 07 — Waterproofing","Liquid membranes، sheet membranes، pond test","م²","",""],
    ["أعمال العزل","WATER_ROOF","عزل الأسطح (Roof waterproofing)","Division 07 — Roofing","Torch-on، single-ply membranes، liquid applied PU","م²","",""],
    ["أعمال العزل","WATER_POOL","عزل خزانات/أحواض (Tanking / Pools)","Division 07 / 03","Cementitious tanking، PVC liners، epoxy coatings","م²","",""],
    # Finishes
    ["التشطيبات","FIN_PLASTER","محارة (Plaster / Render)","Division 09 — Plaster & Gypsum","محارة خشنة، محارة ناعمة، floating، sanding","م²","10-20 mm",""],
    ["التشطيبات","FIN_PAINT","دهانات داخلية (Paints)","Division 09 — Painting","Primer، putty، 2 coats finish","م²","",""],
    ["التشطيبات","FIN_TILE","بلاط سيراميك/بورسلان (Tiling)","Division 09 — Tiling","Tile adhesive، grout، leveling، waterproofing under tile if wet area","م²","",""],
    ["التشطيبات","FIN_STONE","رخام/جرانيت (Stone finishes)","Division 09 — Stone","cut & fix، polishing، jointing","م²","",""],
    ["التشطيبات","FIN_FLOOR_WOOD","أرضيات خشبية / باركيه","Division 09 — Wood Flooring","Subfloor prep، adhesive/floating installation","م²","",""],
    # Ceilings
    ["أعمال تكميلية","CEIL_SUSP_GYP","أسقف معلقة جبسون / شبكة","Division 09 — Ceilings","Install framework، hangers، gypsum tiles، access panels","م²","",""],
    ["أعمال تكميلية","CEIL_ACOUSTIC","أسقف مستعارة صوتية","Division 09 — Ceilings","Grid installation، acoustic tiles، trims","م²","",""],
    # Plumbing
    ["السباكة","PLUMB_WATER","تمديدات مياه باردة/ساخنة","Division 22 — Plumbing","Lay pipes (PVC/Cu/PEX)، valves، fittings، pressure test","RM","",""],
    ["السباكة","PLUMB_SAN","صرف صحي داخلي","Division 22 — Sanitary Piping","Stacks، traps، vents، connection to external sewer","RM / fixture","",""],
    ["السباكة","PLUMB_STORM_EXT","شبكات تصريف خارجية","Division 33 / 22","Pipes، manholes، gullies، outfalls","RM / manhole","",""],
    ["السباكة","PLUMB_FIX","تجهيزات صحية (Fixtures)","Division 22 — Plumbing Fixtures","Install WC، basin، shower، sealing and testing","each","",""]
]

# English rows
rows_en = [
    # Concrete works
    ["Concrete works","CONC_FOOT_ISO_PLAIN","Isolated footings - plain","Division 03 — Cast-in-Place Concrete (03 30)","Simple pad formwork / concrete casting / curing","CUM","400-600 mm",""],
    ["Concrete works","CONC_FOOT_ISO_REINF","Isolated footings - reinforced","Division 03 — 03 10 / 03 20 / 03 30","Footing formwork, reinforcement mats/dowels, casting, curing","CUM","600-1000 mm",""],
    ["Concrete works","CONC_FOOT_STRIP_PLAIN","Strip footings - plain","Division 03 — Cast-in-Place Concrete (03 30)","Continuous strip formwork, continuous pour, jointing","CUM","Varies",""],
    ["Concrete works","CONC_FOOT_STRIP_REINF","Strip footings - reinforced","Division 03 — 03 10 / 03 20 / 03 30","Formwork, strip reinforcement cages, staged casting if needed","CUM","Varies",""],
    ["Concrete works","CONC_RAFT_PLAIN","Raft / Mat foundation - plain","Division 03 — Cast-in-Place Concrete (03 30)","Edge formwork, large slab pour, joints","SQM / CUM","300-600 mm",""],
    ["Concrete works","CONC_RAFT_REINF","Raft / Mat foundation - reinforced","Division 03 — 03 10 / 03 20 / 03 30","Top & bottom reinforcement mats, staged casting, curing","SQM / CUM","300-600 mm",""],
    ["Concrete works","CONC_TIE_BEAM","Tie beams / Ground beams","Division 03 — Cast-in-Place Concrete (03 30)","Beam formwork, stirrups & main bars, cast & tie to footings","RM / CUM","Depth per design",""],
    ["Concrete works","CONC_COLUMN","Concrete columns","Division 03 — 03 10 / 03 20 / 03 30","Column formwork, vertical reinforcement, casting, connection to bases","Each","Height per design",""],
    ["Concrete works","CONC_SLAB_GRADE","Slab on grade","Division 03 — Cast-in-Place Concrete (03 30)","Edge forms, mesh reinforcement, vapor barrier (if required), pour & finishing","SQM / CUM","120-200 mm",""],
    ["Concrete works","CONC_SLAB_SUSP","Suspended floor slabs","Division 03 — Cast-in-Place Concrete (03 30)","Formwork + props, reinforcement, curing, control joints","SQM / CUM","Thickness per design",""],
    ["Concrete works","CONC_FORMWORK_GEN","Formwork - general","Division 03 — 03 10 00","Supply & install plywood/steel forms, shoring, stripping sequence","SQM / count","",""],
    ["Concrete works","CONC_REINF_GEN","Reinforcing - general","Division 03 — 03 20 00","Supply & fixing of rebar, cutting / bending, chairs, lapping","KG / TON","",""],
    ["Concrete works","CONC_CAST_GEN","Casting & curing - general","Division 03 — 03 30 00","Concrete supply, placement/pumping, vibration, finishing, curing","CUM","",""],
    # Earthworks
    ["Earthworks","EARTH_TOPSOIL","Topsoil stripping","Division 02 — Site Work","Remove organic layer, stockpile, protect vegetation","CUM / SQM","",""],
    ["Earthworks","EARTH_EXCAV","Excavation for foundations","Division 02 — Excavation & Trenching","Bulk and trench excavation, slope benching, disposal","CUM","",""],
    ["Earthworks","EARTH_SHORING","Shoring / trench support","Division 02 — Temporary shoring","Install sheet piles, soldier piles, timber shoring, bracing","assembly","",""],
    ["Earthworks","EARTH_BACKFILL","Backfill & compaction","Division 02 — Backfill","Layered backfill, compaction, compaction testing","CUM","",""],
    ["Earthworks","EARTH_GRADING","Grading / site leveling","Division 02 — Grading","Cut & fill balance, fine grading, proof roll","SQM / CUM","",""],
    # Dewatering
    ["Dewatering","DEWATER_SURF","Surface drainage / runoff control","Division 02 / 33 — Site utilities","Temporary channels, diversion, settling pits","LM / SQM","",""],
    ["Dewatering","DEWATER_SUB","Dewatering / groundwater control","Division 02 — Dewatering systems","Wellpoint systems, sumps, pumps, discharge management","system / day","",""],
    ["Dewatering","DEWATER_STORM","Stormwater drainage systems","Division 33","Pipes, manholes, outfalls, connections","RM / manhole","",""],
    # Waterproofing
    ["Waterproofing","WATER_FOUND","Foundation waterproofing","Division 07 — Waterproofing","Torch-on bitumen, cementitious coatings, bentonite, protection board","SQM","",""],
    ["Waterproofing","WATER_WETAREA","Wet area waterproofing (bathrooms)","Division 07 — Waterproofing","Liquid membranes, sheet membranes, pond test","SQM","",""],
    ["Waterproofing","WATER_ROOF","Roof waterproofing","Division 07 — Roofing","Torch-on, single-ply membranes, liquid applied PU","SQM","",""],
    ["Waterproofing","WATER_POOL","Tank/pool waterproofing","Division 07 / 03","Cementitious tanking, PVC liners, epoxy coatings","SQM","",""],
    # Finishes
    ["Finishes","FIN_PLASTER","Plaster / render","Division 09 — Plaster & Gypsum","Rough coat, finish coat, curing, sanding","SQM","10-20 mm",""],
    ["Finishes","FIN_PAINT","Interior painting","Division 09 — Painting","Primer, putty, 2 coats finish","SQM","",""],
    ["Finishes","FIN_TILE","Tiling (ceramic/porcelain)","Division 09 — Tiling","Tile adhesive, grout, leveling, waterproofing under tile if wet area","SQM","",""],
    ["Finishes","FIN_STONE","Stone finishes (marble/granite)","Division 09 — Stone","Cut & fix, polishing, jointing","SQM","",""],
    ["Finishes","FIN_FLOOR_WOOD","Wood flooring / parquet","Division 09 — Wood Flooring","Subfloor preparation, adhesive/floating installation","SQM","",""],
    # Ceilings
    ["Supplementary works","CEIL_SUSP_GYP","Suspended gypsum ceilings (grid)","Division 09 — Ceilings","Install framework, hangers, gypsum tiles, access panels","SQM","",""],
    ["Supplementary works","CEIL_ACOUSTIC","Acoustic suspended ceilings","Division 09 — Ceilings","Grid installation, acoustic tiles, trims","SQM","",""],
    # Plumbing
    ["Plumbing","PLUMB_WATER","Water supply piping (hot/cold)","Division 22 — Plumbing","Lay pipes (PVC/Cu/PEX), valves, fittings, pressure testing","RM","",""],
    ["Plumbing","PLUMB_SAN","Sanitary waste & vent piping","Division 22 — Sanitary Piping","Stacks, traps, vents, connection to sewer","RM / fixture","",""],
    ["Plumbing","PLUMB_STORM_EXT","External storm drainage networks","Division 33 / 22","Pipes, manholes, gullies, outfalls","RM / manhole","",""],
    ["Plumbing","PLUMB_FIX","Plumbing fixtures installation","Division 22 — Plumbing Fixtures","Install WC, basin, shower, sealing and testing","each","",""]
]

# Create DataFrames
df_ar = pd.DataFrame(rows_ar, columns=["Category","ItemKey","ItemName_ar","CSI_Division","TypicalActivities","DefaultUnit","DefaultDepth","Notes"])
df_en = pd.DataFrame(rows_en, columns=["Category","ItemKey","ItemName_en","CSI_Division","TypicalActivities","DefaultUnit","DefaultDepth","Notes"])

# Save to Excel
df_ar.to_excel(out_path, sheet_name="Arabic", index=False)
df_en.to_excel(out_path, sheet_name="English", index=False)

print("Excel file created:", out_path.resolve())
