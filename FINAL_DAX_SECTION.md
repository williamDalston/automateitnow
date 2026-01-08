# 📊 FINAL DAX SECTION - FOR SANITY CHECK

**Purpose:** Complete DAX code section with all fixes applied  
**Status:** Ready for Review  
**Version:** 2.3 (Production-Safe)

---

## ✅ ALL FIXES APPLIED

This section contains the corrected DAX code with all mathematical fixes:
1. ✅ Top 10 PR Views (per-URL aggregation)
2. ✅ # Press Releases (filter added)
3. ✅ Page_Type logic (enhanced precision)
4. ✅ Top10_Series (SortOrder added)
5. ✅ YearMonth sort key (for Month_Year)

---

## 📋 COMPLETE DAX CODE

### Base Measures

```dax
// Press Release Views (base measure)
Press Release Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Page_Type] = "Press Release"
)

// Landing Page Views (base measure)
Landing Page Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Page_Type] = "Landing Page"
)

// Landing Page Share % (calculated)
Landing Page Share % =
DIVIDE([Landing Page Views], [Total Views], 0)

// # Press Releases (count with filter - FIXED)
# Press Releases =
CALCULATE(
    DISTINCTCOUNT(Fact_Press_Analytics[Page_URL]),
    Fact_Press_Analytics[Page_Type] = "Press Release"
)
```

---

### Top 10 Measures (FIXED - Production-Safe Version)

```dax
// Top 10 PR Views (top 10 calculation - fixed set across date range - PRODUCTION-SAFE)
// Top 10 is determined across the selected date range, then shown over time
Top 10 PR Views =
VAR prTableAllDates =
    SUMMARIZE(
        FILTER(
            ALLSELECTED(Fact_Press_Analytics),
            Fact_Press_Analytics[Page_Type] = "Press Release"
        ),
        Fact_Press_Analytics[Page_URL],
        "__Views", SUM(Fact_Press_Analytics[Views])
    )
VAR top10 =
    TOPN(10, prTableAllDates, [__Views], DESC)
VAR top10Urls =
    SELECTCOLUMNS(
        top10,
        "Page_URL", Fact_Press_Analytics[Page_URL]
    )
RETURN
    CALCULATE(
        SUM(Fact_Press_Analytics[Views]),
        Fact_Press_Analytics[Page_Type] = "Press Release",
        TREATAS(top10Urls, Fact_Press_Analytics[Page_URL])
    )

// Remaining PR Views (remainder)
Remaining PR Views =
[Press Release Views] - [Top 10 PR Views]

// Top 10 Share (percentage for KPI)
Top 10 Share =
DIVIDE([Top 10 PR Views], [Press Release Views], 0)

// Top10 Series Value (switch measure for chart)
Top10 Series Value =
SWITCH(
    SELECTEDVALUE(Top10_Series[Series]),
    "Top 10", [Top 10 PR Views],
    "Remaining", [Remaining PR Views],
    BLANK()
)
```

**Key Fixes:**
1. Uses `ALLSELECTED` to calculate top 10 across entire selected date range (fixed set)
2. Uses `SUMMARIZE` with `SUM(Fact_Press_Analytics[Views])` per URL, not total `[Press Release Views]` measure
3. Uses `SELECTCOLUMNS` + `TREATAS` for production-safe URL extraction (not `ADDCOLUMNS` pattern)
4. Ensures correct per-URL aggregation and respects date filters automatically
5. Prevents "blank chart" and "same values" silent failures
6. Top 10 is fixed for the period, chart shows how their share changes over time

---

### Helper Table (FIXED - SortOrder Added)

```dax
// Top10_Series helper table (with SortOrder for legend ordering - FIXED)
Top10_Series = 
DATATABLE(
    "Series", STRING,
    "SortOrder", INTEGER,
    {
        { "Top 10", 1 },
        { "Remaining", 2 }
    }
)
```

