# Evidence Report Updated - Summary

**Date:** 2026-01-08  
**Status:** ✅ Completed

---

## Actions Taken

### 1. Fixed Model Sorting Compliance ✅

**Issue:** `Dim_Date[Year_Month]` had no `sortByColumn` property, risking lexical sorting.

**Fix Applied:**
- Added `YearMonth` numeric key column (YYYYMM format: `YEAR(Date) * 100 + MONTH(Date)`)
- Set `Year_Month.sortByColumn = YearMonth` in TMDL
- Updated Power Query M source to include `YearMonth` column calculation
- Marked `YearMonth` as hidden (internal sort key only)

**File Modified:**
- `press-room-dashboard.SemanticModel/definition/tables/Dim_Date.tmdl`

**Evidence (VERBATIM):**
```tmdl
/// Year-Month formatted as text (e.g., '2025-03'). Useful for sorting and labeling. Sorted by YearMonth for chronological ordering.
column Year_Month
	dataType: string
	lineageTag: pr-dimdate-yearmonth
	summarizeBy: none
	sourceColumn: Year_Month
	sortByColumn: YearMonth

	annotation SummarizationSetBy = Automatic

/// Numeric sort key for Year_Month column (YYYYMM format). Used to ensure chronological sorting instead of alphabetical.
column YearMonth
	dataType: int64
	formatString: 0
	isHidden
	lineageTag: pr-dimdate-yearmonth-sort
	summarizeBy: sum
	expression = YEAR(Dim_Date[Date]) * 100 + MONTH(Dim_Date[Date])

	annotation SummarizationSetBy = Automatic
```

### 2. Updated Evidence Report ✅

**File:** `VISUAL_GENERATION_EVIDENCE_REPORT.md`

**Changes:**
- Reorganized into sections: ✅ Confirmed, ⚠️ Conditional, ❌ Unknowns
- Added "Merged, Cleaned-Up Truth Set" section at top
- Added verbatim file contents section
- Added "Generator Impact" annotations for each confirmed structure
- Marked model sorting compliance as FIXED
- Added explicit list of missing evidence

### 3. Updated Precise Generation Method ✅

**File:** `PRECISE_VISUAL_GENERATION_METHOD.md`

**Changes:**
- Added version 2.0 header with evidence source reference
- Added new section "✅ CONFIRMED STRUCTURES" with generator contracts
- Added new section "⚠️ CONDITIONAL RULES" (PBIP dataset artifact, visual mounting)
- Added new section "❌ EXPLICIT UNKNOWNS" (blockers list)
- Added new section "🔒 GENERATOR CONSTRAINTS" (floats, schema versions, visualType strings)
- Updated projection requirements to mark measures as unknown
- Updated position calculation to use floats (not pixels/points)
- Updated z-index section to note floats are allowed

---

## Current State

**✅ Ready for Generator (Confirmed):**
- PBIP/PBIR structure (artifacts, definition.pbir, folder map)
- Coordinate system (floats allowed, no pixel claims)
- Column queryRef/nativeQueryRef patterns (dot notation confirmed)
- Slicer sorting structure (sortDefinition confirmed)
- Model sorting compliance (Year_Month fixed)

**⚠️ Conditional (Require Validation):**
- PBIP dataset artifact (only report observed, may vary by build)
- Visual mounting (likely folder-discovery, needs rename test)

**❌ Unknowns (Blockers):**
- Power BI Desktop version/build
- Card/Line/Donut/Stacked Column golden samples
- Measure queryRef/nativeQueryRef (measures with spaces)
- Chart sorting behavior
- Chart role buckets

---

## Next Manual Actions Required

1. **Get Power BI Desktop version** (Help → About)
2. **Create GOLDEN_MIN PBIP** (5 visuals: Card, Line, Donut, Stacked, Slicer)
3. **Run rename test** (validate visual mounting)
4. **Extract golden samples** (full visual.json for each type)
