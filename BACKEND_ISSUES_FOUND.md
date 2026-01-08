# Backend Issues Found - Comprehensive Check

## ✅ Already Fixed (Previous Session)
1. ✅ YearMonth sort key created and configured
2. ✅ Channel measures updated to base pattern
3. ✅ Press Release Views updated to base pattern
4. ✅ Landing Page Views updated to base pattern
5. ✅ Top10_Series sort configuration set

## 🔴 Critical Issues Found

### 1. Duplicate/Old Measure Names in TMDL
**Location:** `Metrics.tmdl` lines 435-472

**Issue:** Old measures with long names exist alongside new spec-compliant measures:
- `Top 10 Press Release Views` (line 435) - OLD, should be deleted or renamed
- `Remaining Press Release Views` (line 463) - OLD, should be deleted or renamed
- `Top 10 % of Press Release Traffic` (line 457) - References old name, should reference `Top 10 Share`
- `Remaining Press Release %` (line 469) - References old name, should be deleted or updated

**Status:** 
- ✅ Correct measures exist: `Top 10 PR Views`, `Remaining PR Views`, `Top 10 Share`
- ❌ Old measures still in TMDL (may cause confusion or errors)

**Action Required:** 
- Delete old measures OR rename them if they're used elsewhere
- Update percentage measures to reference new names

### 2. TMDL Syntax Error - Nested Measure Definition
**Location:** `Metrics.tmdl` lines 1078-1091

**Issue:** `Top10 Series Value` measure is incorrectly nested inside `Top Channel (PR)` measure definition. This is invalid TMDL syntax.

**Current (WRONG):**
```tmdl
measure 'Top Channel (PR)' = ```
    measure 'Top10 Series Value' = ...
```

**Action Required:** 
- Move `Top10 Series Value` to top level (it already exists correctly at line 1081, but this nested one is wrong)
- Fix `Top Channel (PR)` measure definition

### 3. Helper Tables Reference Old Measure Names
**Location:** 
- `Traffic_Breakdown_Categories.tmdl` lines 12-13
- `PR_Distribution_Categories.tmdl` lines 11-12

**Issue:** Both helper tables reference old measure names:
- `[Top 10 Press Release Views]` → Should be `[Top 10 PR Views]`
- `[Remaining Press Release Views]` → Should be `[Remaining PR Views]`

**Action Required:** Update SWITCH statements in both tables

### 4. Executive Summary References Old Names
**Location:** `Metrics.tmdl` lines 1009-1011

**Issue:** `Executive Summary Line 2` references:
- `[Top 10 Press Release Views]` → Should be `[Top 10 PR Views]`
- `[Top 10 % of Press Release Traffic]` → Should be `[Top 10 Share]`
- `[Remaining Press Release Views]` → Should be `[Remaining PR Views]`

**Action Required:** Update measure references

### 5. Channel Selector Table Uses Deprecated Pattern
**Location:** `Channel Selector.tmdl` lines 126-140

**Issue:** `Top 10 Views` measure uses `PressRelease_Summary` table instead of base measure pattern.

**Current:**
```dax
VAR Top10 = TOPN(10, PressRelease_Summary, PressRelease_Summary[Total Views], DESC)
RETURN SUMX(Top10, PressRelease_Summary[Total Views])
```

**Should be:** Use `[Top 10 PR Views]` measure directly, or use the spec pattern with `ALLSELECTED` and `TREATAS`.

**Action Required:** Update to use `[Top 10 PR Views]` or implement spec pattern

### 6. PressRelease_Summary Table Status
**Location:** `PressRelease_Summary.tmdl`

**Issue:** This calculated table was used by old measures. Now that we use base measure pattern, it may be:
- Still needed by `Channel Selector` table
- Or can be deprecated/hidden

**Action Required:** 
- If `Channel Selector` is updated, consider hiding/deprecating this table
- Or keep it if it's used elsewhere

### 7. Metric Dictionary Has Old Names
**Location:** `Metric_Dictionary.tmdl` lines 62-64

**Issue:** Dictionary data contains old measure names in its DATATABLE.

**Action Required:** Update dictionary entries to reflect new measure names

## 📋 Summary

**Total Issues:** 7
**Critical:** 4 (duplicate measures, syntax error, helper tables, executive summary)
**Medium:** 2 (Channel Selector pattern, PressRelease_Summary status)
**Low:** 1 (Metric Dictionary)

**Priority Order:**
1. Fix TMDL syntax error (nested measure)
2. Update helper tables to use new measure names
3. Update Executive Summary references
4. Fix Channel Selector measure pattern
5. Clean up duplicate old measures
6. Update Metric Dictionary
7. Evaluate PressRelease_Summary table
