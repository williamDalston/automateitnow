# Complete queryState for `top10_vs_remaining` Stacked Chart

**Visual Type:** `hundredPercentStackedBarChart`  
**Purpose:** Schema smell test - full queryState structure for final review

---

## Complete queryState Structure

```json
{
  "queryState": {
    "Category": {
      "projections": [
        {
          "field": {
            "Column": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Dim_Date"
                }
              },
              "Property": "Month_Year"
            }
          },
          "queryRef": "Dim_Date.Month_Year",
          "nativeQueryRef": "Month_Year",
          "active": true
        },
        {
          "field": {
            "Column": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Dim_Date"
                }
              },
              "Property": "YearMonth"
            }
          },
          "queryRef": "Dim_Date.YearMonth",
          "nativeQueryRef": "YearMonth",
          "active": true
        }
      ]
    },
    "Series": {
      "projections": [
        {
          "field": {
            "Column": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Top10_Series"
                }
              },
              "Property": "Series"
            }
          },
          "queryRef": "Top10_Series.Series",
          "nativeQueryRef": "Series",
          "active": true
        },
        {
          "field": {
            "Column": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Top10_Series"
                }
              },
              "Property": "SortOrder"
            }
          },
          "queryRef": "Top10_Series.SortOrder",
          "nativeQueryRef": "SortOrder",
          "active": true
        }
      ]
    },
    "Y": {
      "projections": [
        {
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Metrics"
                }
              },
              "Property": "Top10 Series Value"
            }
          },
          "queryRef": "Metrics.Top10 Series Value",
          "nativeQueryRef": "Top10 Series Value",
          "active": true
        }
      ]
    },
    "Tooltips": {
      "projections": [
        {
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Metrics"
                }
              },
              "Property": "Top 10 PR Views"
            }
          },
          "queryRef": "Metrics.Top 10 PR Views",
          "nativeQueryRef": "Top 10 PR Views",
          "active": true
        },
        {
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Metrics"
                }
              },
              "Property": "Remaining PR Views"
            }
          },
          "queryRef": "Metrics.Remaining PR Views",
          "nativeQueryRef": "Remaining PR Views",
          "active": true
        },
        {
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Metrics"
                }
              },
              "Property": "Press Release Views"
            }
          },
          "queryRef": "Metrics.Press Release Views",
          "nativeQueryRef": "Press Release Views",
          "active": true
        },
        {
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": {
                  "Entity": "Metrics"
                }
              },
              "Property": "Top 10 Share"
            }
          },
          "queryRef": "Metrics.Top 10 Share",
          "nativeQueryRef": "Top 10 Share",
          "active": true
        }
      ]
    }
  },
  "sortDefinition": {
    "sort": [
      {
        "field": {
          "Column": {
            "Expression": {
              "SourceRef": {
                "Entity": "Dim_Date"
              }
            },
            "Property": "YearMonth"
          }
        },
        "direction": "Ascending"
      }
    ],
    "isDefaultSort": true
  }
}
```

---

## Contract Compliance Checklist

### ✅ Category Bucket
- [x] Display field: `Dim_Date.Month_Year` (first projection - display)
- [x] Sort key: `Dim_Date.YearMonth` (second projection - sort)
- [x] Both have `active: true`
- [x] Both have correct `queryRef` and `nativeQueryRef`

### ✅ Series Bucket
- [x] Display field: `Top10_Series.Series` (first projection - display)
- [x] Sort key: `Top10_Series.SortOrder` (second projection - for model-level sortByColumn)
- [x] Both have `active: true`
- [x] Both have correct `queryRef` and `nativeQueryRef`

### ✅ Y Bucket
- [x] Measure: `Metrics.Top10 Series Value`
- [x] Has `active: true`
- [x] Correct `queryRef` and `nativeQueryRef` (spaces preserved)

### ✅ Tooltips Bucket
- [x] 4 tooltip measures (all with spaces preserved)
- [x] All have `active: true`
- [x] All have correct `queryRef` and `nativeQueryRef`

### ✅ sortDefinition
- [x] Single field: `Dim_Date.YearMonth` (X-axis sorting)
- [x] Sort field appears in Category projections
- [x] Direction: `"Ascending"` (Title Case, matches observed samples)
- [x] `isDefaultSort: true`
- [x] **NOT** including SortOrder (relying on model-level sortByColumn for legend)

---

## Sorting Strategy

**X-axis (Category):**
- Visual-level `sortDefinition` sorts by `YearMonth` (numeric key)
- Display shows `Month_Year` (text label)
- Both fields in Category projections ✅

**Legend (Series):**
- Model-level `sortByColumn` on `Top10_Series[Series]` → `Top10_Series[SortOrder]`
- `SortOrder` included in Series projections for stability ✅
- **No visual-level sortDefinition for legend** (cleaner, more Power BI-native)

---

## ⚠️ Critical Model Requirement

### YearMonth Column Visibility

**REQUIRED:** `Dim_Date[YearMonth]` must be **hidden** in the semantic model.

