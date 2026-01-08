# 🎯 FINAL DASHBOARD SPECIFICATION

**Version:** 2.3 LOCKED  
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

### Filters

- **Global Date Filter:** Last 90 days (default)
- **Page-Level Filters:** None (all data)

### Drillthrough

- **From:** KPI cards, chart
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
- **Charts:** Press release performance charts (to be specified in future iteration)

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
- **Trigger:** Click on KPI card, chart data point, or table row
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
| | `Metrics[Engagement Rate]` | Measure | If available |

### Configuration

```json
{
  "visualType": "donutChart",
  "title": "Channel Share Distribution",
  "bindings": {
    "legend": "Fact_Press_Analytics[Channel_Group]",
    "values": "Metrics[Total Views]",
    "tooltips": [
      "Metrics[Total Users]",
      "Metrics[Engagement Rate]"
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

- **Projection:** Single measure in `Data` bucket (not `Values`)
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

---

**Status:** 🔒 **LOCKED FOR IMPLEMENTATION**  
**Next Step:** Build generation scripts using this specification
