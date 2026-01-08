# 📂 FILE STRUCTURE - COMPLETE LAYOUT

**Base Path:** `C:\Users\farad\OneDrive\Desktop\automation-system`

---

## 📁 Complete Directory Structure

```
C:\Users\farad\OneDrive\Desktop\automation-system\
│
├── INDEX.md                               ← Complete file guide
├── README.md                              ← Start here
├── QUICK_REFERENCE.md                     ← One-page reference (print this)
├── SYSTEM_SUMMARY.md                      ← System overview
├── FILE_STRUCTURE.md                      ← This file
│
├── 🔒 SPECIFICATION (LOCKED)
├── FINAL_DASHBOARD_SPEC.md                ← ⭐ Complete specification
├── DECISIONS_LOG.md                       ← Decision rationale
├── IMPLEMENTATION_GUIDE.md                ← ⭐ 75-minute implementation plan
├── MEASURES_TO_ADD.dax                    ← Copy-paste DAX code
├── DASHBOARD_STRUCTURE_AND_NAMING.md      ← (superseded, archived)
│
├── ✅ VALIDATION & QUALITY
├── FOOLPROOF_AUTOMATION_PLAN.md           ← System architecture
├── VALIDATION_CHECKLIST.md                ← Quick checks
│
├── press-room-dashboard.pbip                    ← Main PBIP file
│
├── press-room-dashboard.Report\                 ← Report folder
│   ├── definition.pbir                          ← Dataset reference (CRITICAL)
│   ├── definition\
│   │   ├── pages\
│   │   │   ├── pages.json
│   │   │   └── [page-id]\
│   │   │       ├── page.json
│   │   │       └── visuals\
│   │   │           └── [visual-id]\
│   │   │               └── visual.json
│   │   ├── report.json                          ← Report config
│   │   └── version.json
│   └── StaticResources\
│
├── press-room-dashboard.SemanticModel\          ← Semantic model folder
│   ├── definition.pbism                         ← Semantic model metadata
│   └── definition\
│       ├── database.tmdl
│       ├── model.tmdl
│       ├── relationships.tmdl                   ← Relationships (CRITICAL)
│       ├── cultures\
│       ├── perspectives\
│       └── tables\
│           └── [table-name].tmdl
│
├── scripts\
│   ├── validators\
│   │   ├── master_pbip_validator.py             ← Main validator
│   │   └── check_all_measure_names.py           ← Binding checker
│   ├── generators\                              ← (To be populated)
│   └── fixers\                                  ← (To be populated)
│
├── templates\
│   ├── visual_templates\                        ← (To be populated)
│   └── structure_templates\                     ← (To be populated)
│
├── patterns\
│   ├── working_visuals\                         ← (To be populated)
│   └── working_structure\                       ← (To be populated)
│
├── docs\
│   └── TROUBLESHOOTING.md
│
└── assets\                                      ← HHS Assets
    ├── ICONS_README.md
    ├── *.svg                                    ← SVG icons
    ├── *.png                                    ← PNG images
    └── HHS_Spec_Deck_With_Data\
        └── Slide*.SVG
```

---

## 🔑 Critical File Paths

### Main Dashboard Files
```
C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.pbip
C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.Report\definition.pbir
C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.Report\definition\report.json
C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.SemanticModel\definition.pbism
C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.SemanticModel\definition\relationships.tmdl
```

### Scripts
```
C:\Users\farad\OneDrive\Desktop\automation-system\scripts\validators\master_pbip_validator.py
C:\Users\farad\OneDrive\Desktop\automation-system\scripts\validators\check_all_measure_names.py
```

### Documentation
```
C:\Users\farad\OneDrive\Desktop\automation-system\README.md
C:\Users\farad\OneDrive\Desktop\automation-system\FOOLPROOF_AUTOMATION_PLAN.md
C:\Users\farad\OneDrive\Desktop\automation-system\VALIDATION_CHECKLIST.md
C:\Users\farad\OneDrive\Desktop\automation-system\SYSTEM_SUMMARY.md
C:\Users\farad\OneDrive\Desktop\automation-system\docs\TROUBLESHOOTING.md
```

---

## 📝 Usage Examples

### Validate Dashboard
```bash
cd C:\Users\farad\OneDrive\Desktop\automation-system
python scripts\validators\master_pbip_validator.py "press-room-dashboard.Report" --fix
```

### Check Measure Bindings
```bash
cd C:\Users\farad\OneDrive\Desktop\automation-system
python scripts\validators\check_all_measure_names.py
```

### Open Dashboard
```
Double-click: C:\Users\farad\OneDrive\Desktop\automation-system\press-room-dashboard.pbip
```

---

## 🔄 Relative Paths (from automation-system folder)

### From Root to Scripts
```
scripts\validators\master_pbip_validator.py
```

### From Scripts to Dashboard
```
..\..\press-room-dashboard.Report
```

### From Report to Semantic Model
```
..\press-room-dashboard.SemanticModel
```

---

## ✅ File Status

| Path | Status | Notes |
|------|--------|-------|
| `press-room-dashboard.pbip` | ✅ Complete | Working reference |
| `press-room-dashboard.Report\` | ✅ Complete | Full report structure |
| `press-room-dashboard.SemanticModel\` | ✅ Complete | Full semantic model |
| `scripts\validators\` | ✅ Complete | 2 critical scripts |
| `scripts\generators\` | ⏳ Empty | Ready for patterns |
| `scripts\fixers\` | ⏳ Empty | Ready for fixes |
| `templates\` | ⏳ Empty | Ready for templates |
| `patterns\` | ⏳ Empty | Ready for extraction |
| `docs\` | ✅ Complete | Troubleshooting guide |
| `assets\` | ✅ Complete | All HHS assets |

---

**Last Updated:** December 2024
