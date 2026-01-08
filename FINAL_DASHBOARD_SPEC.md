# 🎯 FINAL DASHBOARD SPECIFICATION

**Version:** 2.4 LOCKED  
**Status:** ✅ Production-Ready (Mathematically Locked + Silent Failures Fixed)  
**Last Updated:** January 8, 2026

---

## 📋 DOCUMENT STRUCTURE

This specification is organized into **4 locked blocks**:

1. **🔒 DECISIONS** - Scope, naming, and locked choices
2. **📊 MEASURE CONTRACT** - Canonical metric definitions
3. **📄 PAGE SPECS** - Per-page specifications (KPIs, visuals, filters, drillthrough)
4. **🔧 BUILD RECIPES** - Field well configurations for each visual

---

# 🔒 BLOCK 1: DECISIONS

## 1.1 Landing Page Scope (LOCKED)

**Decision:** Landing Page = **Press Room Homepage Only**

**Definition:**
- `Page_Type = "Landing Page"` identifies **ONLY** `/press-room/index.html`
- **NOT** all entry pages (GA4 landing page dimension)
- **NOT** all press room pages

**Model Logic (Production-Grade):**
```dax
Page_Type =
VAR url0 = LOWER(TRIM(Fact_Press_Analytics[Page_URL]))

-- Guard: Treat empty string as blank (ISBLANK doesn't always catch "" for text)
VAR urlIsMissing = ISBLANK(url0) || url0 = ""

-- Strip query string + hash fragment properly (cut at first ? or #)
VAR qPos = FIND("?", url0, 1, 0)
VAR hPos = FIND("#", url0, 1, 0)
VAR cutPos =
    IF(
        qPos = 0 && hPos = 0, 0,
        IF(qPos = 0, hPos,
            IF(hPos = 0, qPos, MIN(qPos, hPos))
        )
    )
VAR urlPath = IF(cutPos > 0, LEFT(url0, cutPos - 1), url0)

-- Normalize trailing slash for comparisons
VAR urlNoTrail =
    IF(RIGHT(urlPath, 1) = "/", LEFT(urlPath, LEN(urlPath) - 1), urlPath)

-- Landing page canonical variants (ENDS-WITH style checks)
-- Guard: Treat /press-room (no trailing slash) as Press Home if it occurs
VAR isPressHome =
    urlNoTrail = "/press-room"
    || RIGHT(urlPath, LEN("/press-room/")) = "/press-room/"
    || RIGHT(urlNoTrail, LEN("/press-room/index")) = "/press-room/index"
    || RIGHT(urlNoTrail, LEN("/press-room/index.html")) = "/press-room/index.html"

-- Broad press-room bucket (still overinclusive, but matches your locked warning)
VAR isPressRoom =
    CONTAINSSTRING(urlPath, "/press-room/")

RETURN
SWITCH(
    TRUE(),
    urlIsMissing, "Other",
    isPressHome, "Landing Page",
    isPressRoom, "Press Release",
    "Other"
)
```

**🔒 URL CANONICALIZATION RULE (LOCKED):**
> **Landing page detection must handle canonical variants:**
> - Strip query string (`?utm=...`) and hash fragments (`#section`) by cutting at first `?` or `#`
> - Use ENDS-WITH style pattern matching (not `CONTAINSSTRING`) to detect landing page
> - Treat `/press-room/` as landing page (if true in your site)
> - Treat `/press-room/index` as landing page (if true in your site)
> - Treat `/press-room/index.html` as landing page
> 
> **Do NOT use `CONTAINSSTRING("/press-room/")` to detect landing page. Landing must be matched via end-of-path patterns.**
> 
> **For production-grade implementation:** Use a `Dim_Page` mapping table (canonical URL → Page_Type) instead of string matching.

**Note:** For true production-grade implementation, create a `Dim_Page` mapping table (URL → Page_Type) and join it, so this logic isn't embedded in the fact table.

**Terminology:** "Landing Page" in measures = "Press Home" (single URL). Kept for consistency with `Page_Type` column name.

**Configuration:**
```json
"landingScope": "press_home"
```

**Impact:**
- Page 4 name: **Press Home Performance** (not "Landing Page Performance")
- Nav label: **Press Home** (not "Landing")
- Measures filter: `Page_Type = "Landing Page"` (single URL only)

**⚠️ PRODUCTION WARNING:**
> **Press Release classification must be validated against known URL patterns or a Dim_Page mapping table. Do not assume all `/press-room/*` URLs are press releases.** The current logic classifies any URL under `/press-room/` (except index) as "Press Release", which may incorrectly label non-release pages (about pages, category pages, media assets, etc.). For production-grade implementation, create a `Dim_Page` mapping table (URL → Page_Type) and join it, so classification logic is not embedded in the fact table.

---

## 1.2 Page Names (LOCKED)

| # | Display Name | Internal ID | Nav Label | Type |
|---|--------------|-------------|-----------|------|
| 1 | **Executive Overview** | `home` | **Overview** | Standard |
| 2 | **Press Releases** | `releases` | **Releases** | Standard |
| 3 | **Channel Performance** | `channels` | **Channels** | Standard |
| 4 | **Press Home Performance** | `landing` | **Press Home** | Standard |
| 5 | **Release Detail** | `release_detail` | *(drillthrough)* | Drillthrough |
| 6 | **Metric Dictionary** | `metric_dictionary` | **(i)** | Reference |

**Note:** Page 4 name locked to "Press Home Performance" based on scope decision (1.1).

---

## 1.3 KPI Labels (LOCKED)

### Page 1: Executive Overview (6 KPIs)

| # | Label | Measure | Format | Definition |
|---|-------|---------|--------|------------|
| 1 | **Total Views** | `Metrics[Total Views]` | `#,0` | Total page views across all press room pages |
| 2 | **Total Users** | `Metrics[Total Users]` | `#,0` | Total unique users across all press room pages |
| 3 | **Landing Page Share of Views** | `Metrics[Landing Page Share %]` | `0.0%` | Landing Page Views ÷ Total Views |
| 4 | **# Press Releases** | `Metrics[# Press Releases]` | `#,0` | Count of distinct press releases |
| 5 | **Avg Views per Release** | `Metrics[Avg Views per Release]` | `#,0` | Press Release Views ÷ # Press Releases |
| 6 | **Top 10 Share** | `Metrics[Top 10 Share]` | `0.0%` | Share of Press Release Views from top 10 releases by views |

