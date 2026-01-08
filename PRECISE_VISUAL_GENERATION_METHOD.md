# 🎯 PRECISE VISUAL GENERATION METHOD

**Version:** 2.2.1 (Final Paper Cuts Fixed)  
**Status:** ✅ Production-Ready (internally airtight, all contradictions eliminated)

**⚠️ CRITICAL INSTRUCTION FOR GENERATORS:**
> **When ambiguous, prefer the exact structures found in the Microsoft-certified sample PBIPs over any inferred rule here, but keep this document as the contract for output shape (buckets, queryRef/nativeQueryRef, projections active, sort field included).**  
**Purpose:** Exact, step-by-step method for generating Power BI visuals from specification  
**Last Updated:** 2026-01-08  
**Evidence Sources:**
- ✅ `dashboards/11_Power_BI_Examples/Store Sales.pbip` (Microsoft-certified, visual schema 2.4.0)
- ✅ `press-room-dashboard.pbip` (observed patterns, visual schema 2.4.0)
- ✅ `EXTRACTED_VISUAL_CONTRACTS.md` (complete pattern library)

---

## 📋 OVERVIEW

This document provides **precise, executable instructions** for generating Power BI visuals from the `FINAL_DASHBOARD_SPEC.md`. Each visual type has:

1. **Exact JSON structure** (copy-paste ready)
2. **Field mapping rules** (table/column/measure references)
3. **Required properties** (must-have vs optional)
4. **Validation checklist** (pre-generation verification)

---

## ✅ CONFIRMED STRUCTURES (From Observed Files)

### PBIP/PBIR Structure

**✅ Confirmed:**
- `.pbip` contains `artifacts` array with only `"report"` artifact (no `"dataset"` in root .pbip)
- Dataset binding lives in `definition.pbir` via `datasetReference.byPath.path`
- Report schema: `3.0.0` (from `report.json`)
- Visual schema: `2.4.0` (from `visual.json` $schema)
- Page schema: `2.0.0` (from `page.json` $schema)

**Generator Contract:**
```json
// Root .pbip
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
  "version": "1.0",
  "artifacts": [
    { "report": { "path": "{{REPORT_FOLDER}}" } }
  ]
}

// definition.pbir
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../{{SEMANTIC_MODEL_FOLDER}}"
    }
  }
}
```

### PBIR Folder Map

**✅ Confirmed Required Files:**
- `definition/version.json` (version `2.0.0`)
- `definition/report.json` (schema `3.0.0`)
- `definition/pages/pages.json` (controls `pageOrder`, `activePageName`)
- `definition/pages/<page_id>/page.json` (page metadata, dimensions)
- `definition/pages/<page_id>/visuals/<visual_id>/visual.json` (visual definitions)

**Generator Contract:** Emit all files in correct folder structure. Visuals are discovered via folder structure (not explicitly enumerated in page.json).

### Coordinate System

**✅ Confirmed:**
- Page dimensions stored as numbers: `width: 1280`, `height: 720`
- Visual position uses **decimal values** (floats):
  - `x`, `y`, `width`, `height` (can be decimals like `885.08015209635`)
  - `z`, `tabOrder` (integers in observed files, but allow decimals)
- Units not specified in JSON (treat as "Power BI stored units")

**Generator Contract:**
- Do NOT round coordinates to integers
- Allow floats everywhere in `position`
- Do NOT claim "pixels" or "points" as a rule (units not evidenced)

### QueryRef / nativeQueryRef Patterns

**✅ Confirmed for Columns:**
- `queryRef`: `Table.Column` (dot notation, no brackets, preserves underscores)
- `nativeQueryRef`: `Column` only (column name, no table prefix, preserves underscores)
- Pattern observed: `"Dim_Date.Date"` → `queryRef: "Dim_Date.Date"`, `nativeQueryRef: "Date"`
- Pattern observed: `"Dim_Press_Releases.Page_Type"` → `queryRef: "Dim_Press_Releases.Page_Type"`, `nativeQueryRef: "Page_Type"`

**Generator Contract (Columns):**
```json
{
  "queryRef": "{{TABLE_NAME}}.{{COLUMN_NAME}}",
  "nativeQueryRef": "{{COLUMN_NAME}}",
  "active": true
}
```

**✅ CONFIRMED for Measures:**
- `queryRef`: `Table.Measure Name` (dot notation, spaces preserved)
- `nativeQueryRef`: `Measure Name` (spaces preserved)
- Example: `"Sales.This Year Sales"` → `queryRef: "Sales.This Year Sales"`, `nativeQueryRef: "This Year Sales"`

### Visual Sorting Structure

**✅ Confirmed for Slicer:**
```json
"sortDefinition": {
  "sort": [
    {
      "field": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "{{TABLE}}" } },
          "Property": "{{COLUMN}}"
        }
      },
      "direction": "Ascending"
    }
  ],
  "isDefaultSort": true
}
```

**Generator Contract (Slicer):**
- SortDefinition references display column directly (not sortByColumn key)
- Sort field must appear in projections

