# 🎯 QUICK REFERENCE CARD

**Print this page for desk reference**

---

## 📄 FINAL PAGE NAMES

| # | Display Name | Nav Label |
|---|--------------|-----------|
| 1 | Executive Overview | Overview |
| 2 | Press Releases | Releases |
| 3 | Channel Performance | Channels |
| 4 | **Press Home Performance** | Press Home |
| 5 | Release Detail | *(drillthrough)* |
| 6 | Metric Dictionary | (i) |

---

## 📊 PAGE 1 KPIs (6 total)

1. **Total Views** - `#,0`
2. **Total Users** - `#,0`
3. **Landing Page Share of Views** - `0.0%`
4. **# Press Releases** - `#,0`
5. **Avg Views per Release** - `#,0`
6. **Top 10 Share** - `0.0%` ← Changed from "Top 10 %"

---

## 🔧 REQUIRED MEASURES (5 new)

Add to `Metrics` table:

1. `Press Release Views`
2. `Top 10 PR Views`
3. `Remaining PR Views`
4. `Top 10 Share`
5. `Top10 Series Value`

See `MEASURES_TO_ADD.dax` for code.

---

## 📋 REQUIRED HELPER TABLE

Create `Top10_Series` table:
- Column: `Series` (string)
- Values: "Top 10", "Remaining"

---

## 🎨 TOP 10 VS REMAINING CHART

**Visual Type:** 100% Stacked Column

**Field Wells:**
- **X-axis:** `Dim_Date[Month_Year]` ← COLUMN
- **Legend:** `Top10_Series[Series]` ← COLUMN
- **Y-axis:** `Metrics[Top10 Series Value]` ← MEASURE
- **Tooltips:** 4 measures (see spec)

---

## ⚠️ COMMON MISTAKES

| Mistake | Fix |
|---------|-----|
| X-axis has measure | Use column instead |
| Missing `active: true` | Run validator |
| Slicer has `visualContainerObjects` | Remove it |
| Wrong Measure/Column type | Check field type |

---

## 🚀 VALIDATION COMMANDS

```bash
# Full validation + auto-fix
python scripts/validators/master_pbip_validator.py "press-room-dashboard.Report" --fix

# Check measure bindings
python scripts/validators/check_all_measure_names.py

# Verify no errors
python scripts/validators/master_pbip_validator.py "press-room-dashboard.Report" --check
```

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `FINAL_DASHBOARD_SPEC.md` | Complete specification |
| `IMPLEMENTATION_GUIDE.md` | Step-by-step instructions |
| `MEASURES_TO_ADD.dax` | DAX code to add |
| `VALIDATION_CHECKLIST.md` | Quick validation checks |

---

## 🔍 LANDING PAGE DEFINITION

**Scope:** Press home only (not all entry pages)

**Logic:** 
```dax
IF(CONTAINSSTRING(Page_URL, "/press-room/index"), "Landing Page", ...)
```

**Result:** Only `/press-room/index.html` is "Landing Page"

---

## 📐 LAYOUT SPECS

- **Canvas:** 1280 × 720 px (16:9)
- **Margins:** 20px
- **Header:** 56px (with info icon)
- **Footer:** 24px ("INTERNAL USE ONLY", no page #)
- **Nav Rail:** 56px

---

## ✅ IMPLEMENTATION PHASES

1. **Phase 1:** Semantic model updates (15 min)
2. **Phase 2:** Visual generation (30 min)
3. **Phase 3:** Validation & testing (20 min)
4. **Phase 4:** Deployment (10 min)

**Total:** ~75 minutes

---

## 🆘 QUICK TROUBLESHOOTING

### Visuals show no data
→ Check `active: true` in projections

### "Non-measure field required" error
→ X-axis needs column, not measure

### Top 10 chart shows 0%
→ Verify `Press Release Views` returns data

### Cache issues
→ Delete `%LocalAppData%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces`

---

## 📞 HELP

- Full spec: `FINAL_DASHBOARD_SPEC.md`
- Implementation: `IMPLEMENTATION_GUIDE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

---

**Version:** 1.0  
**Last Updated:** January 7, 2026  
**Status:** ✅ Ready for Implementation