**Critical Notes:**
- KPI #3: **"Landing Page Share of Views"** (not "Landing Page %")
- KPI #6: **"Top 10 Share"** (not "Top 10 %" - eliminates percentile ambiguity)
- KPI #6 Tooltip: *"Share of total Press Release Views coming from the top 10 releases by views."*

---

## 1.4 Layout Dimensions (LOCKED)

### Canvas
- **Size:** 1280 × 720 px (16:9)
- **Display:** FitToPage
- **Margins:** 20px (all sides)
- **Gap:** 20px between elements

### Header Band
- **Height:** **56px**
- **Readability Rules:**
  - Header font size: >= 14pt
  - KPI label font size: >= 11pt
  - Minimum contrast ratio: 4.5:1 (WCAG AA)
- **Contains:**
  - Page title (left)
  - Info icon (i) → links to Metric Dictionary (right)
  - Date context (right, top)
  - Last refreshed (right, bottom)

### Footer Band
- **Height:** 24px
- **Contains:**
  - Data source (left)
  - **"INTERNAL USE ONLY"** (center) ← **No page numbers**
  - Generated date (right)

### Navigation Rail
- **Width:** 56px
- **Position:** Left side
- **Layering:** Controlled via Selection Pane (Background, Containers, Visuals, Overlays)
- **Items:**
  1. Overview (home icon)
  2. Releases (document icon)
  3. Channels (chart icon)
  4. Press Home (target icon)
  5. (i) icon (bottom) → Metric Dictionary

---

## 1.5 Naming Conventions (LOCKED)

### Table Naming
- **Prefix:** `Dim_` for dimensions, `Fact_` for facts
- **Examples:**
  - `Dim_Date`
  - `Fact_Press_Analytics`
  - `Metrics` (measures table)
  - **Note:** No `Dim_Channel` in v2.2 - channel data lives in `Fact_Press_Analytics[Channel_Group]`

### Measure Naming
- **Structure:** `Metrics[Measure Name]`
- **Format:** PascalCase with spaces allowed
- **Examples:**
  - `Metrics[Total Views]`
  - `Metrics[Press Release Views]`
  - `Metrics[Top 10 Share]`

### Column Naming
- **Format:** PascalCase with underscores
- **Examples:**
  - `Page_URL`
  - `Page_Type`
  - `Channel_Group`
  - `Month_Year`

### Channel Dimension Source (LOCKED)

**Decision:** Channel grouping lives in `Fact_Press_Analytics[Channel_Group]`

- **No `Dim_Channel` table in v2.2**
- All channel visuals and channel measures bind to **Fact** column
- All channel references use: `Fact_Press_Analytics[Channel_Group]`
- **Rationale:** Matches actual data model structure

### Visual Naming
- **Format:** `snake_case` for internal IDs
- **Examples:**
  - `total_views` (KPI card)
  - `top10_vs_remaining` (chart)
  - `date_slicer` (slicer)

### Global Sorting Rules (CRITICAL)
- **All time text labels must have an integer sort key**
- **Month_Year must sort by YearMonth (YYYYMM format)**
- **All categorical series must have SortOrder column**
- **Rationale:** Prevents alphabetical sorting, ensures chronological/correct ordering

---

# 📊 BLOCK 2: MEASURE CONTRACT

## 2.0 Model Prerequisites (LOCKED)

**Purpose:** Required fields and data types for generator to hard-fail early if missing.

### Fact Table: `Fact_Press_Analytics`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `Views` | Numeric | ✅ | Page view count |
| `Users` | Numeric | ✅ | Unique user count (may be non-additive) |
| `Page_URL` | Text | ✅ | Full URL path |
| `Channel_Group` | Text | ✅ | Channel classification |
| `Page_Type` | Text | ✅ | Calculated column or dimension join |

### Dimension Table: `Dim_Date`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `Date` | Date | ✅ | Primary date key |
| `Month_Year` | Text | ✅ | Display label (e.g., "Jan 2024") |
| `YearMonth` | Numeric | ✅ | Sort key (YYYYMM format) |

### Measures Table: `Metrics`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| All measures defined in 2.1 | Measure | ✅ | See Measure Contract below |

### Helper Tables

| Table | Required | Notes |
|-------|----------|-------|
| `Top10_Series` | ✅ | 2-row table with `Series` and `SortOrder` columns |

### Optional Dimension: `Dim_Press_Releases`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `Page_URL` | Text | ⚠️ Optional | Primary key (or use `ReleaseID` if available) |
| `Page_Title` | Text | ⚠️ Optional | Display name for releases |
| `Publish_Date` | Date | ⚠️ Optional | Publication date |
| `Category` | Text | ⚠️ Optional | Release category |

**Fallback Behavior:**
- If `Dim_Press_Releases` missing, use `Fact_Press_Analytics[Page_URL]` for all release references
- Top Releases Table shows `Page_URL` instead of `Page_Title` if dimension missing
- Release Detail metadata table shows URL-only if dimension missing

**Generator Validation:** Generator must validate all prerequisites exist before generating visuals. Hard-fail with clear error message if any required field is missing. Warn (but continue) if optional dimension fields are missing.

---

## 2.1 Core Measures (Global)

**Purpose:** Canonical list of measures used across all pages. This is the shared language between wireframe and DAX.

| Measure Name | Definition | Formula | Filter Context |
|--------------|------------|---------|----------------|
| **Total Views** | Total page views across all press room pages | `SUM(Fact_Press_Analytics[Views])` | None (all pages) |
| **Total Users** | Total unique users across all press room pages | `SUM(Fact_Press_Analytics[Users])` | None (all pages) |
| **Press Release Users** | Total unique users for press releases only | `CALCULATE([Total Users], Fact_Press_Analytics[Page_Type] = "Press Release")` | `Page_Type = "Press Release"` |
| **Landing Page Users** | Total unique users for press room homepage only | `CALCULATE([Total Users], Fact_Press_Analytics[Page_Type] = "Landing Page")` | `Page_Type = "Landing Page"` |

