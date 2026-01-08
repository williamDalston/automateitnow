# Backend Fixes - Round 2

**Date:** 2026-01-08  
**Status:** ✅ Complete

## Issues Fixed

### 1. ✅ Top10_Series SortByColumn Missing

**Issue:** The `Series` column in `Top10_Series` table was missing the `sortByColumn: SortOrder` property, even though the spec explicitly requires it and it was documented as fixed.

**Fix:** Added `sortByColumn: SortOrder` to the `Series` column definition.

**File:** `press-room-dashboard.SemanticModel/definition/tables/Top10_Series.tmdl`

**Impact:** Ensures the legend order in the "Top 10 vs Remaining" chart is correct (Top 10 first, then Remaining).

---

### 2. ✅ Dim_Date Day_Of_Week_Number TMDL Syntax Error

**Issue:** The `Day_Of_Week_Number` calculated column used the wrong TMDL syntax for DAX expressions, causing a connection error: "Property 'expression' is unknown and is not expected in the situation it appears."

**Fix:** Changed from separate-line `expression =` syntax to inline syntax: `column Day_Of_Week_Number = WEEKDAY(Dim_Date[Date], 2)` followed by `dataType:` on the next line. This matches the pattern used in `Fact_Press_Analytics.tmdl` for DAX calculated columns.

**File:** `press-room-dashboard.SemanticModel/definition/tables/Dim_Date.tmdl`

**Impact:** Fixes TMDL import/connection errors for DAX calculated columns.

---

### 3. ✅ Dim_Date YearMonth Expression vs SourceColumn

**Issue:** The `YearMonth` column was using `expression = YEAR(...)` syntax, but it's actually calculated in Power Query M (line 168: `AddYearMonthKey = Table.AddColumn(AddYearMonth, "YearMonth", each [Year] * 100 + [Month], Int64.Type)`), not DAX. Columns from M partitions should use `sourceColumn`, not `expression`.

**Fix:** Changed `expression = YEAR(Dim_Date[Date]) * 100 + MONTH(Dim_Date[Date])` to `sourceColumn: YearMonth` to match the M query source.

**File:** `press-room-dashboard.SemanticModel/definition/tables/Dim_Date.tmdl`

**Impact:** Fixes the remaining TMDL import/connection error. Model now connects successfully via MCP.

---

## Verification

After these fixes:
- ✅ `Top10_Series[Series]` now sorts correctly by `SortOrder`
- ✅ TMDL syntax is correct for all calculated columns
- ✅ DAX calculated columns use inline syntax (`column Name = Expression`)
- ✅ M-calculated columns use `sourceColumn` instead of `expression`
- ✅ Model connects successfully via MCP (tested and confirmed)

---

## Summary

All three fixes were related to ensuring the model matches the spec requirements and uses correct TMDL syntax:

1. **Top10_Series sortByColumn:** Ensures proper legend ordering in visuals
2. **Day_Of_Week_Number syntax:** Fixes DAX calculated column syntax (use inline `= Expression`)
3. **YearMonth sourceColumn:** Fixes M-calculated column syntax (use `sourceColumn` not `expression`)

The model now connects successfully via MCP, and all calculated columns use the correct TMDL syntax for their source type (DAX vs Power Query M).
