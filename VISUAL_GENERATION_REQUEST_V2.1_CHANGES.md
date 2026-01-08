# 📋 VISUAL GENERATION INFORMATION REQUEST - V2.1 CHANGES

**Date:** January 8, 2026  
**Version:** 2.0 → 2.1  
**Status:** All redlines applied + critical additions

---

## 🔧 REDLINES / FIXES APPLIED

### 1. ✅ Dim_Date Section Fixed

**Issue:** Document referenced `Month_Year` and `YearMonth` which don't exist in actual model.

**Fix Applied:**
- Changed `Month_Year` → `Year_Month` (actual model column)
- Changed `YearMonth` → `[numeric_sort_key]` (unknown, needs confirmation)
- Added warning: Use actual model names and resolve spec names via alias map
- All references now clearly labeled "(Observed from current files)" vs "(Confirmed)"

**Location:** Section 3 (Model Manifest Contract)

---

### 2. ✅ PBIP Schema Lock Added

**Issue:** Document assumed `.pbip` structure without requiring actual file content.

**Fix Applied:**
- Added requirement: "Provide exact current `.pbip` file content (before modification)"
- Added requirement: "Confirm exact key name(s) Power BI expects"
- Added requirement: "Confirm dataset reference location"
- Changed generator rule: "Mirror the observed schema exactly from golden sample"

**Location:** Section 🚨 BLOCKER (at top)

---

### 3. ✅ Visual Mounting Mechanism Enhanced

**Issue:** Page Definition Integration section didn't explicitly ask for the key that links visual to page.

**Fix Applied:**
- Added explicit ask: "Visual mounting mechanism - what key links a visual folder to the page?"
- Added requirement: "Exact field/path in page file that enumerates visuals"
- Added requirement: "Example mapping" (visual id → folder path → visual.json name)
- Clarified: Without this, you can generate visuals that Power BI never loads

**Location:** Section 6 (Page Definition Integration)

---

### 4. ✅ Coordinate System Lock Added

**Issue:** Document assumed 1280×720 units without confirming what Power BI actually stores.

**Fix Applied:**
- Added new section: "Coordinate System Lock"
- Requires: Page dimensions from golden sample (width/height stored values)
- Requires: Visual position dimensions from golden sample
- Requires: Coordinate system (origin, axis directions)
- Generator rule: Use exact units from goldens, don't assume pixels

**Location:** Section 16 (Coordinate System Lock)

---

### 5. ✅ VisualType Canonical Strings Added

**Issue:** Document said "visualType matches expected value" but didn't require exact strings.

**Fix Applied:**
- Added new section: "Visual Type Canonical Strings"
- Requires: Exact `visual.visualType` string for each visual type from goldens
- Requires: Any `subType`/`drillDown`/`smallMultiples` flags
- Generator rule: Never invent visualType names; only use golden-derived constants

**Location:** Section 14 (Visual Type Canonical Strings)

---

### 6. ✅ Data Roles Contract Enhanced

**Issue:** Document asked for "role buckets and names" but wasn't strict enough.

**Fix Applied:**
- Enhanced to require: "Data roles contract (role bucket names + role IDs)"
- Added: "Role keys are singular or arrays?"
- Added: "Fields appear under `projections` only, or also under `select`/`from`/`where`?"
- Applied to: Line Chart, 100% Stacked Column Chart, Donut Chart sections

**Location:** Section 10 (Visual-Specific Requirements)

---

### 7. ✅ Visual-Level Filters Check Added

**Issue:** Document didn't ask about visual-level filters that can affect rendering.

**Fix Applied:**
- Added to each chart type: "Visual-level filters" subsection
- Requires: "Does golden contain a `filters` array?"
- Requires: "Does it contain any `filter` objects inside query state?"
- Generator rule: If goldens include `filters`, replicate exactly. If not, omit entirely.

**Location:** Section 10 (Visual-Specific Requirements)

---

### 8. ✅ Identity & Stable IDs Rules Added

**Issue:** Document didn't specify ID format requirements.