**⚠️ USERS METRIC ADDITIVITY WARNING:**
> **Users is additive only if the source metric is already de-duplicated at the exported grain. Otherwise treat as 'summed users' and interpret cautiously.** Many analytics exports make "Users" non-additive across pages (summing double-counts people who visited multiple pages). Verify your source data grain before summing users across pages.
| **Organic Search Views** | Total views from organic search traffic | `CALCULATE([Total Views], Fact_Press_Analytics[Channel_Group] = "Organic Search")` | `Channel_Group = "Organic Search"` |
| **Direct Views** | Total views from direct traffic | `CALCULATE([Total Views], Fact_Press_Analytics[Channel_Group] = "Direct")` | `Channel_Group = "Direct"` |
| **Referral Views** | Total views from referral traffic | `CALCULATE([Total Views], Fact_Press_Analytics[Channel_Group] = "Referral")` | `Channel_Group = "Referral"` |
| **Social Views** | Total views from social media traffic | `CALCULATE([Total Views], Fact_Press_Analytics[Channel_Group] IN {"Organic Social", "Social"})` | `Channel_Group IN {"Organic Social", "Social"}` |
| **Press Release Views** | Total views for press releases only | `CALCULATE([Total Views], Fact_Press_Analytics[Page_Type] = "Press Release")` | `Page_Type = "Press Release"` |
| **Landing Page Views** | Total views for press room homepage only | `CALCULATE([Total Views], Fact_Press_Analytics[Page_Type] = "Landing Page")` | `Page_Type = "Landing Page"` |
| **Landing Page Share %** | Percentage of total views that are landing page views | `[Landing Page Views] / [Total Views]` | None (calculated) |
| **# Press Releases** | Count of distinct press releases | `CALCULATE(DISTINCTCOUNT(Fact_Press_Analytics[Page_URL]), Fact_Press_Analytics[Page_Type] = "Press Release")` | `Page_Type = "Press Release"` (locked) |
| | | **⚠️ WARNING:** `DISTINCTCOUNT(Page_URL)` can overcount if URLs have tracking params, localization, or alternate slugs. For production, use a canonical key: `ReleaseURL_Canonical` or `Dim_Press_Releases[ReleaseID]` |
| **Avg Views per Release** | Average views per press release | `[Press Release Views] / [# Press Releases]` | Calculated |
| **Top 10 PR Views** | Views from top 10 press releases by views (fixed set across date range) | See DAX below | `Page_Type = "Press Release"` |
| **Remaining PR Views** | Views from all press releases except top 10 | `[Press Release Views] - [Top 10 PR Views]` | Calculated |
| **Top 10 Share** | Share of press release views from top 10 | `[Top 10 PR Views] / [Press Release Views]` | Calculated |
| **Top10 Series Value** | Switch measure for stacked chart | See DAX below | Dynamic based on series |

**🔒 TOP 10 DEFINITION (LOCKED):**
> **Top 10 is determined across the selected date range, then you show how that same Top 10 performs over time.** This ensures executive clarity - the Top 10 releases are fixed for the period, and the chart shows how their share changes month-by-month. The chart title reflects this: "Top 10 vs Remaining Share (Over Time)".

---

## 2.2 Required DAX Measures

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

// # Press Releases (count with filter)
# Press Releases =
CALCULATE(
    DISTINCTCOUNT(Fact_Press_Analytics[Page_URL]),
    Fact_Press_Analytics[Page_Type] = "Press Release"
)

// Press Release Users
Press Release Users =
CALCULATE(
    [Total Users],
    Fact_Press_Analytics[Page_Type] = "Press Release"
)

// Landing Page Users
Landing Page Users =
CALCULATE(
    [Total Users],
    Fact_Press_Analytics[Page_Type] = "Landing Page"
)
```

### Channel Measures

```dax
// Organic Search Views
Organic Search Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Channel_Group] = "Organic Search"
)

// Direct Views
Direct Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Channel_Group] = "Direct"
)

// Referral Views
Referral Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Channel_Group] = "Referral"
)

// Social Views (includes both "Organic Social" and "Social" categories)
Social Views =
CALCULATE(
    [Total Views],
    Fact_Press_Analytics[Channel_Group] IN {"Organic Social", "Social"}
)
```

### Top 10 Measures

```dax
// Top 10 PR Views (top 10 calculation - fixed set across date range)
// Top 10 is determined across the selected date range, then shown over time
// Production-safe version using SELECTCOLUMNS + TREATAS
// CRITICAL: REMOVEFILTERS on chart axis time grain (Month_Year) to prevent "Top 10 per month" bug
Top 10 PR Views =
VAR Top10Base =
    CALCULATETABLE(
        SUMMARIZE(
            Fact_Press_Analytics,
            Fact_Press_Analytics[Page_URL],
            "__Views", SUM(Fact_Press_Analytics[Views])
        ),
        Fact_Press_Analytics[Page_Type] = "Press Release",
        REMOVEFILTERS(Dim_Date[Month_Year])  -- Ignores chart's month grouping, retains date slicer
    )
VAR Top10 =
    TOPN(10, Top10Base, [__Views], DESC)
VAR Top10Urls =
    SELECTCOLUMNS(Top10, "Page_URL", Fact_Press_Analytics[Page_URL])