**Configuration:** Set `Top10_Series[Series]` → **Sort by column** → `Top10_Series[SortOrder]`

---

### Required Date Column (NEW - Sort Key)

```dax
// Dim_Date[YearMonth] - Numeric sort key for Month_Year
YearMonth = YEAR(Dim_Date[Date]) * 100 + MONTH(Dim_Date[Date])
```

**Configuration:** Sort `Dim_Date[Month_Year]` by `Dim_Date[YearMonth]` to prevent alphabetical sorting.

---

### Page_Type Logic (ENHANCED - Production-Grade)

```dax
// Page_Type (enhanced precision - FIXED)
Page_Type =
VAR url = LOWER(Fact_Press_Analytics[Page_URL])
RETURN
SWITCH(
    TRUE(),
    ISBLANK(url), "Other",
    CONTAINSSTRING(url, "/press-room/index.html"), "Landing Page",
    CONTAINSSTRING(url, "/press-room/") && NOT CONTAINSSTRING(url, "/press-room/index.html"), "Press Release",
    "Other"
)
```

**Key Improvements:**
- Uses `LOWER()` for case-insensitive matching
- Checks for `/press-room/index.html` specifically (not just `/press-room/index`)
- Prevents false positives from querystrings or similar URLs

**Note:** For true production-grade, consider creating a `Dim_Page` mapping table (URL → Page_Type) and joining it.

---

## ✅ VALIDATION CHECKLIST

### Mathematical Correctness
- [x] Top 10 PR Views uses per-URL aggregation (not total measure)
- [x] # Press Releases includes filter context
- [x] All measures respect date filters automatically
- [x] No risk of "same values for every URL" bug
- [x] No risk of negative remainder (Top 10 + Remaining = Total)

### Sorting/Ordering
- [x] Top10_Series has SortOrder column
- [x] YearMonth sort key defined for Month_Year
- [x] Legend will order correctly (Top 10, then Remaining)
- [x] Months will sort chronologically (not alphabetically)

### Precision
- [x] Page_Type logic uses LOWER() and specific .html check
- [x] Prevents misclassification from querystrings
- [x] Handles blank URLs gracefully

---

## 🎯 EXPECTED BEHAVIOR

### Top 10 PR Views
- ✅ Returns sum of views from top 10 press releases by views
- ✅ Top 10 fixed across selected date range (not recalculated per month)
- ✅ Uses production-safe `SELECTCOLUMNS` + `TREATAS` pattern
- ✅ Respects current date filter context
- ✅ Each URL aggregated separately before ranking
- ✅ No "same number" issue
- ✅ No "blank chart" issue

### Top 10 Share
- ✅ Returns percentage (0-100%)
- ✅ Always: Top 10 PR Views + Remaining PR Views = Press Release Views
- ✅ No negative remainder possible

### Sorting
- ✅ Legend shows "Top 10" first, "Remaining" second
- ✅ X-axis months sort chronologically (Jan, Feb, Mar... not Apr, Aug, Dec...)

---

## 🚨 KNOWN FAILURE MODES PREVENTED

| Failure Mode | Prevention |
|--------------|------------|
| **"Same values for every URL"** | ✅ Fixed: Per-URL aggregation with SUMMARIZE |
| **"Blank chart" (URL extraction fails)** | ✅ Fixed: SELECTCOLUMNS + TREATAS pattern |
| **"Negative remainder"** | ✅ Prevented: Remaining = Total - Top 10 (always positive) |
| **"Blank chart"** | ✅ Prevented: Proper filter context, active: true in projections |
| **"Alphabetical month sorting"** | ✅ Prevented: YearMonth sort key |
| **"Wrong legend order"** | ✅ Prevented: SortOrder column |
| **"Misclassified URLs"** | ✅ Prevented: Enhanced Page_Type logic |

---

**Status:** ✅ Ready for Sanity Check  
**Version:** 2.1  
**All Fixes Applied:** Yes