**Fix Applied:**
- Added new section: "Identity & Stable IDs Rules"
- Requires: Visual folder name format (GUID, length, charset)
- Requires: `visual.json` `name` property format
- Requires: `tabOrder` format and uniqueness
- Requires: How `page.json` references visuals (folder ID vs visual name)
- Generator rule: Produce IDs matching golden format (length + charset)

**Location:** Section 15 (Identity & Stable IDs Rules)

---

### 9. ✅ Minimal Golden Report Option Added

**Issue:** Document asked for samples from real report, which could have complexity/drift.

**Fix Applied:**
- Added to Section 2: "Alternative: Minimal Golden Report Option"
- Request: Create tiny "Golden PBIP" with 1 page, 5 visuals, theme applied
- Why: Single package becomes master truth, avoids drift

**Location:** Section 2 (Golden Sample Visuals)

---

### 10. ✅ Top 10 Validation Tightened

**Issue:** Validation only checked count, not URL identity.

**Fix Applied:**
- Added second assertion: "The same URLs persist across months (not just count)"
- Added manual test: Table with Month, URL, IsTop10 flag
- Generator rule: Top 10 URLs must be identical across date axis points (not just count)

**Location:** Section 11 (Top 10 Fixed Set Validation)

---

### 11. ✅ Wording Changes Applied

**Issue:** Document used "Expected" and ✅ checkmarks that could be treated as facts.

**Fix Applied:**
- Changed "Expected" → "Observed in golden sample" throughout
- Changed ✅ → "(Observed from current files)" vs "(Confirmed)"
- Clarified: Observations are not confirmed facts

**Locations:** Throughout document, especially:
- QueryRef patterns section
- Visual-specific requirements
- Model manifest contract
- Relationships contract

---

## 📊 SUMMARY OF CHANGES

| Category | Changes | Status |
|----------|---------|--------|
| **Redlines** | Dim_Date naming fixed | ✅ Complete |
| **Redlines** | PBIP schema lock added | ✅ Complete |
| **Redlines** | Visual mounting mechanism enhanced | ✅ Complete |
| **Additions** | Coordinate system lock | ✅ Complete |
| **Additions** | VisualType canonical strings | ✅ Complete |
| **Additions** | Data roles contract enhanced | ✅ Complete |
| **Additions** | Visual-level filters check | ✅ Complete |
| **Additions** | Identity & stable IDs rules | ✅ Complete |
| **Additions** | Minimal golden report option | ✅ Complete |
| **Enhancements** | Top 10 validation tightened | ✅ Complete |
| **Enhancements** | Wording improvements | ✅ Complete |

**Total Changes:** 11 major updates  
**Version:** 2.0 → 2.1  
**Status:** ✅ **All Redlines Applied + Critical Additions Complete**

---

## 🎯 TOP 5 CRITICAL CHANGES (As Requested)

1. ✅ **Dim_Date naming contradictions fixed** - Year_Month + numeric sort key as actual, everything else via alias map
2. ✅ **PBIP schema lock** - Require actual `.pbip` file content before enforcing structure
3. ✅ **Visual mounting key** - Require explicit mapping from page file to visual folder/id/name
4. ✅ **Coordinate system lock** - Confirm layout units from a page set to 1280×720
5. ✅ **Canonical visualType strings** - Require exact strings from goldens

---

## ✅ FINAL STATUS

The document is now:
- ✅ **Internally consistent** - No contradictions between spec names and model names
- ✅ **Schema-safe** - Requires actual file content, doesn't assume structure
- ✅ **Mounting-clear** - Explicitly asks for visual-to-page linkage
- ✅ **Unit-precise** - Requires coordinate system confirmation
- ✅ **Type-exact** - Requires canonical visualType strings
- ✅ **Role-strict** - Enhanced data roles contract
- ✅ **Filter-aware** - Checks for visual-level filters
- ✅ **ID-format-locked** - Specifies ID requirements
- ✅ **Golden-focused** - Minimal golden report option
- ✅ **Validation-tight** - Top 10 checks both count and identity
- ✅ **Wording-precise** - "Observed" vs "Confirmed" throughout

**Status:** 🔒 **Ready for Information Collection**

---

**Next Step:** Once information is provided, update `PRECISE_VISUAL_GENERATION_METHOD.md` with verified patterns and create generation script that matches Power BI's exact expectations.