RETURN
    CALCULATE(
        SUM(Fact_Press_Analytics[Views]),
        Fact_Press_Analytics[Page_Type] = "Press Release",
        TREATAS(Top10Urls, Fact_Press_Analytics[Page_URL])
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

**🔒 TOP-N RANKING RULE (LOCKED):**
> **Top-N ranking table must remove filters from the chart axis time grain (ex: `Month_Year`) while retaining date slicer selection.** This ensures the Top 10 set is fixed across the selected date range, not recalculated per month.

### Top 10 Table Filter Measure

```dax
// Is Top 10 Release (filter measure for Top Releases Table)
Is Top 10 Release =
VAR url = SELECTEDVALUE(Fact_Press_Analytics[Page_URL])
VAR Top10Base =
    CALCULATETABLE(
        SUMMARIZE(
            Fact_Press_Analytics,
            Fact_Press_Analytics[Page_URL],
            "__Views", SUM(Fact_Press_Analytics[Views])
        ),
        Fact_Press_Analytics[Page_Type] = "Press Release",
        REMOVEFILTERS(Dim_Date[Month_Year]),
        REMOVEFILTERS(Dim_Date[YearMonth])
    )
VAR Top10 =
    TOPN(10, Top10Base, [__Views], DESC)
VAR Top10Urls =
    SELECTCOLUMNS(Top10, "Page_URL", Fact_Press_Analytics[Page_URL])
RETURN
IF(NOT ISBLANK(url) && CONTAINS(Top10Urls, [Page_URL], url), 1, 0)
```

**🔒 TOP RELEASES TABLE RULE (LOCKED):**
> **Visual-level filter:** `Metrics[Is Top 10 Release] = 1`  
> **Sort:** `Metrics[Press Release Views]` descending  
> This ensures the table shows exactly the same Top 10 set as the stacked chart.

### Helper Table

```dax
// Top10_Series helper table (with SortOrder for legend ordering)
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

**Configuration:** Set `Top10_Series[Series]` → **Sort by column** → `Top10_Series[SortOrder]` to ensure correct legend order.

---

# 📄 BLOCK 3: PAGE SPECS

## 3.1 Page 1: Executive Overview

### KPIs (6 total)

| # | Label | Measure | Format |
|---|-------|---------|--------|
| 1 | Total Views | `Metrics[Total Views]` | `#,0` |
| 2 | Total Users | `Metrics[Total Users]` | `#,0` |
| 3 | Landing Page Share of Views | `Metrics[Landing Page Share %]` | `0.0%` |
| 4 | # Press Releases | `Metrics[# Press Releases]` | `#,0` |
| 5 | Avg Views per Release | `Metrics[Avg Views per Release]` | `#,0` |
| 6 | Top 10 Share | `Metrics[Top 10 Share]` | `0.0%` |

### Visuals

#### Visual 1: Top 10 vs Remaining Share Chart
- **Type:** 100% Stacked Column Chart
- **Title:** "Top 10 vs Remaining Share (Over Time)"
- **Field Wells:** See Build Recipes (4.1)

#### Visual 2: Top Releases Table (Top 10)
- **Type:** Table
- **Purpose:** Enable drillthrough to Release Detail page
- **Columns:**
  - `Page_Title` (visible) - **Fallback:** `Page_URL` if `Dim_Press_Releases` missing
  - `Metrics[Press Release Views]` (visible, sorted descending)
  - `Page_URL` (hidden, used for drillthrough)
- **Rows:** Top 10 press releases by views (matches Top 10 definition)
- **Visual-Level Filter:** `Metrics[Is Top 10 Release] = 1` (locked)
- **Sort:** `Metrics[Press Release Views]` descending (locked)
- **Drillthrough:** Enabled on table rows → Release Detail page

### Filters

- **Global Date Filter:** Last 90 days (default)
- **Page-Level Filters:** None (all data)

### Drillthrough

- **From:** Visuals that include `Page_URL` in context (table/bar of releases, Top Releases list, etc.)
  - **⚠️ CRITICAL:** KPI cards and the "Top 10 vs Remaining" chart do **not** carry `Page_URL` context and cannot trigger drillthrough
  - **Required Visual:** Top Releases Table (Top 10) with `Page_URL` (hidden), `Page_Title`, `Metrics[Press Release Views]`
- **To:** Release Detail page
- **Field:** `Fact_Press_Analytics[Page_URL]`

---

## 3.2 Page 2: Press Releases

### KPIs (4 total)

| # | Label | Measure | Format |
|---|-------|---------|--------|
| 1 | Total PR Views | `Metrics[Press Release Views]` | `#,0` |
| 2 | Total PR Users | `Metrics[Press Release Users]` | `#,0` |
| 3 | # Press Releases | `Metrics[# Press Releases]` | `#,0` |
| 4 | Avg Views per Release | `Metrics[Avg Views per Release]` | `#,0` |

### Visuals

- **Search-Enabled Table:** Press releases with search/filter capabilities
- **Slicers:** Date range, Category (if available)
- **Charts:** No charts in v2.4 (locked scope)

### Filters

- **Global Date Filter:** Last 90 days (default)
- **Page-Level Filter:** `Page_Type = "Press Release"` (locked)

### Search/Filter

- **Search Method:** Slicer search on `Page_Title` or `Page_URL`
- **Filter Options:** Date range, Category, Channel Group

### Drillthrough

- **From:** Table rows
- **To:** Release Detail page
- **Field:** `Fact_Press_Analytics[Page_URL]`

---

## 3.3 Page 3: Channel Performance

### KPIs (5 total)

| # | Label | Measure | Format |
|---|-------|---------|--------|
| 1 | Total Views | `Metrics[Total Views]` | `#,0` |
| 2 | Organic Search Views | `Metrics[Organic Search Views]` | `#,0` |
| 3 | Direct Views | `Metrics[Direct Views]` | `#,0` |
| 4 | Referral Views | `Metrics[Referral Views]` | `#,0` |
| 5 | Social Views | `Metrics[Social Views]` | `#,0` |

### Visuals

- **Channel Share Chart:** Donut or bar chart
- **Channel Over Time:** Line or column chart
- **Channel Performance Matrix:** Table or matrix

### Filters

- **Global Date Filter:** Last 90 days (default)
- **Page-Level Filter:** **All press room page types** (default)
  - **Optional:** Slicer toggle to filter to Press Releases only
  - **Rationale:** Channel analysis benefits from seeing all traffic sources, with option to focus on press releases

### Field Wells: See Build Recipes (4.2)

---

## 3.4 Page 4: Press Home Performance

### KPIs (3 total)

| # | Label | Measure | Format |
|---|-------|---------|--------|
| 1 | Landing Page Views | `Metrics[Landing Page Views]` | `#,0` |
| 2 | Landing Page Users | `Metrics[Landing Page Users]` | `#,0` |
| 3 | Landing Page Share of Views | `Metrics[Landing Page Share %]` | `0.0%` |

### Visuals

- **Landing Page Trend:** Line or column chart (daily views)
- **Traffic Sources:** Donut or bar chart (channels to landing page)

### Filters

- **Global Date Filter:** Last 90 days (default)
- **Page-Level Filter:** `Page_Type = "Landing Page"` (locked - press homepage only)

---

## 3.5 Page 5: Release Detail (Drillthrough)

### Purpose

Deep-dive page for individual press releases, accessed via drillthrough from other pages.

### Required Visuals

#### KPI Strip (3-4 KPIs)
- **Views:** `Metrics[Total Views]` (filtered to this release)
- **Users:** `Metrics[Total Users]` (filtered to this release)
- **Avg Time on Page:** (if available)
- **Bounce Rate:** (if available)

#### Trend Chart
- **Type:** Line chart
- **Title:** "Daily Views (Last 30 Days)"
- **X-axis:** `Dim_Date[Date]`
- **Y-axis:** `Metrics[Total Views]`
- **Filter:** This release only
- **Date Override:** Visual-level relative date filter = Last 30 days (overrides global "Last 90 days" for this chart only)

#### Referrers/Channels Chart
- **Type:** Bar or donut chart
- **Title:** "Traffic Sources"
- **Legend/Axis:** `Fact_Press_Analytics[Channel_Group]`
- **Values:** `Metrics[Total Views]`
- **Filter:** This release only

#### Metadata Table
- **Columns:**
  - Title (`Dim_Press_Releases[Page_Title]`)
  - Publish Date (`Dim_Press_Releases[Publish_Date]`)
  - Category (`Dim_Press_Releases[Category]`)
  - URL (`Fact_Press_Analytics[Page_URL]`)

### Drillthrough Contract

- **Drillthrough Field (Preferred):** `Dim_Press_Releases[Page_URL]` or `Dim_Press_Releases[ReleaseID]` (if dimension exists)
- **Drillthrough Field (Fallback):** `Fact_Press_Analytics[Page_URL]` (if dimension not available)
- **Source Pages:** Executive Overview, Press Releases
- **Trigger:** Table row or data point **only from visuals that include `Page_URL` in context** (e.g., Top Releases table, Releases table)
  - **⚠️ CRITICAL:** KPI cards and charts without `Page_URL` context cannot trigger drillthrough
- **Filter Applied:** `Fact_Press_Analytics[Page_URL] = [Selected Value]` (or dimension equivalent)

---

## 3.6 Page 6: Metric Dictionary

### Purpose

Reference page with metric definitions and glossary.

### Content

- **Table:** Metric definitions (name, definition, formula, filter context)
- **Organized by:** Category (Core KPIs, Distribution, Trends, etc.)

### Access

- **Navigation:** Info icon (i) in header or nav rail bottom
- **Not in main navigation:** Hidden from primary nav

---

## 3.7 Global Filter Standards

### Default Date Filter

- **Scope:** Global (applies to all pages unless overridden)
- **Default:** **Last 90 days**
- **Slicer:** Date range slicer on all pages
- **Format:** `Dim_Date[Date]` between [Start Date] and [End Date]

### Page-Level Filter Rules

| Page | Filter Rule | Locked? |
|------|-------------|---------|
| Executive Overview | None (all data) | Yes |
| Press Releases | `Page_Type = "Press Release"` | Yes |
| Channel Performance | All press room page types (default), optional slicer to filter to Press Releases only | Yes |
| Press Home Performance | `Page_Type = "Landing Page"` | Yes |
| Release Detail | `Page_URL = [Drillthrough Value]` | Yes (drillthrough) |

**⚠️ JSON Filter String Format:**
> **Filter values in JSON must be quote-safe.** Use escaped quotes: `"Page_Type = \"Press Release\""` (not `"Page_Type = Press Release"`). This prevents "it compiles but doesn't filter" issues in automation.

### Filter DSL Contract (Automation Config → PBIR Filter Object)

**Purpose:** Translate internal DSL filter strings to Power BI PBIR filter objects.

**DSL Format (Internal Config):**
- `Page_Type = "Press Release"` → Categorical In filter
- `Page_Type IN {"Press Release", "Landing Page"}` → Categorical In filter with multiple values

**PBIR Filter Object Structure:**
```json
{
  "filters": [
    {
      "name": "Fact_Press_Analytics[Page_Type]",
      "type": "Categorical",
      "filter": {
        "And": [
          {
            "Left": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Fact_Press_Analytics"
                },
                "Property": "Page_Type"
              }
            },
            "ComparisonKind": 0,
            "Right": {
              "Literal": {
                "Value": "Press Release"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Generator Rule:**
- Config field refs use `Table[Column]` and `Metrics[Measure]`
- Generator converts to PBIR `queryRef`/`nativeQueryRef` per Visual Contract library
- All filters must compile to PBIR `filter` objects (not string literals)

**Recommended Structured Config Format:**
```json
"pageLevel": [
  { 
    "field": "Fact_Press_Analytics[Page_Type]", 
    "op": "IN", 
    "values": ["Press Release"] 
  }
]
```

---

# 🔧 BLOCK 4: BUILD RECIPES

**📘 For complete, precise visual generation instructions, see:** `PRECISE_VISUAL_GENERATION_METHOD.md`

This section provides high-level field well configurations. The precise method document contains:
- Exact JSON templates for each visual type
- Step-by-step generation algorithms
- Field mapping rules
- Validation checklists
- Position calculation formulas

---

## 4.1 Top 10 vs Remaining Share Chart

### Visual Type
**100% Stacked Column Chart**

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **X-axis** | `Dim_Date[Month_Year]` | Column | Time series (monthly) |
| **Sort By** | `Dim_Date[YearMonth]` | Column | **CRITICAL:** Sort `Month_Year` by `YearMonth` to prevent alphabetical sorting |
| **Legend** | `Top10_Series[Series]` | Column | "Top 10" vs "Remaining" |
| **Y-axis** | `Metrics[Top10 Series Value]` | Measure | Switch measure |
| **Tooltips** | `Metrics[Top 10 PR Views]` | Measure | Additional context |
| | `Metrics[Remaining PR Views]` | Measure | Additional context |
| | `Metrics[Press Release Views]` | Measure | Additional context |
| | `Metrics[Top 10 Share]` | Measure | Additional context |

### Configuration

```json
{
  "visualType": "hundredPercentStackedColumnChart",
  "title": "Top 10 vs Remaining Share (Over Time)",
  "bindings": {
    "xAxis": "Dim_Date[Month_Year]",
    "legend": "Top10_Series[Series]",
    "yAxis": "Metrics[Top10 Series Value]",
    "tooltips": [
      "Metrics[Top 10 PR Views]",
      "Metrics[Remaining PR Views]",
      "Metrics[Press Release Views]",
      "Metrics[Top 10 Share]"
    ]
  }
}
```

### Generation Notes

- **Projection Order:** X-axis (0), Legend (1), Y-axis (2), Tooltips (3+)
- **Sort Definition:** MUST sort `Month_Year` by `YearMonth` (Ascending)
- **All Projections:** MUST have `active: true`
- **Visual Container Objects:** Required (background, border, visualHeader, title)
- **See:** `PRECISE_VISUAL_GENERATION_METHOD.md` Section 2 for complete template

---

## 4.2 Channel Share Distribution Chart

### Visual Type
**Donut Chart** (or **Bar Chart**)

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **Legend** | `Fact_Press_Analytics[Channel_Group]` | Column | Channel categories |
| **Values** | `Metrics[Total Views]` | Measure | Primary metric |
| **Tooltips** | `Metrics[Total Users]` | Measure | Additional context |

### Configuration

```json
{
  "visualType": "donutChart",
  "title": "Channel Share Distribution",
  "bindings": {
    "legend": "Fact_Press_Analytics[Channel_Group]",
    "values": "Metrics[Total Views]",
      "tooltips": [
        "Metrics[Total Users]"
      ]
  }
}
```

---

## 4.3 Channel Over Time Chart

### Visual Type
**Line Chart** (or **Clustered Column Chart**)

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **X-axis** | `Dim_Date[Date]` | Column | Daily granularity |
| **Legend** | `Fact_Press_Analytics[Channel_Group]` | Column | Channel series |
| **Y-axis** | `Metrics[Total Views]` | Measure | Primary metric |
| **Tooltips** | `Metrics[Total Users]` | Measure | Additional context |

### Configuration

```json
{
  "visualType": "lineChart",
  "title": "Channel Performance Over Time",
  "bindings": {
    "xAxis": "Dim_Date[Date]",
    "legend": "Fact_Press_Analytics[Channel_Group]",
    "yAxis": "Metrics[Total Views]",
    "tooltips": [
      "Metrics[Total Users]"
    ]
  }
}
```

---

## 4.4 Landing Page Trend Chart

### Visual Type
**Line Chart** (or **Column Chart**)

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **X-axis** | `Dim_Date[Date]` | Column | Daily granularity |
| **Y-axis** | `Metrics[Landing Page Views]` | Measure | Primary metric |
| **Tooltips** | `Metrics[Landing Page Users]` | Measure | Additional context |

### Configuration

```json
{
  "visualType": "lineChart",
  "title": "Landing Page Views Trend",
  "bindings": {
    "xAxis": "Dim_Date[Date]",
    "yAxis": "Metrics[Landing Page Views]",
    "tooltips": [
      "Metrics[Landing Page Users]"
    ]
  }
}
```

---

## 4.5 KPI Card Template

### Visual Type
**Card**

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **Fields** | `Metrics[Measure Name]` | Measure | Single measure |

### Configuration

```json
{
  "visualType": "card",
  "bindings": {
    "fields": [
      {
        "measure": "Metrics[{{MEASURE_NAME}}]",
        "label": "{{LABEL}}",
        "format": "{{FORMAT}}"
      }
    ]
  },
  "visualContainerObjects": {
    "background": [...],
    "border": [...],
    "visualHeader": [...]
  }
}
```

### Generation Notes

- **Projection:** Single measure in bucket role name observed in baseline exported PBIR specimen for `card` visual type
  - **⚠️ NOTE:** Bucket role names differ by visual type/version. Do not assume "Data" vs "Values" without verifying against exported `visual.json` sample.
- **Field Type:** MUST be `Measure` (never `Column`)
- **Visual Container Objects:** Required (background, border, visualHeader)
- **Position:** Standard KPI card size: 184px × 88px
- **See:** `PRECISE_VISUAL_GENERATION_METHOD.md` Section 1 for complete template

---

## 4.6 Slicer Template

### Visual Type
**Slicer**

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **Values** | `Dim_Date[Date]` | Column | Date range slicer |
| | `Fact_Press_Analytics[Channel_Group]` | Column | Channel slicer |
| | `Dim_Press_Releases[Category]` | Column | Category slicer |

### Configuration

### Generation Notes

- **Query State:** Use `Values` bucket (not `Data`)
- **Projection:** Single column projection
- **Visual Container Objects:** Minimal (most properties `show: false`)
- **Filter Config:** Required (type: "Categorical")
- **Sort Definition:** Required (sort by column, Ascending)
- **Date Slicer:** Special case - requires date range objects
- **See:** `PRECISE_VISUAL_GENERATION_METHOD.md` Section 3 for complete template

```json
{
  "visualType": "slicer",
  "bindings": {
    "values": "{{TABLE_NAME}}[{{COLUMN_NAME}}]"
  },
  "objects": {
    "data": [...],
    "general": [...],
    "header": [...]
  },
  "visualContainerObjects": {
    // Minimal - background, border, padding only
  }
}
```

---

## 4.7 Search-Enabled Table

### Visual Type
**Table**

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **Columns** | `Dim_Press_Releases[Page_Title]` | Column | Searchable |
| | `Dim_Press_Releases[Publish_Date]` | Column | Sortable |
| | `Metrics[Total Views]` | Measure | Sortable |
| | `Metrics[Total Users]` | Measure | Sortable |
| **Search** | Slicer search on `Page_Title` | Column | Text filter |

### Configuration

**Note:** Power BI doesn't have a true "search box" visual. Use:
- **Slicer with search enabled** on `Page_Title` or `Page_URL`
- **Text filter** on table columns
- **Custom visual** (if available)

---

## 4.8 Top Releases Table (Top 10)

### Visual Type
**Table**

### Field Well Recipe

| Well | Field | Type | Notes |
|------|-------|------|-------|
| **Columns** | `Page_Title` (or `Page_URL` if `Dim_Press_Releases` missing) | Column | Visible, display name |
| | `Metrics[Press Release Views]` | Measure | Visible, sorted descending |
| | `Page_URL` | Column | Hidden, used for drillthrough |

### Configuration

```json
{
  "visualType": "table",
  "title": "Top 10 Press Releases",
  "bindings": {
    "columns": [
      { "field": "Page_Title", "visible": true },
      { "field": "Metrics[Press Release Views]", "visible": true, "sort": "desc" },
      { "field": "Page_URL", "visible": false }
    ]
  },
  "filter": {
    "measure": "Metrics[Is Top 10 Release]",
    "value": 1
  },
  "drillthrough": {
    "enabled": true,
    "targetPage": "release_detail",
    "field": "Page_URL"
  }
}
```

### Generation Notes

- **Visual-Level Filter:** `Metrics[Is Top 10 Release] = 1` (locked)
- **Sort:** `Metrics[Press Release Views]` descending (locked)
- **Fallback:** If `Dim_Press_Releases[Page_Title]` missing, use `Fact_Press_Analytics[Page_URL]` as display column
- **Drillthrough:** Enabled on table rows → Release Detail page
- **See:** Section 2.2 for `Is Top 10 Release` measure definition

---

# ✅ VALIDATION CHECKLIST

## Pre-Implementation

- [x] Landing Page scope locked (press_home only)
- [x] Page names finalized and locked
- [x] KPI labels refined (Top 10 Share, not Top 10 %)
- [x] Navigation labels confirmed
- [x] Footer: no page numbers, "INTERNAL USE ONLY"
- [x] Header height: 56px (federal readability)
- [x] Info icon placement: header right
- [x] Field wells clarified (X-axis = columns, Y-axis = measures)
- [x] Measure contract defined
- [x] Filter standards locked
- [x] Drillthrough contract defined
- [x] Naming conventions locked

## DAX Measures Required

- [ ] `Press Release Views` (base measure)
- [ ] `Landing Page Views` (base measure)
- [ ] `Landing Page Share %` (calculated)
- [ ] `Press Release Users` (base measure)
- [ ] `Landing Page Users` (base measure)
- [ ] `# Press Releases` (count with filter)
- [ ] `Organic Search Views` (channel measure)
- [ ] `Direct Views` (channel measure)
- [ ] `Referral Views` (channel measure)
- [ ] `Social Views` (channel measure)
- [ ] `Top 10 PR Views` (top 10 calculation - fixed set)
- [ ] `Remaining PR Views` (remainder)
- [ ] `Top 10 Share` (percentage for KPI)
- [ ] `Top10 Series Value` (switch measure for chart)

## Helper Tables Required

- [ ] `Top10_Series` (2-row table: "Top 10", "Remaining" with SortOrder column)
- [ ] `Dim_Date[Month_Year]` column (if not exists)
- [ ] `Dim_Date[YearMonth]` column (numeric sort key: `YEAR([Date]) * 100 + MONTH([Date])`)
  - **Critical:** Sort `Month_Year` by `YearMonth` to prevent alphabetical sorting

## Visual Configuration

- [ ] Top 10 vs Remaining chart uses 100% Stacked Column
- [ ] All field wells configured per Build Recipes
- [ ] All visuals have `active: true` in projections
- [ ] All cards have `visualContainerObjects`
- [ ] All slicers have minimal `visualContainerObjects`
- [ ] `Top10_Series[Series]` sorted by `Top10_Series[SortOrder]`
- [ ] `Dim_Date[Month_Year]` sorted by `Dim_Date[YearMonth]`

---

# 🚀 AUTOMATION-READY CONFIGURATION

## JSON Configuration

```json
{
  "report": {
    "canvas": { "width": 1280, "height": 720 },
    "grid": { "margin": 20, "gap": 20 },
    "header": { 
      "height": 56, 
      "showInfoIcon": true, 
      "infoTargetPage": "metric_dictionary" 
    },
    "footer": { 
      "height": 24, 
      "showPageNumber": false, 
      "centerText": "INTERNAL USE ONLY" 
    }
  },
  "decisions": {
    "landingScope": "press_home",
    "defaultDateFilter": "last_90_days"
  },
  "naming": {
    "tablePrefix": {
      "dimension": "Dim_",
      "fact": "Fact_"
    },
    "measureTable": "Metrics",
    "columnFormat": "PascalCase_Underscore",
    "visualFormat": "snake_case"
  },
  "navigation": {
    "railWidth": 56,
    "items": [
      { "order": 1, "label": "Overview", "targetPage": "home", "icon": "home" },
      { "order": 2, "label": "Releases", "targetPage": "releases", "icon": "document" },
      { "order": 3, "label": "Channels", "targetPage": "channels", "icon": "chart" },
      { "order": 4, "label": "Press Home", "targetPage": "landing", "icon": "target" },
      { "order": 99, "label": "i", "targetPage": "metric_dictionary", "icon": "info", "placement": "bottom" }
    ]
  },
  "pages": [
    {
      "id": "home",
      "displayName": "Executive Overview",
      "type": "standard",
      "titleText": "Press Room Analytics",
      "filters": {
        "global": ["date_last_90_days"],
        "pageLevel": []
      },
      "kpis": [
        { "label": "Total Views", "measure": "Metrics[Total Views]", "format": "#,0" },
        { "label": "Total Users", "measure": "Metrics[Total Users]", "format": "#,0" },
        { "label": "Landing Page Share of Views", "measure": "Metrics[Landing Page Share %]", "format": "0.0%" },
        { "label": "# Press Releases", "measure": "Metrics[# Press Releases]", "format": "#,0" },
        { "label": "Avg Views per Release", "measure": "Metrics[Avg Views per Release]", "format": "#,0" },
        { "label": "Top 10 Share", "measure": "Metrics[Top 10 Share]", "format": "0.0%", "tooltip": "Share of total Press Release Views coming from the top 10 releases by views." }
      ],
      "visuals": [
        {
          "id": "top10_vs_remaining",
          "type": "hundredPercentStackedColumnChart",
          "title": "Top 10 vs Remaining Share (Over Time)",
          "recipe": "4.1"
        },
        {
          "id": "top_releases_table",
          "type": "table",
          "title": "Top 10 Press Releases",
          "recipe": "4.8",
          "columns": [
            { "field": "Page_Title", "visible": true, "fallback": "Page_URL" },
            { "field": "Metrics[Press Release Views]", "visible": true, "sort": "desc" },
            { "field": "Page_URL", "visible": false }
          ],
          "filter": "Metrics[Is Top 10 Release] = 1",
          "drillthrough": { "enabled": true, "targetPage": "release_detail" }
        }
      ]
    },
    {
      "id": "releases",
      "displayName": "Press Releases",
      "type": "standard",
      "filters": {
        "global": ["date_last_90_days"],
        "pageLevel": ["Page_Type = \"Press Release\""]
      }
    },
    {
      "id": "channels",
      "displayName": "Channel Performance",
      "type": "standard",
      "filters": {
        "global": ["date_last_90_days"],
        "pageLevel": []
      }
    },
    {
      "id": "landing",
      "displayName": "Press Home Performance",
      "type": "standard",
      "filters": {
        "global": ["date_last_90_days"],
        "pageLevel": ["Page_Type = \"Landing Page\""]
      }
    },
    {
      "id": "release_detail",
      "displayName": "Release Detail",
      "type": "drillthrough",
      "showInNav": false,
      "drillthroughField": "Fact_Press_Analytics[Page_URL]",
      "requiredVisuals": ["kpi_strip", "trend_chart", "referrers_chart", "metadata_table"]
    },
    {
      "id": "metric_dictionary",
      "displayName": "Metric Dictionary",
      "type": "reference",
      "showInNav": false
    }
  ]
}
```

---

# 📎 APPENDIX: PBIR GENERATOR GUARDRAILS

**Purpose:** Hard contracts that prevent silent failures and schema violations during PBIR generation.

## A.1 Visual Identity Contracts

- **Visual folder name == visual.json.name:** Must be identical (enforced by validator)
- **Required directory structure:** `pages/<pageId>/visuals/<visualId>/visual.json`
- **Required files:** `pages.json`, `report.json`, `definition.pbir` must exist

## A.2 Binding Integrity Rules

- **Every projected field has valid queryRef:** Format `"Table.Field"` matching model exactly
- **queryRef table/field names match model exactly:** Case-sensitive validation
- **Measures not wrapped in aggregations:** Use explicit measure names, not `SUM(Table[Column])`

## A.3 Sorting Rule (Critical)

- **If sortDefinition references a field, that field must appear in projections:** Prevents "sort silently ignored" bug
- **Sort field must be Column (not Measure):** For time-based sorting (e.g., `YearMonth`)

## A.4 No Hallucinated Properties

- **Only emit properties observed in known-good samples OR Microsoft schema:**
  - Do not include: `drillFilterOtherVisuals`, `altText` (in visualContainerObjects), `description`/`fromCardinality`/`toCardinality` (in relationships.tmdl)
  - Verify against exported PBIP samples before adding new properties

## A.5 Filter DSL Contract

- **Config field refs use `Table[Column]` and `Metrics[Measure]`:** Internal DSL format
- **Generator converts to PBIR queryRef/nativeQueryRef:** Per Visual Contract library
- **All filters must compile to PBIR filter objects:** Not string literals

## A.6 Top-N Ranking Rule

- **Top-N ranking table must remove filters from chart axis time grain:** Use `REMOVEFILTERS(Dim_Date[Month_Year])` to prevent "Top 10 per month" bug
- **Retain date slicer selection:** Only remove axis grain, not global date filter

## A.7 JSON Syntax Rules

- **No comments in JSON:** `/* */` and `//` cause hard failures
- **UTF-8 encoding, no BOM:** Power BI chokes on BOM

---

# 📝 CHANGE LOG

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-01-08 | Complete restructure into 4 locked blocks | Organization and clarity |
| 2026-01-08 | Removed "Top 10 %" recommendation entirely | Eliminate ambiguity |
| 2026-01-08 | Added formal definition for "Landing Page Share" | Prevent executive questions |
| 2026-01-08 | Locked Page 4 name to "Press Home Performance" | Match scope decision |
| 2026-01-08 | Header height confirmed 56px | Federal readability standard |
| 2026-01-08 | Added Measure Contract section | Shared language for wireframe/DAX |
| 2026-01-08 | Added Field Well Recipes | Prevent field well confusion |
| 2026-01-08 | Added Page-Level Filter Standards | Prevent filter drift |
| 2026-01-08 | Added Naming Conventions | Automation consistency |
| 2026-01-08 | Added Drillthrough Contract | Prevent broken drillthrough |
| 2026-01-08 | Fixed "search box" terminology | Power BI accuracy |
| 2026-01-08 | Fixed "z-index" to "Selection Pane layering" | Power BI accuracy |
| 2026-01-08 | Added tooltip definition for Top 10 Share | Executive clarity |
| 2026-01-08 | Fixed Top 10 PR Views DAX (per-URL aggregation) | Prevent "same values" bug |
| 2026-01-08 | Fixed # Press Releases formula (added filter) | Match filter context |
| 2026-01-08 | Enhanced Page_Type logic (LOWER, .html check) | Prevent misclassification |
| 2026-01-08 | Added SortOrder to Top10_Series table | Correct legend ordering |
| 2026-01-08 | Added YearMonth sort key for Month_Year | Prevent alphabetical sorting |
| 2026-01-08 | Removed all TBD items | Locked specification |
| 2026-01-08 | Added terminology note (Landing Page vs Press Home) | Prevent confusion |
| 2026-01-08 | Replaced "federal readability" with specific rules | Measurable standards |
| 2026-01-08 | Locked drillthrough field (prefer dimension) | Best practice |
| 2026-01-08 | Added missing measure definitions (Users, Channel measures) | Complete measure contract |
| 2026-01-08 | Added Page_Type classification warning | Production safety |
| 2026-01-08 | Locked Top 10 definition (fixed set across date range) | Executive clarity |
| 2026-01-08 | Added Users additivity warning | Prevent double-counting confusion |
| 2026-01-08 | Promoted sorting constraint to global rule | Prevent alphabetical sorting |
| 2026-01-08 | Fixed Top 10 DAX (SELECTCOLUMNS + TREATAS) | Prevent "blank chart" silent failure |
| 2026-01-08 | Locked Channel dimension to Fact table everywhere | Prevent field binding mismatches |
| 2026-01-08 | Fixed filter string quoting in JSON | Prevent "compiles but doesn't filter" issues |
| 2026-01-08 | Fixed drillthrough contract (removed KPI cards/chart, added Top Releases Table) | Prevent silent drillthrough failures |
| 2026-01-08 | Fixed Top 10 DAX (added REMOVEFILTERS for Month_Year) | Prevent "Top 10 per month" bug |
| 2026-01-08 | Removed "Engagement Rate" from tooltips | Eliminate TBD references |
| 2026-01-08 | Added Filter DSL Contract section | Formal translation from config to PBIR filters |
| 2026-01-08 | Added URL canonicalization guidance | Handle `/press-room/`, query strings, hash fragments |
| 2026-01-08 | Added canonical key warning for # Press Releases | Prevent overcounting from URL variants |
| 2026-01-08 | Fixed card bucket naming to be sample-driven | Prevent PBIR version-specific failures |
| 2026-01-08 | Fixed Release Detail date filter conflict (30 vs 90 days) | Clarify visual-level override mechanism |
| 2026-01-08 | Added Model Prerequisites section | Enable generator early validation |
| 2026-01-08 | Added FieldRef grammar clarification | Document DSL → PBIR conversion |
| 2026-01-08 | Added Appendix: PBIR Generator Guardrails | Centralized hard contracts reference |
| 2026-01-08 | Fixed Page_Type DAX (proper query string stripping, ENDS-WITH pattern matching) | Prevent landing page matching all press-room URLs |
| 2026-01-08 | Removed Engagement Rate from Build Recipe 4.2 tooltips | Eliminate remaining TBD references |
| 2026-01-08 | Fixed drillthrough trigger in Release Detail section | Consistent with Page 1 correction |
| 2026-01-08 | Added Is Top 10 Release measure and locked table filter rule | Ensure Top Releases Table matches chart Top 10 set |
| 2026-01-08 | Locked Page 2 charts scope (no charts in v2.4) | Remove "to be specified" ambiguity |
| 2026-01-08 | Added Dim_Press_Releases to Model Prerequisites (optional) | Document fallback behavior |
| 2026-01-08 | Added Top Releases Table to automation JSON and Build Recipes | Complete automation-ready config |

---

**Status:** 🔒 **LOCKED FOR IMPLEMENTATION**  
**Next Step:** Build generation scripts using this specification
