# 📝 DECISIONS LOG

**Purpose:** Record of all key decisions made during dashboard specification  
**Status:** Final decisions locked ✅

---

## 🔒 FINAL DECISIONS (January 7, 2026)

### Decision 1: Landing Page Naming

**Question:** Should Page 4 be "Landing Page Performance" or "Press Home Performance"?

**Analysis:**
- Reviewed TMDL model: `Fact_Press_Analytics[Page_Type]`
- Found logic: `IF(CONTAINSSTRING(Page_URL, "/press-room/index"), "Landing Page", ...)`
- **Finding:** Only `/press-room/index.html` is tagged as "Landing Page"

**Decision:** **Press Home Performance**

**Rationale:**
- Accurately describes what's being measured (press homepage only)
- Not all entry pages (which would be "Landing Page Performance")
- Eliminates confusion with GA4 landing page dimension

**Configuration:**
```json
"landingScope": "press_home"
```

---

### Decision 2: Top 10 KPI Label

**Question:** Should KPI be "Top 10 %" or "Top 10 Share"?

**Issue:** "Top 10 %" is ambiguous - could mean:
- Top 10 percentile (90th percentile)
- Share of views from top 10 releases

**Decision:** **Top 10 Share**

**Rationale:**
- Eliminates ambiguity
- "Share" clearly means proportion/percentage
- Prevents executive meeting questions
- Professional terminology

---

### Decision 3: Footer Page Numbers

**Question:** Should footer show "Page 1 of 5"?

**Decision:** **No page numbers**

**Rationale:**
- Power BI is not PowerPoint
- Modern dashboard design omits page numbers
- Replace with "INTERNAL USE ONLY" classification

---

### Decision 4: Metric Dictionary Access

**Question:** Should "Metric Dictionary" be in main navigation?

**Decision:** **No - use info icon (i) instead**

**Rationale:**
- Don't waste prime nav rail space
- Still discoverable via info icon
- Common pattern in modern dashboards
- Placement: Header right or nav rail bottom

---

### Decision 5: Page Names

**Question:** What should each page be named?

**Decisions:**

| Page | Final Name | Rejected Options | Rationale |
|------|------------|------------------|-----------|
| 1 | **Executive Overview** | "HOME: Executive Summary", "Dashboard Overview", "Performance Summary" | Professional, clear purpose, federal standard |
| 2 | **Press Releases** | "All Press Releases", "Release Catalog" | Concise, clear, matches HHS patterns |
| 3 | **Channel Performance** | "Channel Attribution", "Traffic Sources", "Channel Analysis" | Consistent with performance theme |
| 4 | **Press Home Performance** | "Landing Page Performance", "Entry Point Analysis" | Accurate to data model scope |
| 5 | **Release Detail** | "Press Release Detail", "Release Analytics" | Standard drillthrough naming |
| 6 | **Metric Dictionary** | *(unchanged)* | Clear reference page name |

---

### Decision 6: Navigation Labels

**Question:** What should navigation buttons say?

**Decisions:**

| Button | Final Label | Rejected Options | Rationale |
|--------|-------------|------------------|-----------|
| 1 | **Overview** | "Home", "Dashboard", "Summary" | More professional than "Home" |
| 2 | **Releases** | "Press Releases", "All Releases" | Concise, clear |
| 3 | **Channels** | "Channel Performance", "Traffic" | Short, recognizable |
| 4 | **Press Home** | "Landing", "Homepage", "Entry" | Specific, not ambiguous |

---

### Decision 7: KPI Labels (Page 1)

**Question:** How should KPIs be labeled?

**Decisions:**

| KPI | Final Label | Rejected Options | Rationale |
|-----|-------------|------------------|-----------|
| 1 | **Total Views** | *(unchanged)* | Standard, clear |
| 2 | **Total Users** | *(unchanged)* | Standard, clear |
| 3 | **Landing Page Share of Views** | "Landing Page %", "% Landing Page" | Explicit, unambiguous |
| 4 | **# Press Releases** | "Press Releases", "Count of Releases" | Count symbol clear |
| 5 | **Avg Views per Release** | "Avg per Release", "Avg Views/Release" | Concise, clear |
| 6 | **Top 10 Share** | "Top 10 %", "Top 10 Percentile" | Eliminates ambiguity |

---

### Decision 8: Top 10 vs Remaining Chart

**Question:** How should this chart be structured?

