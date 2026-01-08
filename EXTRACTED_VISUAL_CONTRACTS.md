# Extracted Visual Contracts from Microsoft-Certified Samples

**Date:** 2026-01-08  
**Evidence Source:** `dashboards/11_Power_BI_Examples/Store Sales.pbip` (Microsoft-certified) + `press-room-dashboard.pbip` (observed)  
**Schema Match:** ✅ Visual schema 2.4.0, Report schema 3.0.0 (matches press-room)

---

## PHASE 0: SAMPLE SELECTION

### Selected Sample Set

**Primary Source:** `dashboards/11_Power_BI_Examples/Store Sales.pbip`
- ✅ Visual schema: `2.4.0` (matches press-room)
- ✅ Report schema: `3.0.0` (matches press-room)
- ✅ Microsoft-certified Power BI example
- **Path:** `dashboards/11_Power_BI_Examples/Store Sales.Report/definition/pages/ReportSectiona9cc27467b93abd98c40/visuals/28e166680a992ae270ad/visual.json`

**Supporting Source:** `press-room-dashboard.pbip` (observed patterns)
- ✅ Visual schema: `2.4.0`
- ✅ Report schema: `3.0.0`
- ✅ Contains lineChart, donutChart, hundredPercentStackedBarChart, slicer

---

## PHASE 1: EXTRACTED CONTRACTS

### A. Canonical visualType Strings (Exact Case)

**✅ CONFIRMED from Samples:**

| Visual Type | Exact String | Source File |
|------------|--------------|-------------|
| card | `"card"` | Store Sales: `28e166680a992ae270ad/visual.json` |
| lineChart | `"lineChart"` | press-room: `lifecycle_trend/visual.json` |
| donutChart | `"donutChart"` | press-room: `channel_share/visual.json` |
| hundredPercentStackedBarChart | `"hundredPercentStackedBarChart"` | press-room: `top10_vs_remaining/visual.json` |
| slicer | `"slicer"` | press-room: `79f5f9f9ae9d08a9c70b/visual.json` |

**⚠️ CONDITIONAL:** Spec references `"hundredPercentStackedColumnChart"` but actual visual type is `"hundredPercentStackedBarChart"` (Bar, not Column). Generator must map spec name to actual type.

---

### B. Chart Query Structure (queryState Buckets & Role Names)

**✅ CONFIRMED from Samples:**

#### Card Visual

**QueryState Bucket:** `"Values"` (NOT "Data")

**Source:** `Store Sales.Report/.../28e166680a992ae270ad/visual.json` (lines 15-32)

```json
"queryState": {
  "Values": {
    "projections": [
      {
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Sales" } },
            "Property": "This Year Sales"
          }
        },
        "queryRef": "Sales.This Year Sales"
      }
    ]
  }
}
```

**Role Buckets:** Single bucket `"Values"` with measure projection.

---

#### Line Chart

**QueryState Buckets:** `"Category"`, `"Y"`

**Source:** `press-room-dashboard.Report/.../lifecycle_trend/visual.json` (lines 15-52)

```json
"queryState": {
  "Category": {
    "projections": [
      {
        "field": {
          "Column": {
            "Expression": { "SourceRef": { "Entity": "Dim_Date" } },
            "Property": "Date"
          }
        },
        "queryRef": "Dim_Date.Date",
        "nativeQueryRef": "Date",
        "active": true
      }
    ]
  },
  "Y": {
    "projections": [
      {
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Metrics" } },
            "Property": "Press Release Views"
          }
        },
        "queryRef": "Metrics.Press Release Views",
        "nativeQueryRef": "Press Release Views"
      }
    ]
  }
}
```

**Role Buckets:** `"Category"` (X-axis), `"Y"` (values).

---

#### Donut Chart

**QueryState Buckets:** `"Category"`, `"Y"`

**Source:** `press-room-dashboard.Report/.../channel_share/visual.json` (lines 15-52)

```json
"queryState": {
  "Category": {
    "projections": [
      {
        "field": {
          "Column": {
            "Expression": { "SourceRef": { "Entity": "Fact_Press_Analytics" } },
            "Property": "Channel_Group"
          }
        },
        "queryRef": "Fact_Press_Analytics.Channel_Group",
        "nativeQueryRef": "Channel_Group",
        "active": true
      }
    ]
  },
  "Y": {
    "projections": [
      {
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Metrics" } },
            "Property": "Press Release Views"
          }
        },
        "queryRef": "Metrics.Press Release Views",
        "nativeQueryRef": "Press Release Views"
      }
    ]
  }
}
```

**Role Buckets:** `"Category"` (legend/grouping), `"Y"` (values).

---

#### 100% Stacked Bar Chart

**QueryState Buckets:** `"Category"`, `"Series"`, `"Y"`