**Why:**
- Category bucket includes two projections: `Month_Year` (display) and `YearMonth` (sort key)
- If `YearMonth` is visible, Power BI Desktop may treat it as a second axis level
- This can cause unwanted drill/hierarchy behavior in the chart

**Model Configuration:**
```tmdl
// In Dim_Date.tmdl
column 'YearMonth' {
    dataType: 'int64'
    isHidden: true  // ← MUST be hidden
    // ... other properties
}
```

**Verification:**
- Check TMDL: `Dim_Date.tmdl` should have `isHidden: true` for `YearMonth`
- If not hidden, Desktop may show it as a second axis level or create hierarchy behavior

---

## Complete Visual Query Wrapper Structure

**Full nesting context** for schema validation:

```json
{
  "visual": {
    "visualType": "hundredPercentStackedBarChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Dim_Date" } }, "Property": "Month_Year" } }, "queryRef": "Dim_Date.Month_Year", "nativeQueryRef": "Month_Year", "active": true },
            { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Dim_Date" } }, "Property": "YearMonth" } }, "queryRef": "Dim_Date.YearMonth", "nativeQueryRef": "YearMonth", "active": true }
          ]
        },
        "Series": {
          "projections": [
            { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Top10_Series" } }, "Property": "Series" } }, "queryRef": "Top10_Series.Series", "nativeQueryRef": "Series", "active": true },
            { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Top10_Series" } }, "Property": "SortOrder" } }, "queryRef": "Top10_Series.SortOrder", "nativeQueryRef": "SortOrder", "active": true }
          ]
        },
        "Y": {
          "projections": [
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Metrics" } }, "Property": "Top10 Series Value" } }, "queryRef": "Metrics.Top10 Series Value", "nativeQueryRef": "Top10 Series Value", "active": true }
          ]
        },
        "Tooltips": {
          "projections": [
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Metrics" } }, "Property": "Top 10 PR Views" } }, "queryRef": "Metrics.Top 10 PR Views", "nativeQueryRef": "Top 10 PR Views", "active": true },
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Metrics" } }, "Property": "Remaining PR Views" } }, "queryRef": "Metrics.Remaining PR Views", "nativeQueryRef": "Remaining PR Views", "active": true },
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Metrics" } }, "Property": "Press Release Views" } }, "queryRef": "Metrics.Press Release Views", "nativeQueryRef": "Press Release Views", "active": true },
            { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Metrics" } }, "Property": "Top 10 Share" } }, "queryRef": "Metrics.Top 10 Share", "nativeQueryRef": "Top 10 Share", "active": true }
          ]
        }
      },
      "sortDefinition": {
        "sort": [
          {
            "field": {
              "Column": {
                "Expression": { "SourceRef": { "Entity": "Dim_Date" } },
                "Property": "YearMonth"
              }
            },
            "direction": "Ascending"
          }
        ],
        "isDefaultSort": true
      }
    }
  }
}
```

**Key Points:**
- ✅ `queryState` is inside `visual.query.queryState`
- ✅ `sortDefinition` is inside `visual.query.sortDefinition` (sibling to `queryState`)
- ✅ Both are direct children of `query` object
- ✅ No `query` property inside `queryState` (common mistake)
- ✅ All projections fully expanded (no placeholders)

---

## Multi-Sort Decision (Confirmed)

**Question:** Can `sortDefinition.sort` contain multiple fields (YearMonth + SortOrder)?

**Answer:** 
- ✅ Schema allows it (it's an array)
- ⚠️ **But:** Power BI visuals typically behave like they have one active sort axis at a time
- ✅ **Decision:** Keep single-field sort (`YearMonth` only)
- ✅ **Legend sorting:** Rely on model-level `sortByColumn` for `Top10_Series[Series]` → `SortOrder`

**Rationale:**
- Multi-sort is "possible-but-not-reliable" unless observed in Microsoft-certified samples
- Model-level `sortByColumn` is cleaner and more Power BI-native
- Single-field `sortDefinition` is more stable across Desktop re-saves

---

## Potential Schema Smells to Check

1. **Bucket order:** Category → Series → Y → Tooltips (matches observed pattern) ✅
2. **Projection order within buckets:** Display field first, sort key second ✅
3. **Measure spacing:** All measures with spaces preserved correctly ✅
4. **active flag:** All projections have `active: true` ✅
5. **sortDefinition field type:** Column (not Measure) ✅
6. **Direction casing:** "Ascending" (Title Case) ✅
7. **YearMonth visibility:** Must be hidden in model ⚠️
8. **Query nesting:** `queryState` and `sortDefinition` are siblings under `query` ✅

---

## ✅ Final Schema Review Status

**Structural Status:** ✅ **PASSES** schema smell test

**Requirements:**
- [x] All buckets correctly structured
- [x] All projections have required properties
- [x] Sort field appears in projections
- [x] Single-field sortDefinition (no multi-sort)
- [x] Tooltips fully expanded (not placeholders)
- [ ] **VERIFY:** `Dim_Date[YearMonth]` is hidden in semantic model

**Ready for generation** (pending YearMonth visibility confirmation).