**Decisions:**

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Visual Type** | 100% Stacked Column | Best for share over time |
| **X-axis** | `Dim_Date[Month_Year]` (column) | Time series, monthly granularity |
| **Legend** | `Top10_Series[Series]` (column) | Two series: "Top 10", "Remaining" |
| **Y-axis** | `Metrics[Top10 Series Value]` (measure) | Switch measure for dynamic values |
| **Tooltips** | 4 supporting measures | Context for hover details |

**Required Infrastructure:**
- 5 new measures (see `MEASURES_TO_ADD.dax`)
- 1 helper table (`Top10_Series`)
- 1 new column (`Dim_Date[Month_Year]`, if needed)

---

### Decision 9: Field Wells Clarification

**Question:** Why "Non-measure field required" error on X-axis?

**Finding:** Power BI field wells have strict type requirements:

| Well | Accepts | Purpose |
|------|---------|---------|
| **X-axis** | **Columns only** | Category field |
| **Y-axis** | **Measures** | Values to plot |
| **Legend** | **Columns only** | Series split |
| **Tooltips** | **Measures** | Hover context |

**Decision:** Document this clearly in spec and guide

**Impact:** Prevents common configuration errors

---

## 📊 DESIGN PRINCIPLES APPLIED

1. **Professional & Clear** - Names immediately understandable
2. **Concise** - Short but descriptive
3. **Consistent** - Follow patterns throughout
4. **User-Focused** - What users actually call things
5. **HHS Standards** - Align with HHS.gov terminology
6. **Unambiguous** - Eliminate confusion (e.g., "Top 10 Share" not "Top 10 %")

---

## 🎯 CONFIGURATION FLAGS

For future flexibility, key decisions are configurable:

```json
{
  "naming": {
    "landingScope": "press_home",  // or "all_entry_points"
    "landingDisplayName": {
      "press_home": "Press Home Performance",
      "all_entry_points": "Landing Page Performance"
    }
  },
  "footer": {
    "showPageNumber": false,
    "centerText": "INTERNAL USE ONLY"
  },
  "header": {
    "showInfoIcon": true,
    "infoTargetPage": "metric_dictionary"
  }
}
```

---

## 📈 IMPACT ANALYSIS

### User Experience Improvements
- ✅ Clearer page names (no "HOME:" prefix)
- ✅ Unambiguous KPI labels (Top 10 Share)
- ✅ Discoverable metric definitions (info icon)
- ✅ Modern design (no page numbers)

### Technical Improvements
- ✅ Accurate naming (Press Home vs Landing Page)
- ✅ Clear field well requirements (column vs measure)
- ✅ Configurable for future changes

### Stakeholder Benefits
- ✅ Professional appearance
- ✅ No confusing terminology
- ✅ Easy to understand at a glance
- ✅ Aligned with federal standards

---

## 🔄 CHANGE HISTORY

| Date | Decision | Changed From | Changed To | Reason |
|------|----------|--------------|------------|--------|
| 2026-01-07 | KPI #6 label | "Top 10 %" | "Top 10 Share" | Eliminate percentile ambiguity |
| 2026-01-07 | Page 4 name | "Landing Page Performance" | "Press Home Performance" | Match data model scope |
| 2026-01-07 | Footer | Page numbers | "INTERNAL USE ONLY" | Modern design + classification |
| 2026-01-07 | Metric Dictionary access | Main nav | Info icon (i) | Don't waste nav space |
| 2026-01-07 | Nav button 1 | "Home" | "Overview" | More professional |
| 2026-01-07 | KPI #3 label | "Landing Page %" | "Landing Page Share of Views" | More explicit |

---

## ✅ SIGN-OFF

**Specification Status:** 🔒 LOCKED  
**Approved By:** Executive review (implied by user refinements)  
**Date:** January 7, 2026  
**Next Step:** Implementation (see `IMPLEMENTATION_GUIDE.md`)

---

## 📝 NOTES FOR FUTURE CHANGES

### If Landing Page Scope Changes
If you later need to analyze **all entry pages** (not just press homepage):

1. Update `landingScope` to `"all_entry_points"`
2. Update Page 4 display name to "Landing Page Performance"
3. Update nav label to "Landing"
4. Add DAX logic to identify entry pages from GA4 data
5. Update measure filters from `Page_Type = "Landing Page"` to new logic

### If Top 10 Definition Changes
If "Top 10" should be top 10 by a different metric (e.g., users instead of views):

1. Update `Top 10 PR Views` measure calculation
2. Update tooltip measures
3. Update KPI description
4. Test chart displays correctly

---

**Document Status:** ✅ Complete  
**Last Updated:** January 7, 2026