**Source:** `press-room-dashboard.Report/.../top10_vs_remaining/visual.json` (lines 97-153)

```json
"queryState": {
  "Category": {
    "projections": [
      {
        "field": {
          "Column": {
            "Expression": { "SourceRef": { "Entity": "Chart_Category" } },
            "Property": "Category"
          }
        },
        "queryRef": "Chart_Category.Category",
        "nativeQueryRef": "Category",
        "active": true
      }
    ]
  },
  "Series": {
    "projections": [
      {
        "field": {
          "Column": {
            "Expression": { "SourceRef": { "Entity": "Top10_Series" } },
            "Property": "Series"
          }
        },
        "queryRef": "Top10_Series.Series",
        "nativeQueryRef": "Series",
        "active": true
      }
    ]
  },
  "Y": {
    "projections": [
      {
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "Metrics" } },
            "Property": "Top10 Series Value"
          }
        },
        "queryRef": "Metrics.Top10 Series Value",
        "nativeQueryRef": "Top10 Series Value"
      }
    ]
  }
}
```

**Role Buckets:** `"Category"` (X-axis), `"Series"` (legend), `"Y"` (values).

---

### C. Measures with Spaces (queryRef / nativeQueryRef Formatting)

**✅ CONFIRMED from Samples:**

#### Pattern 1: Store Sales Sample (Card)

**Measure:** `"This Year Sales"` (spaces preserved)

**Source:** `Store Sales.Report/.../28e166680a992ae270ad/visual.json` (lines 26-29)

```json
{
  "Property": "This Year Sales",
  "queryRef": "Sales.This Year Sales"
}
```

**Note:** This sample does NOT include `nativeQueryRef` for the measure (only `queryRef`).

---

#### Pattern 2: Press-Room Dashboard (Chart - Line/Donut)

**Measure:** `"Press Release Views"` (spaces preserved)

**Source:** `press-room-dashboard.Report/.../channel_share/visual.json` (lines 45-49)

```json
{
  "Property": "Press Release Views",
  "queryRef": "Metrics.Press Release Views",
  "nativeQueryRef": "Press Release Views"
}
```

---

#### Pattern 3: Press-Room Dashboard (Chart - Stacked Bar)

**Measure:** `"Top10 Series Value"` (spaces preserved)

**Source:** `press-room-dashboard.Report/.../top10_vs_remaining/visual.json` (lines 146-150)

```json
{
  "Property": "Top10 Series Value",
  "queryRef": "Metrics.Top10 Series Value",
  "nativeQueryRef": "Top10 Series Value"
}
```

**Extracted Rule:**
- ✅ `queryRef`: `"TableName.Measure Name"` (dot notation, spaces preserved, no escaping)
- ✅ `nativeQueryRef`: `"Measure Name"` (measure name only, spaces preserved, no escaping)
- ✅ Pattern: `queryRef` = `"{{TABLE}}.{{MEASURE}}"`, `nativeQueryRef` = `"{{MEASURE}}"`

---

### D. sortDefinition Patterns for Charts

**✅ CONFIRMED from Samples:**

#### Donut Chart Sort Pattern

**Source:** `press-room-dashboard.Report/.../channel_share/visual.json` (lines 54-70)

```json
"sortDefinition": {
  "sort": [
    {
      "field": {
        "Measure": {
          "Expression": { "SourceRef": { "Entity": "Metrics" } },
          "Property": "Press Release Views"
        }
      },
      "direction": "Descending"
    }
  ],
  "isDefaultSort": true
}
```

**Key Findings:**
- ✅ Chart can sort by measure (not just column)
- ✅ Sort field (`"Press Release Views"`) appears in `"Y"` projections
- ✅ Sort field reference matches projection field exactly

---

#### Stacked Bar Chart Sort Pattern

**Source:** `press-room-dashboard.Report/.../top10_vs_remaining/visual.json` (lines 155-172)

```json
"sortDefinition": {
  "sort": [
    {
      "field": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "Top10_Series" } },
          "Property": "SortOrder"
        }
      },
      "direction": "Ascending"
    }
  ],
  "isDefaultSort": true
}
```

**Key Findings:**
- ✅ Chart can sort by column (sort key, not display column)
- ✅ Sort field (`SortOrder`) does NOT appear in projections (hidden sort key)
- ⚠️ **CONDITIONAL:** May be chart-type specific (stacked bar allows hidden sort key, donut sorts by visible measure)

---

### E. Slicer Requirements

**✅ CONFIRMED from Press-Room Dashboard:**

**Source:** `press-room-dashboard.Report/.../79f5f9f9ae9d08a9c70b/visual.json` (lines 204-277)

#### visualContainerObjects Presence

**✅ CONFIRMED:** Slicer HAS `visualContainerObjects` in press-room-dashboard sample:

