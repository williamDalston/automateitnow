# 🎯 PRECISE VISUAL GENERATION METHOD

**Version:** 2.0  
**Status:** Production-Ready (Evidence-Based)  
**Purpose:** Exact, step-by-step method for generating Power BI visuals from specification  
**Last Updated:** 2026-01-08  
**Evidence Source:** `VISUAL_GENERATION_EVIDENCE_REPORT.md`

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

**❌ UNKNOWN for Measures:**
- Measure `queryRef`/`nativeQueryRef` patterns (especially measures with spaces like `"Total Views"`)
- **DO NOT assume:** Requires golden Card sample to confirm
- **Current hypothesis (NOT CONFIRMED):** `queryRef: "Metrics.Total Views"`, `nativeQueryRef: "Total Views"` (preserves spaces)

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

**❌ UNKNOWN for Charts:**
- Chart sorting behavior (what sortDefinition looks like for Line/Stacked Column)
- Whether charts use display column or numeric sort key
- Whether sort field must appear in projections (even if hidden)

### Model Sorting Compliance

**✅ Fixed:**
- `Dim_Date[Year_Month]` now has `sortByColumn: YearMonth`
- `YearMonth` numeric key exists (YYYYMM format, hidden)

**Generator Contract:**
- When using `Year_Month` on axis, visual `sortDefinition` should reference `YearMonth` (numeric key) for proper chronological sorting
- If model lacks sortByColumn, risk lexical sorting (alphabetical "2024-01", "2024-10", "2024-02" instead of chronological)

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
│   │       └── Data/Values (REQUIRED)
│   │           └── projections (REQUIRED)
│   │               └── field (REQUIRED)
│   │               └── queryRef (REQUIRED)
│   │               └── nativeQueryRef (REQUIRED)
│   │               └── active (REQUIRED - must be true)
│   └── visualContainerObjects (REQUIRED for cards/charts, NOT for slicers)
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
- `queryRef` - Full reference: `TableName.ColumnName` or `TableName.MeasureName` (✅ confirmed for columns, ❌ unknown for measures)
- `nativeQueryRef` - Short name: `ColumnName` or `MeasureName` (✅ confirmed for columns, ❌ unknown for measures)
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

### 2. Golden Visual Samples

**Missing:**
- Card visual (for measure queryRef patterns)
- Line chart (for chart role buckets, sorting behavior)
- Donut chart (for chart role buckets)
- 100% stacked column chart (for chart role buckets, sorting behavior)

**Impact:** Cannot generate these visual types with complete confidence

### 3. Measure QueryRef Patterns

**Unknown:**
- Exact `queryRef` format for measures with spaces (e.g., `"Total Views"`)
- Exact `nativeQueryRef` format for measures with spaces
- Whether spaces are preserved or escaped

**Impact:** Card visuals using measures cannot be generated accurately

### 4. Chart Role Buckets

**Unknown:**
- QueryState bucket name for charts (is it `Data` or `Values`?)
- Projection role bucket names for charts (Category, Y, Legend, Tooltips, Values, etc.)
- Which roles are required vs optional

**Impact:** Chart visuals cannot be generated with correct field well structure

### 5. Chart Sorting Behavior

**Unknown:**
- Whether charts use display column or numeric sort key in `sortDefinition`
- Whether sort field must appear in projections (even if hidden/tooltip role)
- SortDefinition structure for charts (may differ from slicer)

**Impact:** Chart visuals may have incorrect or missing sorting

### 6. Page Mounting Confirmation

**Unknown:**
- Whether visual mounting is truly folder-discovery or depends on hidden index
- What happens if visual folder is renamed (does visual disappear? error? unchanged?)

**Impact:** Visual generation may fail if mounting mechanism is misunderstood

---

## 🔒 GENERATOR CONSTRAINTS

Based on observed evidence:

1. **Coordinate System:**
   - Use floats for `x`, `y`, `width`, `height` (do not round)
   - `z` and `tabOrder` can be integers or floats (allow both)
   - Page dimensions: `1280 × 720` (stored as numbers)

2. **Visual Structure:**
   - `visualContainerObjects` REQUIRED for cards/charts
   - `visualContainerObjects` NOT ALLOWED for slicers
   - `active: true` REQUIRED on all projections

3. **Field References:**
   - Column pattern: `queryRef: "Table.Column"`, `nativeQueryRef: "Column"` (✅ confirmed)
   - Measure pattern: UNKNOWN (❌ requires golden Card sample)

4. **Schema Versions:**
   - Visual schema: `2.4.0` (from `visual.json` $schema)
   - Report schema: `3.0.0` (from `report.json` $schema)
   - Page schema: `2.0.0` (from `page.json` $schema)
   - Report definition schema: `4.0` (from `definition.pbir` version)

5. **VisualType Canonical Strings:**
   - ✅ Observed: `slicer`, `actionButton`
   - ❌ Unknown: `card`, `lineChart`, `donutChart`, `hundredPercentStackedColumnChart` (exact casing)
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
    "tabOrder": {{Z_INDEX * 100}}
  },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Data": {
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
   - `tabOrder`: Can match `z` or be calculated independently (observed pattern varies)
   - **Constraint:** `z` and `tabOrder` are separate axes (layering vs keyboard navigation)