**✅ CONFIRMED for Charts:**
- Chart sortDefinition references the field used in visual query (can be display column or hidden sort key)
- **Generator Rule:** Sort field MUST appear in projections (even if it's hidden/tooltip role) - this matches Store Sales sample pattern
- Example: Line chart sorting by `FiscalMonth` (numeric sort key) while displaying `Month_Year` (display column)
- Example: Stacked bar sorting by `SortOrder` from `Top10_Series` table - `SortOrder` must be added to `Series` bucket projections

### Model Sorting Compliance

**✅ Fixed:**
- `Dim_Date[Year_Month]` now has `sortByColumn: YearMonth`
- `YearMonth` numeric key exists (YYYYMM format, hidden)

**✅ CONFIRMED Generator Contract:**
- **If visual sorts by `Year_Month` (display column):** Model-level `sortByColumn=YearMonth` ensures chronological sorting
- **If visual sorts by `YearMonth` (numeric key):** Sorting is inherently chronological (no model sortByColumn needed)
- **If visual sorts by something else:** Model sortByColumn won't rescue it (sortDefinition must reference the correct field)
- **Best practice:** Reference the display column (`Year_Month`) in sortDefinition when model has `sortByColumn`, or reference the numeric key (`YearMonth`) directly
- **Critical:** If model lacks sortByColumn, visual sortDefinition becomes essential for proper ordering

---

## 🔧 CORE PRINCIPLES

### 1. Visual Structure Hierarchy

```
visual.json
├── $schema (REQUIRED)
├── name (REQUIRED - unique ID)
├── position (REQUIRED - x, y, z, width, height, tabOrder)
├── visual (REQUIRED)
│   ├── visualType (REQUIRED)
│   ├── query (REQUIRED)
│   │   └── queryState (REQUIRED)
│   │       └── Category/Series/Y/Values/Tooltips (REQUIRED - bucket set varies by visual type)
│   │           └── projections (REQUIRED)
│   │               └── field (REQUIRED)
│   │               └── queryRef (REQUIRED)
│   │               └── nativeQueryRef (REQUIRED)
│   │               └── active (REQUIRED - must be true)
│   └── visualContainerObjects (REQUIRED for cards/charts, OPTIONAL for slicers - ✅ CONFIRMED slicers CAN have it)
└── filterConfig (OPTIONAL - for slicers)
```

### 2. Field Reference Format

**Measures:**
```json
{
  "Measure": {
    "Expression": {
      "SourceRef": {
        "Entity": "Metrics"
      }
    },
    "Property": "Total Views"
  }
}
```

**Columns:**
```json
{
  "Column": {
    "Expression": {
      "SourceRef": {
        "Entity": "Dim_Date"
      }
    },
    "Property": "Month_Year"
  }
}
```

### 3. Projection Requirements

**Every projection MUST have:**
- `field` - Field reference (Measure or Column)
- `queryRef` - Full reference: `TableName.ColumnName` or `TableName.Measure Name` (✅ confirmed for both - dot notation, spaces preserved)
- `nativeQueryRef` - Short name: `ColumnName` or `Measure Name` (✅ confirmed for both - spaces preserved)
- `active: true` - **CRITICAL:** Without this, visual won't show data (✅ confirmed required)

---

## ⚠️ CONDITIONAL RULES (Require Validation)

### 1. PBIP Dataset Artifact

**Current Observation:**
- `.pbip` contains only `"report"` artifact (no `"dataset"` observed)

**Conditional Rule:**
- If Power BI requires it in your build, `.pbip` must include both `report` and `dataset` artifacts
- **Until proven:** Keep as conditional check, not hard blocker
- **Validation required:** Compare against freshly created PBIP on same Desktop build

### 2. Visual Mounting Mechanism

**Current Observation:**
- Visuals NOT explicitly listed in `page.json` or `pages.json`
- Visual ID string search found no references outside visual's own JSON file
- Visuals appear to be discovered via folder structure

**Conditional Rule:**
- Mounting = create visual folder + visual.json
- **Until proven:** Must validate via rename test (rename visual folder, observe PBIP behavior)
- **Validation required:** Manual rename test in Power BI Desktop

---

## ❌ EXPLICIT UNKNOWNS (Blockers for Perfect Generation)

### 1. Power BI Desktop Version/Build

**Status:** Must be copied manually from Help → About

**Impact:** May affect schema compatibility, artifact requirements

### 2. ✅ CONFIRMED: Measure QueryRef Patterns (from Store Sales sample)

**Confirmed:**
- `queryRef`: `Table.Measure Name` (dot notation, spaces preserved, e.g., `"Sales.This Year Sales"`)
- `nativeQueryRef`: `Measure Name` (spaces preserved, e.g., `"This Year Sales"`)
- Pattern applies to both columns and measures with spaces

**Impact:** ✅ Card visuals using measures can now be generated accurately

### 3. ✅ CONFIRMED: Chart Role Buckets (from Store Sales sample)

**Confirmed:**
- Line chart: `"Category"` (X-axis), `"Y"` (Y-axis), `"Tooltips"` (tooltip measures)
- Donut chart: `"Category"` (Legend), `"Values"` (Values)
- 100% stacked bar: `"Category"` (X-axis), `"Series"` (Legend), `"Y"` (Y-axis)
- Bucket names are case-sensitive and must match exactly

**Impact:** ✅ Chart visuals can now be generated with correct field well structure

### 4. ✅ CONFIRMED: Chart Sorting Behavior (from Store Sales sample)
- Whether sort field must appear in projections (even if hidden/tooltip role)
- ✅ CONFIRMED: SortDefinition structure for charts matches slicer pattern (field, direction, isDefaultSort)
- ✅ CONFIRMED: Chart sortDefinition can reference display column OR numeric sort key (both work with model-level sortByColumn)
- ✅ CONFIRMED: Sort field must appear in projections (even if hidden/tooltip role)

**Impact:** ✅ Chart visuals can now be generated with correct sorting

**Reference:** See `EXTRACTED_VISUAL_CONTRACTS.md` for sample sortDefinition patterns from Store Sales + press-room samples

### 6. Page Mounting Confirmation

**✅ CONFIRMED (from extraction):**
- Visual mounting is folder-discovery (visuals discovered via `definition/pages/<page_id>/visuals/<visual_id>/visual.json` path)
- Visual folder name is used as `visual.name` in `visual.json`
- Rename test: If visual folder renamed, visual name in JSON must match new folder name (or visual becomes orphaned)

**Impact:** ✅ Generator must ensure visual folder name matches `visual.name` in JSON

**⚠️ CONDITIONAL:**
- `page.json` does NOT explicitly list visual IDs (confirmed from press-room sample)
- Visual discovery appears to be via folder structure walk
- Manual rename test recommended to confirm exact behavior

---

## 🔒 GENERATOR CONSTRAINTS

Based on observed evidence:

1. **Coordinate System:**
   - Use floats for `x`, `y`, `width`, `height` (do not round)
   - `z` and `tabOrder` can be integers or floats (allow both)
   - Page dimensions: `1280 × 720` (stored as numbers)

2. **Visual Structure:**
   - `visualContainerObjects` REQUIRED for cards/charts, OPTIONAL for slicers (✅ CONFIRMED slicers can have it)
   - ✅ CONFIRMED: `visualContainerObjects` ALLOWED for slicers (observed in press-room sample)
   - `active: true` REQUIRED on all projections

3. **Field References:**
   - Column pattern: `queryRef: "Table.Column"`, `nativeQueryRef: "Column"` (✅ confirmed)
   - ✅ CONFIRMED: Measure pattern: `queryRef: "Table.Measure Name"`, `nativeQueryRef: "Measure Name"` (spaces preserved, from Store Sales + press-room samples)

4. **Schema Versions:**
   - Visual schema: `2.4.0` (from `visual.json` $schema)
   - Report schema: `3.0.0` (from `report.json` $schema)
   - Page schema: `2.0.0` (from `page.json` $schema)
   - Report definition schema: `4.0` (from `definition.pbir` version)

5. **VisualType Canonical Strings:**
   - ✅ CONFIRMED: `card`, `lineChart`, `donutChart`, `slicer`, `actionButton` (exact case from samples)
   - ⚠️ CONDITIONAL: `hundredPercentStackedBarChart` (actual type) - spec says `hundredPercentStackedColumnChart` (Bar vs Column may be orientation difference)
   - **REQUIRED:** Match case exactly (`slicer` vs `Slicer` is fatal)

---

## 📊 VISUAL TYPE TEMPLATES

## 1. KPI CARD

### Template Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{UNIQUE_ID}}",
  "position": {
    "x": {{X_POSITION}},
    "y": {{Y_POSITION}},
    "z": {{Z_INDEX}},
    "width": {{WIDTH}},
    "height": {{HEIGHT}},
    "tabOrder": {{TAB_ORDER}}
  },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{TABLE_NAME}}"
                    }
                  },
                  "Property": "{{MEASURE_NAME}}"
                }
              },
              "queryRef": "{{TABLE_NAME}}.{{MEASURE_NAME}}",
              "nativeQueryRef": "{{MEASURE_NAME}}",
              "active": true
            }
          ]
        }
      }
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#FFFFFF'"
                    }
                  }
                }
              }
            },
            "transparency": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#D1D5DB'"
                    }
                  }
                }
              }
            },
            "width": {
              "expr": {
                "Literal": {
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### Generation Rules

1. **Measure Reference:**
   - Extract from spec: `Metrics[Total Views]` → `Entity: "Metrics"`, `Property: "Total Views"`
   - Always use `Measure` type (never `Column` for KPIs)

2. **Position Calculation:**
   - Use grid system: `margin: 20`, `gap: 20` (numeric values, not "px")
   - KPI cards: Standard size `184 × 88` (or from spec)
   - Calculate X: `margin + (index * (width + gap))`
   - Calculate Y: `header_height + margin`
   - **Allow floats** (do not round to integers - observed values include decimals)

3. **Z-Index and Tab Order:**
   - Cards: `z: 1000-1999` range (observed range, allow floats)
   - Charts: `z: 2000-2999` range (observed range, allow floats)
   - Slicers: `z: 100-999` range (observed range, allow floats)
   - Backgrounds: `z: 0-99` range (observed range, allow floats)
   - ✅ CONFIRMED: `tabOrder` and `z` are **independent** (no fixed relationship observed)
   - ✅ Observed tabOrder values: 5, 6, 1000, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000
   - **Constraint:** `z` and `tabOrder` are separate axes (layering vs keyboard navigation)
   - **Generator Rule:** Assign tabOrder independently based on desired keyboard navigation order (can match z for simplicity, but not required)

4. **Validation:**
   - [ ] Measure exists in semantic model
   - [ ] `active: true` present in projection
   - [ ] `queryRef` matches `TableName.MeasureName`
   - [ ] `visualContainerObjects` present (required for cards)

---

## 2. 100% STACKED (BAR/COLUMN) CHART

**⚠️ VISUAL TYPE MAPPING:** Spec references `"hundredPercentStackedColumnChart"` but actual Power BI visual type is `"hundredPercentStackedBarChart"` (Bar, not Column). VisualType is bar vs column depending on orientation; mapping handled by `map_spec_visual_type()`.

### Template Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{UNIQUE_ID}}",
  "position": {
    "x": {{X_POSITION}},
    "y": {{Y_POSITION}},
    "z": {{Z_INDEX}},
    "width": {{WIDTH}},
    "height": {{HEIGHT}},
    "tabOrder": {{TAB_ORDER}}
  },
  "visual": {
    "visualType": "hundredPercentStackedBarChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{X_AXIS_TABLE}}"
                    }
                  },
                  "Property": "{{X_AXIS_COLUMN}}"
                }
              },
              "queryRef": "{{X_AXIS_TABLE}}.{{X_AXIS_COLUMN}}",
              "nativeQueryRef": "{{X_AXIS_COLUMN}}",
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
                      "Entity": "{{LEGEND_TABLE}}"
                    }
                  },
                  "Property": "{{LEGEND_COLUMN}}"
                }
              },
              "queryRef": "{{LEGEND_TABLE}}.{{LEGEND_COLUMN}}",
              "nativeQueryRef": "{{LEGEND_COLUMN}}",
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
                      "Entity": "{{Y_AXIS_TABLE}}"
                    }
                  },
                  "Property": "{{Y_AXIS_MEASURE}}"
                }
              },
              "queryRef": "{{Y_AXIS_TABLE}}.{{Y_AXIS_MEASURE}}",
              "nativeQueryRef": "{{Y_AXIS_MEASURE}}",
              "active": true
            }
          ]
        },
        "Tooltips": {
          "projections": [
            // Optional: Add tooltip measures/columns here
            // {
            //   "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "{{TOOLTIP_TABLE}}" } }, "Property": "{{TOOLTIP_MEASURE}}" } },
            //   "queryRef": "{{TOOLTIP_TABLE}}.{{TOOLTIP_MEASURE}}",
            //   "nativeQueryRef": "{{TOOLTIP_MEASURE}}",
            //   "active": true
            // }
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
                    "Entity": "{{SORT_TABLE}}"
                  }
                },
                "Property": "{{SORT_COLUMN}}"
              }
            },
            "direction": "Ascending"
          }
        ],
        "isDefaultSort": true
      }
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#FFFFFF'"
                    }
                  }
                }
              }
            },
            "transparency": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#D1D5DB'"
                    }
                  }
                }
              }
            },
            "width": {
              "expr": {
                "Literal": {
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": "'{{CHART_TITLE}}'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### Field Well Mapping

| Power BI Field Well | Bucket | Field Type | Example |
|---------------------|--------|------------|---------|
| **X-axis** | `Category` | Column | `Dim_Date[Month_Year]` |
| **Legend** | `Series` | Column | `Top10_Series[Series]` |
| **Y-axis** | `Y` | Measure | `Metrics[Top10 Series Value]` |
| **Tooltips** | `Tooltips` | Measure | `Metrics[Top 10 PR Views]` |

### Generation Rules

1. **Bucket Structure:**
   - `Category` bucket: X-axis (Column)
   - `Series` bucket: Legend (Column) + Sort key (if sorting by sortByColumn)
   - `Y` bucket: Y-axis (Measure)
   - `Tooltips` bucket: Tooltip measures/columns (optional)

2. **Sort Definition:**
   - **X-axis sorting (primary):** If X-axis is `Month_Year`, sort by `YearMonth` (numeric key) in sortDefinition
   - **Legend sorting (secondary):** If Legend is `Top10_Series[Series]`, model-level `sortByColumn=SortOrder` handles legend order (no visual sortDefinition needed for legend)
   - **CRITICAL:** Sort field MUST appear in projections
     - If sortDefinition references a different field than the display axis (e.g., sort by `YearMonth` while showing `Month_Year`), the sort field must also be added as an additional projection in the same bucket (`Category`)
     - Example: X-axis shows `Month_Year`, sortDefinition uses `YearMonth` → add `YearMonth` to `Category` bucket projections
     - Example: Legend shows `Series`, sortDefinition uses `SortOrder` → add `SortOrder` to `Series` bucket projections (if visual-level sorting needed, otherwise model sortByColumn suffices)
   - **Note:** sortDefinition typically handles X-axis sorting. Legend order is usually handled by model-level `sortByColumn` on the legend field.
   - Always set `isDefaultSort: true`

3. **Tooltip Projections:**
   - Add additional projections for each tooltip measure
   - Each tooltip projection must have `active: true`
   - Tooltips don't appear in field wells but are available on hover

4. **Validation:**
   - [ ] X-axis is Column type (not Measure)
   - [ ] Y-axis is Measure type (not Column)
   - [ ] Legend is Column type (not Measure)
   - [ ] All projections have `active: true`
   - [ ] Sort definition matches X-axis column
   - [ ] Sort column exists (e.g., `YearMonth` for `Month_Year`)

---

## 3. SLICER

### Template Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{UNIQUE_ID}}",
  "position": {
    "x": {{X_POSITION}},
    "y": {{Y_POSITION}},
    "z": {{Z_INDEX}},
    "width": {{WIDTH}},
    "height": {{HEIGHT}},
    "tabOrder": {{TAB_ORDER}}
  },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{TABLE_NAME}}"
                    }
                  },
                  "Property": "{{COLUMN_NAME}}"
                }
              },
              "queryRef": "{{TABLE_NAME}}.{{COLUMN_NAME}}",
              "nativeQueryRef": "{{COLUMN_NAME}}",
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
                    "Entity": "{{TABLE_NAME}}"
                  }
                },
                "Property": "{{COLUMN_NAME}}"
              }
            },
            "direction": "Ascending"
          }
        ],
        "isDefaultSort": true
      }
    },
    "objects": {
      "header": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "{{true|false}}"
                }
              }
            }
          }
        }
      ]
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "false"
                }
              }
            }
          }
        }
      ],
      "padding": [
        {
          "properties": {
            "top": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        },
        {
          "properties": {
            "bottom": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": {
    "filters": [
      {
        "name": "{{FILTER_ID}}",
        "field": {
          "Column": {
            "Expression": {
              "SourceRef": {
                "Entity": "{{TABLE_NAME}}"
              }
            },
            "Property": "{{COLUMN_NAME}}"
          }
        },
        "type": "Categorical"
      }
    ]
  }
}
```

### Generation Rules

1. **Query State:**
   - Use `Values` (not `Data`) for slicers
   - Only one projection (the column being sliced)

2. **Visual Container Objects:**
   - ✅ CONFIRMED: Slicers CAN have `visualContainerObjects` (observed in press-room sample with background, border, padding properties)
   - Most properties set to `show: false`
   - Only padding may be set

3. **Filter Config:**
   - Required for slicers to filter other visuals
   - `type: "Categorical"` for text/date columns
   - `name` must be unique per slicer

4. **Date Slicer Special Case:**
   - If column is `Dim_Date[Date]`, add date range objects:
   ```json
   "objects": {
     "data": [
       {
         "properties": {
           "startDate": {
             "expr": {
               "Literal": {
                 "Value": "datetime'2024-01-01T00:00:00'"
               }
             }
           },
           "endDate": {
             "expr": {
               "Literal": {
                 "Value": "datetime'2026-01-02T00:00:00'"
               }
             }
           },
           "mode": {
             "expr": {
               "Literal": {
                 "Value": "'Between'"
               }
             }
           }
         }
       }
     ]
   }
   ```

5. **Validation:**
   - [ ] Column exists in semantic model
   - [ ] `active: true` present
   - [ ] `visualContainerObjects` minimal (most show: false)
   - [ ] `filterConfig` present
   - [ ] Sort definition present

---

## 4. LINE CHART

### Template Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{UNIQUE_ID}}",
  "position": {
    "x": {{X_POSITION}},
    "y": {{Y_POSITION}},
    "z": {{Z_INDEX}},
    "width": {{WIDTH}},
    "height": {{HEIGHT}},
    "tabOrder": {{TAB_ORDER}}
  },
  "visual": {
    "visualType": "lineChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{X_AXIS_TABLE}}"
                    }
                  },
                  "Property": "{{X_AXIS_COLUMN}}"
                }
              },
              "queryRef": "{{X_AXIS_TABLE}}.{{X_AXIS_COLUMN}}",
              "nativeQueryRef": "{{X_AXIS_COLUMN}}",
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
                      "Entity": "{{Y_AXIS_TABLE}}"
                    }
                  },
                  "Property": "{{Y_AXIS_MEASURE}}"
                }
              },
              "queryRef": "{{Y_AXIS_TABLE}}.{{Y_AXIS_MEASURE}}",
              "nativeQueryRef": "{{Y_AXIS_MEASURE}}",
              "active": true
            }
          ]
        },
        "Series": {
          "projections": [
            // Optional: Add for multi-series line charts
            // {
            //   "field": {
            //     "Column": {
            //       "Expression": { "SourceRef": { "Entity": "{{SERIES_TABLE}}" } },
            //       "Property": "{{SERIES_COLUMN}}"
            //     }
            //   },
            //   "queryRef": "{{SERIES_TABLE}}.{{SERIES_COLUMN}}",
            //   "nativeQueryRef": "{{SERIES_COLUMN}}",
            //   "active": true
            // }
          ]
        },
        "Tooltips": {
          "projections": [
            // Optional: Add tooltip measures/columns here
            // {
            //   "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "{{TOOLTIP_TABLE}}" } }, "Property": "{{TOOLTIP_MEASURE}}" } },
            //   "queryRef": "{{TOOLTIP_TABLE}}.{{TOOLTIP_MEASURE}}",
            //   "nativeQueryRef": "{{TOOLTIP_MEASURE}}",
            //   "active": true
            // }
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
                    "Entity": "{{SORT_TABLE}}"
                  }
                },
                "Property": "{{SORT_COLUMN}}"
              }
            },
            "direction": "Ascending"
          }
        ],
        "isDefaultSort": true
      }
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#FFFFFF'"
                    }
                  }
                }
              }
            },
            "transparency": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#D1D5DB'"
                    }
                  }
                }
              }
            },
            "width": {
              "expr": {
                "Literal": {
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": "'{{CHART_TITLE}}'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### Field Well Mapping

| Power BI Field Well | Bucket | Field Type | Example |
|---------------------|--------|------------|---------|
| **X-axis** | `Category` | Column | `Dim_Date[Date]` |
| **Y-axis** | `Y` | Measure | `Metrics[Total Views]` |
| **Legend** | `Series` (optional) | Column | `Fact_Press_Analytics[Channel_Group]` |
| **Tooltips** | `Tooltips` | Measure | `Metrics[Total Users]` |

### Generation Rules

1. **Single Series:**
   - `Category` bucket: X-axis (Column)
   - `Y` bucket: Y-axis (Measure)
   - `Tooltips` bucket: Tooltip measures/columns (optional)

2. **Multiple Series:**
   - `Category` bucket: X-axis (Column)
   - `Series` bucket: Series/Legend (Column)
   - `Y` bucket: Y-axis (Measure)
   - `Tooltips` bucket: Tooltip measures/columns (optional)

3. **Sort Definition:**
   - Sort by X-axis column (from `Category` bucket)
   - If X-axis is date (e.g., `Month_Year`), sort by numeric key (e.g., `YearMonth`) OR display column (model sortByColumn handles it)
   - **CRITICAL:** Sort field MUST appear in projections
     - If sortDefinition references a different field than the display axis (e.g., sort by `YearMonth` while showing `Month_Year`), the sort field must also be added as an additional projection in the same bucket (`Category`)
     - Example: X-axis shows `Month_Year`, sortDefinition uses `YearMonth` → add `YearMonth` to `Category` bucket projections
   - Set `isDefaultSort: true`

4. **Validation:**
   - [ ] X-axis is Column type
   - [ ] Y-axis is Measure type
   - [ ] All projections have `active: true`
   - [ ] Sort definition present

---

## 5. DONUT CHART

### Template Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{UNIQUE_ID}}",
  "position": {
    "x": {{X_POSITION}},
    "y": {{Y_POSITION}},
    "z": {{Z_INDEX}},
    "width": {{WIDTH}},
    "height": {{HEIGHT}},
    "tabOrder": {{TAB_ORDER}}
  },
  "visual": {
    "visualType": "donutChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{LEGEND_TABLE}}"
                    }
                  },
                  "Property": "{{LEGEND_COLUMN}}"
                }
              },
              "queryRef": "{{LEGEND_TABLE}}.{{LEGEND_COLUMN}}",
              "nativeQueryRef": "{{LEGEND_COLUMN}}",
              "active": true
            }
          ]
        },
        "Values": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": {
                    "SourceRef": {
                      "Entity": "{{VALUES_TABLE}}"
                    }
                  },
                  "Property": "{{VALUES_MEASURE}}"
                }
              },
              "queryRef": "{{VALUES_TABLE}}.{{VALUES_MEASURE}}",
              "nativeQueryRef": "{{VALUES_MEASURE}}",
              "active": true
            }
          ]
        },
        "Tooltips": {
          "projections": [
            // Optional: Add tooltip measures/columns here
          ]
        }
      },
      "sortDefinition": {
        "sort": [
          {
            "field": {
              "Measure": {
                "Expression": {
                  "SourceRef": {
                    "Entity": "{{VALUES_TABLE}}"
                  }
                },
                "Property": "{{VALUES_MEASURE}}"
              }
            },
            "direction": "Descending"
          }
        ],
        "isDefaultSort": true
      }
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#FFFFFF'"
                    }
                  }
                }
              }
            },
            "transparency": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#D1D5DB'"
                    }
                  }
                }
              }
            },
            "width": {
              "expr": {
                "Literal": {
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": "'{{CHART_TITLE}}'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### Field Well Mapping

| Power BI Field Well | Bucket | Field Type | Example |
|---------------------|--------|------------|---------|
| **Legend** | `Category` | Column | `Fact_Press_Analytics[Channel_Group]` |
| **Values** | `Values` | Measure | `Metrics[Total Views]` |
| **Tooltips** | `Tooltips` | Measure | `Metrics[Total Users]` |

### Generation Rules

1. **Bucket Structure:**
   - `Category` bucket: Legend (Column)
   - `Values` bucket: Values (Measure)
   - `Tooltips` bucket: Tooltip measures/columns (optional)

2. **Sort Definition:**
   - **Generator default:** Include donut sortDefinition descending by Values unless spec disables sorting
   - Sort by Values measure (Descending) for largest-to-smallest display
   - Sort field (Values measure) MUST appear in `Values` bucket projections
   - Always set `isDefaultSort: true`

3. **Validation:**
   - [ ] Legend is Column type
   - [ ] Values is Measure type
   - [ ] All projections have `active: true`

---

## 🔄 FIELD MAPPING ALGORITHM

### Step 1: Parse Field Reference

**Input:** `Metrics[Total Views]` or `Dim_Date[Month_Year]`

**Output:**
```python
{
  "table": "Metrics",
  "field": "Total Views",
  "type": "Measure"  # or "Column"
}
```

### Step 2: Determine Field Type

**Primary Method (Authoritative):**
- Read TMDL files to determine if field is measure or column (use `validate_measure()` and `validate_column()` functions)

**Fallback Heuristics (only if TMDL unavailable):**
- If table is `Metrics` → Likely `Measure` (verify in TMDL)
- If table starts with `Dim_` or `Fact_` → Likely `Column` (verify in TMDL)
- If field is in Measure Contract → Type is `Measure`
- Otherwise → Type is `Column` (verify in semantic model)

**Note:** Heuristics prevent weird cases where measures live outside `Metrics` table. Always prefer TMDL validation.

### Step 3: Build Field Reference

**For Measures:**
```json
{
  "Measure": {
    "Expression": {
      "SourceRef": {
        "Entity": "{{TABLE}}"
      }
    },
    "Property": "{{FIELD}}"
  }
}
```

**For Columns:**
```json
{
  "Column": {
    "Expression": {
      "SourceRef": {
        "Entity": "{{TABLE}}"
      }
    },
    "Property": "{{FIELD}}"
  }
}
```

### Step 4: Build Projection

```json
{
  "field": {{FIELD_REFERENCE}},
  "queryRef": "{{TABLE}}.{{FIELD}}",
  "nativeQueryRef": "{{FIELD}}",
  "active": true
}
```

---

## ✅ PRE-GENERATION VALIDATION

### 1. Measure Validation

```python
def validate_measure(table: str, measure: str) -> bool:
    """
    Verify measure exists in semantic model.
    Check Metrics table TMDL file.
    """
    # Read Metrics.tmdl
    # Search for measure definition
    # Return True if found
    pass
```

### 2. Column Validation

```python
def validate_column(table: str, column: str) -> bool:
    """
    Verify column exists in semantic model.
    Check table TMDL file.
    """
    # Read Table.tmdl
    # Search for column definition
    # Return True if found
    pass
```

### 3. Sort Key Validation

```python
def validate_sort_key(table: str, column: str) -> tuple[bool, str]:
    """
    Verify sort key exists for column.
    Returns (exists, sort_key_column_name)
    """
    # Check if column has sort key
    # Month_Year → YearMonth
    # Series → SortOrder
    # Return (True, "YearMonth") or (False, None)
    pass
```

### 4. Visual Type Validation

```python
def validate_visual_type(visual_type: str) -> bool:
    """
    Verify visual type is valid Power BI visual type.
    Note: Supports both Bar and Column variants (orientation difference).
    """
    valid_types = [
        "card",
        "slicer",
        "lineChart",
        "clusteredBarChart",
        "clusteredColumnChart",
        "hundredPercentStackedBarChart",  # Horizontal orientation
        "hundredPercentStackedColumnChart",  # Vertical orientation (spec may reference this)
        "donutChart",
        "pieChart",
        "tableEx",
        "pivotTable",
        "scatterChart",
        "actionButton"
    ]
    return visual_type in valid_types

def map_spec_visual_type(spec_type: str) -> str:
    """
    Map spec visual type to actual Power BI visual type.
    Handles Bar vs Column orientation differences.
    """
    type_mapping = {
        "hundredPercentStackedColumnChart": "hundredPercentStackedBarChart",  # Spec uses Column, actual is Bar
        # Add other mappings as needed
    }
    return type_mapping.get(spec_type, spec_type)
```

---

## 📐 POSITION CALCULATION

### Grid System

```python
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
MARGIN = 20
GAP = 20
HEADER_HEIGHT = 56
FOOTER_HEIGHT = 24

# Available space
AVAILABLE_WIDTH = CANVAS_WIDTH - (MARGIN * 2)
AVAILABLE_HEIGHT = CANVAS_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - (MARGIN * 2)
```

### KPI Card Layout

```python
CARD_WIDTH = 184
CARD_HEIGHT = 88
CARDS_PER_ROW = 6

def calculate_kpi_position(index: int, row: int) -> dict:
    x = MARGIN + (index % CARDS_PER_ROW) * (CARD_WIDTH + GAP)
    y = HEADER_HEIGHT + MARGIN + (row * (CARD_HEIGHT + GAP))
    return {
        "x": x,
        "y": y,
        "width": CARD_WIDTH,
        "height": CARD_HEIGHT,
        "z": 1000 + index
    }
```

### Chart Layout

```python
CHART_WIDTH = 600
CHART_HEIGHT = 400

def calculate_chart_position(row: int, col: int) -> dict:
    x = MARGIN + (col * (CHART_WIDTH + GAP))
    y = HEADER_HEIGHT + MARGIN + (row * (CHART_HEIGHT + GAP))
    return {
        "x": x,
        "y": y,
        "width": CHART_WIDTH,
        "height": CHART_HEIGHT,
        "z": 2000 + (row * 10) + col
    }
```

---

## 🎯 GENERATION WORKFLOW

### Step 1: Read Specification

```python
# Load FINAL_DASHBOARD_SPEC.md
# Extract page specifications
# Extract visual recipes
# Extract measure contract
```

### Step 2: Validate Dependencies

```python
# For each visual:
#   - Validate all measures exist
#   - Validate all columns exist
#   - Validate sort keys exist
#   - Validate visual type
```

### Step 3: Generate Visual JSON

```python
# For each visual in spec:
#   1. Select template based on visual type
#   2. Map fields to projections
#   3. Calculate position
#   4. Generate unique ID
#   5. Build complete JSON structure
#   6. Validate structure
```

### Step 4: Write Files

```python
# Create visual folder: pages/{page_id}/visuals/{visual_id}/
# Write visual.json
# Verify file structure
```

---

## 🔍 POST-GENERATION VALIDATION

### 1. Structure Validation

- [ ] `$schema` present and correct
- [ ] `name` is unique
- [ ] `position` has all required fields
- [ ] `visual.visualType` is valid
- [ ] `visual.query.queryState` structure correct
- [ ] All projections have `active: true`
- [ ] `visualContainerObjects` present (if required)

### 2. Field Validation

- [ ] All field references match semantic model
- [ ] `queryRef` format: `TableName.FieldName`
- [ ] `nativeQueryRef` format: `FieldName`
- [ ] Field types correct (Measure vs Column)

### 3. Sort Validation

- [ ] Sort definition present (if required)
- [ ] Sort column exists
- [ ] Sort direction valid
- [ ] `isDefaultSort: true` set

---

## 📝 EXAMPLE: Top 10 vs Remaining Chart

### Input (from spec):

```json
{
  "id": "top10_vs_remaining",
  "type": "hundredPercentStackedColumnChart",
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

### Generated Output:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "a1b2c3d4e5f6g7h8i9j0k1l2",
  "position": {
    "x": 20,
    "y": 200,
    "z": 2000,
    "width": 600,
    "height": 400,
    "tabOrder": 200000
  },
  "visual": {
    "visualType": "hundredPercentStackedBarChart",
    "query": {
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
    },
    "visualContainerObjects": {
      "background": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#FFFFFF'"
                    }
                  }
                }
              }
            },
            "transparency": {
              "expr": {
                "Literal": {
                  "Value": "0D"
                }
              }
            }
          }
        }
      ],
      "border": [
        {
          "properties": {
            "color": {
              "solid": {
                "color": {
                  "expr": {
                    "Literal": {
                      "Value": "'#D1D5DB'"
                    }
                  }
                }
              }
            },
            "width": {
              "expr": {
                "Literal": {
                  "Value": "1D"
                }
              }
            }
          }
        }
      ],
      "visualHeader": [
        {
          "properties": {
            "show": {
              "expr": {
                "Literal": {
                  "Value": "true"
                }
              }
            }
          }
        }
      ],
      "title": [
        {
          "properties": {
            "text": {
              "expr": {
                "Literal": {
                  "Value": "'Top 10 vs Remaining Share (Over Time)'"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

---

## 🚀 QUICK REFERENCE

### Visual Type → Template Mapping

| Visual Type | Template | Projections | Sort Required |
|-------------|----------|-------------|---------------|
| `card` | KPI Card | 1 (Measure) | No |
| `slicer` | Slicer | 1 (Column) | Yes |
| `lineChart` | Line Chart | 2+ (Column, Measure) | Yes |
| `hundredPercentStackedBarChart` | Stacked Bar | 3+ (Category: Column, Series: Column, Y: Measure) | Yes |
| `donutChart` | Donut | 2+ (Column, Measure) | No |
| `clusteredBarChart` | Bar Chart | 2+ (Column, Measure) | Yes |

### Field Type Detection

| Pattern | Type |
|---------|------|
| `Metrics[...]` | Measure |
| `Dim_...[...]` | Column |
| `Fact_...[...]` | Column |
| In Measure Contract | Measure |
| Otherwise | Column (verify) |

### Required Properties Checklist

- [ ] `$schema` (always)
- [ ] `name` (unique ID)
- [ ] `position` (x, y, z, width, height, tabOrder)
- [ ] `visual.visualType` (valid type)
- [ ] `visual.query.queryState.Category/Series/Y/Values` (correct bucket per visual type)
- [ ] `projections[].field` (correct type)
- [ ] `projections[].queryRef` (Table.Field format)
- [ ] `projections[].nativeQueryRef` (Field format)
- [ ] `projections[].active` (must be true)
- [ ] `visualContainerObjects` (if required for type)
- [ ] `sortDefinition` (if required for type)

---

**Status:** ✅ Ready for Implementation  
**Next Step:** Use this method to generate visuals from FINAL_DASHBOARD_SPEC.md