```json
"visualContainerObjects": {
  "background": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "title": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "visualHeader": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "border": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "padding": [{ "properties": { "top": { "expr": { "Literal": { "Value": "0D" } } } } }]
}
```

**⚠️ CONTRADICTION FIX:** Previous evidence report stated "NOT ALLOWED for slicers" - this is INCORRECT. Slicers CAN have `visualContainerObjects` (at least in schema 2.4.0).

---

#### filterConfig Presence

**✅ CONFIRMED:** Slicer has `filterConfig`:

**Source:** `press-room-dashboard.Report/.../79f5f9f9ae9d08a9c70b/visual.json` (lines 280-297)

```json
"filterConfig": {
  "filters": [
    {
      "name": "4202e540e256e30923ec",
      "field": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "Dim_Date" } },
          "Property": "Date"
        }
      },
      "type": "Categorical"
    }
  ]
}
```

**Required Fields:**
- `name` (unique ID string)
- `field` (Column or Measure reference)
- `type` (e.g., `"Categorical"`, `"Advanced"`)

---

### F. tabOrder Patterns

**✅ CONFIRMED from Observed Samples:**

**Source:** `press-room-dashboard.Report/definition/pages/*/visuals/*/visual.json`

**Observed tabOrder values:**
- `5`, `6`, `1000`, `2000`, `2500`, `3000`, `4000`, `5000`, `6000`, `7000`, `8000`, `9000`, `10000`, `15000`

**Observed z values:**
- `2`, `100`, `1000`, `2000`, `2500`, `3000`, `4000`, `5000`, `6000`, `7000`, `9000`, `10000`, `11000`, `15000`

**Key Findings:**
- ✅ `tabOrder` and `z` are **independent** (no fixed relationship like `tabOrder = z * 100`)
- ✅ `tabOrder` can be smaller or larger than `z`
- ✅ Both can be integers (no decimal pattern observed in sample)
- ⚠️ **CONDITIONAL:** Relationship may be application-specific or visual-type-specific (no universal rule)

---

## PHASE 2: AUDIT SUMMARY

### Statements Labeled as CONFIRMED

1. ✅ Card: queryState bucket = `"Values"` (not "Data")
2. ✅ Measures with spaces: `queryRef` = `"Table.Measure Name"`, `nativeQueryRef` = `"Measure Name"` (spaces preserved)
3. ✅ Chart role buckets: lineChart uses `"Category"`, `"Y"`; donutChart uses `"Category"`, `"Y"`; stacked bar uses `"Category"`, `"Series"`, `"Y"`
4. ✅ visualType strings: exact case confirmed (`"card"`, `"lineChart"`, `"donutChart"`, `"hundredPercentStackedBarChart"`, `"slicer"`)
5. ✅ Chart sortDefinition: Can reference fields in projections (donut example) OR hidden sort keys (stacked bar example)
6. ✅ Slicer: HAS `visualContainerObjects` (contradicts previous report)
7. ✅ Slicer: HAS `filterConfig` with required structure

### Statements Labeled as CONDITIONAL

1. ⚠️ Visual type mapping: Spec says `"hundredPercentStackedColumnChart"` but actual is `"hundredPercentStackedBarChart"` (Bar vs Column - may be chart orientation difference)
2. ⚠️ Chart sortDefinition: Can sort by hidden sort key (stacked bar) OR visible measure (donut) - behavior may be chart-type-specific
3. ⚠️ tabOrder relationship: No fixed relationship to `z` observed, but may vary by visual type or application logic

### Statements Labeled as UNVERIFIED

1. ❌ Card `nativeQueryRef`: Store Sales sample does NOT include `nativeQueryRef` for measures (only `queryRef`). Press-room charts do include it. May be optional for cards.
2. ❌ Line chart `sortDefinition`: No sortDefinition found in press-room lineChart sample (may be optional)

---

## OUTPUT: Sample File References

### Store Sales (Microsoft-Certified)

- **Card Visual:** `dashboards/11_Power_BI_Examples/Store Sales.Report/definition/pages/ReportSectiona9cc27467b93abd98c40/visuals/28e166680a992ae270ad/visual.json`
- **Report JSON:** `dashboards/11_Power_BI_Examples/Store Sales.Report/definition/report.json`
- **PBIP Root:** `dashboards/11_Power_BI_Examples/Store Sales.pbip`

### Press-Room Dashboard (Observed)

- **Slicer:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/79f5f9f9ae9d08a9c70b/visual.json`
- **Line Chart:** `press-room-dashboard.Report/definition/pages/release_detail/visuals/lifecycle_trend/visual.json`
- **Donut Chart:** `press-room-dashboard.Report/definition/pages/home/visuals/channel_share/visual.json`
- **Stacked Bar Chart:** `press-room-dashboard.Report/definition/pages/home/visuals/top10_vs_remaining/visual.json`

---

**End of Extracted Contracts**