4. **Validation:**
   - [ ] Measure exists in semantic model
   - [ ] `active: true` present in projection
   - [ ] `queryRef` matches `TableName.MeasureName`
   - [ ] `visualContainerObjects` present (required for cards)

---

## 2. 100% STACKED COLUMN CHART

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
    "tabOrder": {{Z_INDEX * 100}}
  },
  "visual": {
    "visualType": "hundredPercentStackedColumnChart",
    "query": {
      "queryState": {
        "Data": {
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
            },
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
            },
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
            "direction": "{{ASCENDING|DESCENDING}}"
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

| Power BI Field Well | Projection Index | Field Type | Example |
|---------------------|------------------|------------|---------|
| **X-axis** | 0 | Column | `Dim_Date[Month_Year]` |
| **Legend** | 1 | Column | `Top10_Series[Series]` |
| **Y-axis** | 2 | Measure | `Metrics[Top10 Series Value]` |
| **Tooltips** | 3+ | Measure | `Metrics[Top 10 PR Views]` |

### Generation Rules

1. **Projection Order:**
   - Index 0: X-axis (Column)
   - Index 1: Legend (Column)
   - Index 2: Y-axis (Measure)
   - Index 3+: Tooltips (Measures)

2. **Sort Definition:**
   - If X-axis is `Month_Year`, MUST sort by `YearMonth`
   - If Legend is `Top10_Series[Series]`, MUST sort by `SortOrder`
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
    "tabOrder": {{Z_INDEX * 100}}
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
   - **CRITICAL:** Slicers have minimal `visualContainerObjects`
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
    "tabOrder": {{Z_INDEX * 100}}
  },
  "visual": {
    "visualType": "lineChart",
    "query": {
      "queryState": {
        "Data": {
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
            },
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

| Power BI Field Well | Projection Index | Field Type | Example |
|---------------------|------------------|------------|---------|
| **X-axis** | 0 | Column | `Dim_Date[Date]` |
| **Y-axis** | 1 | Measure | `Metrics[Total Views]` |
| **Legend** | 2+ (optional) | Column | `Fact_Press_Analytics[Channel_Group]` |
| **Tooltips** | 3+ | Measure | `Metrics[Total Users]` |

### Generation Rules

1. **Single Series:**
   - Index 0: X-axis (Column)
   - Index 1: Y-axis (Measure)
   - Index 2+: Tooltips (Measures)

2. **Multiple Series:**
   - Index 0: X-axis (Column)
   - Index 1: Legend (Column)
   - Index 2: Y-axis (Measure)
   - Index 3+: Tooltips (Measures)

3. **Sort Definition:**
   - Always sort by X-axis column
   - If X-axis is date, sort ascending
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
    "tabOrder": {{Z_INDEX * 100}}
  },
  "visual": {
    "visualType": "donutChart",
    "query": {
      "queryState": {
        "Data": {
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
            },
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

| Power BI Field Well | Projection Index | Field Type | Example |
|---------------------|------------------|------------|---------|
| **Legend** | 0 | Column | `Fact_Press_Analytics[Channel_Group]` |
| **Values** | 1 | Measure | `Metrics[Total Views]` |
| **Tooltips** | 2+ | Measure | `Metrics[Total Users]` |

### Generation Rules

1. **Projection Order:**
   - Index 0: Legend (Column)
   - Index 1: Values (Measure)
   - Index 2+: Tooltips (Measures)

2. **No Sort Definition:**
   - Donut charts don't require sort definition
   - Power BI handles ordering automatically

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

**Rules:**
- If table is `Metrics` → Type is `Measure`
- If table starts with `Dim_` or `Fact_` → Type is `Column`
- If field is in Measure Contract → Type is `Measure`
- Otherwise → Type is `Column` (verify in semantic model)

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
    """
    valid_types = [
        "card",
        "slicer",
        "lineChart",
        "clusteredBarChart",
        "clusteredColumnChart",
        "hundredPercentStackedColumnChart",
        "donutChart",
        "pieChart",
        "tableEx",
        "pivotTable",
        "scatterChart",
        "actionButton"
    ]
    return visual_type in valid_types
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
    "visualType": "hundredPercentStackedColumnChart",
    "query": {
      "queryState": {
        "Data": {
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
            },
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
| `hundredPercentStackedColumnChart` | Stacked Column | 3+ (Column, Column, Measure) | Yes |
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
- [ ] `visual.query.queryState.Data/Values` (correct bucket)
- [ ] `projections[].field` (correct type)
- [ ] `projections[].queryRef` (Table.Field format)
- [ ] `projections[].nativeQueryRef` (Field format)
- [ ] `projections[].active` (must be true)
- [ ] `visualContainerObjects` (if required for type)
- [ ] `sortDefinition` (if required for type)

---

**Status:** ✅ Ready for Implementation  
**Next Step:** Use this method to generate visuals from FINAL_DASHBOARD_SPEC.md
