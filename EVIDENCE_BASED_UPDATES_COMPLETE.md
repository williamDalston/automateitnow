# Evidence-Based Updates Complete

**Date:** 2026-01-08  
**Status:** ✅ All Updates Applied

---

## Summary

All three documents have been updated with the merged, cleaned-up truth set from your feedback:

1. ✅ **VISUAL_GENERATION_EVIDENCE_REPORT.md** - Reorganized with confirmed/conditional/unknown sections
2. ✅ **PRECISE_VISUAL_GENERATION_METHOD.md** - Added evidence-based contracts (v2.0)
3. ✅ **Dim_Date.tmdl** - Fixed Year_Month sorting (added YearMonth key)

---

## ✅ CONFIRMED STRUCTURES (Now in Both Documents)

### PBIP/PBIR Structure
- ✅ `.pbip` artifacts array (report-only observed)
- ✅ `definition.pbir` datasetReference.byPath
- ✅ Folder map (version.json, report.json, pages.json)

### Coordinate System
- ✅ Page dimensions: `1280 × 720` (numbers, not "px")
- ✅ Visual position: **floats allowed** (observed decimals)
- ✅ Units: "Power BI stored units" (not claiming pixels/points)

### QueryRef Patterns
- ✅ Columns: `"Table.Column"` (dot notation, underscores preserved)
- ❌ Measures: **UNKNOWN** (requires golden Card sample)

### Sorting
- ✅ Slicer structure confirmed
- ❌ Chart sorting: **UNKNOWN** (requires golden samples)

### Model Sorting
- ✅ **FIXED:** `Year_Month.sortByColumn = YearMonth` (added numeric key)

---

## ⚠️ CONDITIONAL RULES (Documented)

1. **PBIP Dataset Artifact** - Only report observed, conditional on Desktop build
2. **Visual Mounting** - Likely folder-discovery, needs rename test confirmation

---

## ❌ EXPLICIT UNKNOWNS (Documented as Blockers)

1. Power BI Desktop version/build
2. Card/Line/Donut/Stacked Column golden samples
3. Measure queryRef/nativeQueryRef (measures with spaces)
4. Chart role buckets
5. Chart sorting behavior
6. Page mounting confirmation (rename test)

---

## Changes Made

### 1. VISUAL_GENERATION_EVIDENCE_REPORT.md
- Reorganized into ✅ Confirmed / ⚠️ Conditional / ❌ Unknown sections
- Added "Generator Impact" annotations
- Added verbatim file contents section
- Marked model sorting as FIXED
- Removed guesses (e.g., measure queryRef patterns)

### 2. PRECISE_VISUAL_GENERATION_METHOD.md (v2.0)
- Added "✅ CONFIRMED STRUCTURES" section with generator contracts
- Added "⚠️ CONDITIONAL RULES" section
- Added "❌ EXPLICIT UNKNOWNS" section
- Added "🔒 GENERATOR CONSTRAINTS" section
- Updated position calculation to use floats (not "px")
- Updated z-index section (z and tabOrder are separate axes)
- Marked measure patterns as UNKNOWN (not guessing)

### 3. Dim_Date.tmdl
- Added `YearMonth` numeric key column (YYYYMM format)
- Set `Year_Month.sortByColumn = YearMonth`
- Updated Power Query M source to include `AddYearMonthKey` step
- Marked `YearMonth` as hidden (internal sort key)

---

## Generator Readiness

**Ready to Generate:**
- ✅ Slicers (all patterns confirmed)
- ✅ Page structure (dimensions, folder map)
- ✅ Column bindings (queryRef/nativeQueryRef confirmed)

**Cannot Generate Yet:**
- ❌ Cards (missing measure queryRef patterns)
- ❌ Line Charts (missing role buckets, sorting)
- ❌ Donut Charts (missing role buckets)
- ❌ 100% Stacked Column (missing role buckets, sorting)

**Next Manual Steps:**
1. Create GOLDEN_MIN PBIP in Power BI Desktop (5 visuals)
2. Extract golden samples (full visual.json for each type)
3. Get Power BI Desktop version (Help → About)
4. Run rename test (validate visual mounting)

---

## Files Modified

1. `VISUAL_GENERATION_EVIDENCE_REPORT.md` - Complete rewrite with truth set
2. `PRECISE_VISUAL_GENERATION_METHOD.md` - Added evidence-based sections (v2.0)
3. `press-room-dashboard.SemanticModel/definition/tables/Dim_Date.tmdl` - Added YearMonth sort key

---

## Key Improvements

1. **No More Guessing** - All "conclusions" removed that weren't directly observed
2. **Generator Contracts** - Each confirmed structure has explicit generator rules
3. **Explicit Unknowns** - Clear list of blockers that need golden samples
4. **Model Compliance** - Year_Month sorting now matches spec requirement
5. **Float Support** - Position calculations now allow decimals (not rounded to ints)

---

**All evidence-based updates complete. Documents now reflect observed reality, not assumptions.**
