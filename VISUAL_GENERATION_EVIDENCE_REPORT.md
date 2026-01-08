# Visual Generation Evidence Report

**Date:** 2026-01-08  
**Source PBIP:** `press-room-dashboard.pbip`  
**Location:** `C:\Users\farad\OneDrive\Desktop\automation-system\`  
**Status:** Updated with Merged, Cleaned-Up Truth Set

---

## ✅ CONFIRMED STRUCTURES (From Observed Files)

### PBIP Pointer Behavior

**OBSERVED:** `.pbip` schema and structure confirmed:

- `artifacts` is an **array**
- Contains **only "report" artifact** (no "dataset" or "semanticModel" artifact in root .pbip)
- Dataset binding lives in `definition.pbir` via:
  ```json
  "datasetReference": {
    "byPath": {
      "path": "../press-room-dashboard.SemanticModel"
    }
  }
  ```

**Generator Impact:**
- Generator can open and bind a model successfully using:
  - `.pbip` with report artifact only
  - `definition.pbir.datasetReference.byPath`
- Keep "dataset artifact in .pbip" as **conditional check**, not hard blocker, until compared against freshly created PBIP on same Desktop build

### PBIR Folder Map (Confirmed Real Structure)

**OBSERVED:** Full modular PBIR structure exists:

- `definition/version.json` exists (version `2.0.0`)
- `definition/report.json` exists (schema `3.0.0`)
- `definition/pages/pages.json` exists and controls:
  - `pageOrder` (array of page IDs)
  - `activePageName` (string)
- `definition/bookmarks/*` exists

**Generator Impact:**
- From-scratch generator must emit at minimum:
  - `definition/version.json`
  - `definition/report.json`
  - `definition/pages/pages.json`
  - `definition/pages/<page_id>/page.json`
  - `definition/pages/<page_id>/visuals/<visual_id>/visual.json`

### Page Dimensions and Coordinate Behavior

**OBSERVED from `page.json` (VERBATIM):**
```json
"width": 1280,
"height": 720
```

**OBSERVED from visual `position` (VERBATIM):**
```json
"position": {
  "x": 885.08015209635,
  "y": 23.327693931221631,
  "z": 2,
  "height": 63.121995343305585,
  "width": 196.22707248027606,
  "tabOrder": 2
}
```

**Generator Impact:**
- Treat layout units as "Power BI stored units" (numeric values, sometimes floats)
- **Do NOT claim pixels/points** as a rule (units not specified in JSON)
- Allow floats everywhere in `position` (do not round to ints)
- `z`, `tabOrder`, `x`, `y`, `width`, `height` all use decimal values

### Visual Mounting Mechanism (Likely Folder Discovery)

**OBSERVED:**
- Visual ID string search found **no visual ID references** in:
  - `page.json`
  - `pages.json`
- Each page folder contains:
  - `page.json`
  - `visuals/` subfolder

**Best Current Conclusion:**
- Power BI **discovers visuals by scanning `visuals/<visual_id>/visual.json`**
- Visuals are **NOT explicitly enumerated** in page.json or pages.json

**Generator Impact:**
- Strongly suggests "mounting = create visual folder + visual.json"
- **MUST be validated** by rename test because mounting could still depend on hidden index not yet found
- Until proven, treat as **conditional rule**

### QueryRef / nativeQueryRef Patterns (Confirmed for Columns)

**OBSERVED in slicers (VERBATIM):**

Column with underscore (`Dim_Press_Releases.Page_Type`):
```json
{
  "field": {
    "Column": {
      "Expression": {
        "SourceRef": {
          "Entity": "Dim_Press_Releases"
        }
      },
      "Property": "Page_Type"
    }
  },
  "queryRef": "Dim_Press_Releases.Page_Type",
  "nativeQueryRef": "Page_Type",
  "active": true,
  "format": "G"
}
```

Column without underscore (`Dim_Date.Date`):
```json
{
  "field": {
    "Column": {
      "Expression": {
        "SourceRef": {
          "Entity": "Dim_Date"
        }
      },
      "Property": "Date"
    }
  },
  "queryRef": "Dim_Date.Date",
  "nativeQueryRef": "Date",
  "active": true
}
```

**Pattern Observed:**
- `queryRef`: `Table.Column` (dot notation, no brackets)
- `nativeQueryRef`: `Column` only (column name, no table prefix)
- Underscores preserved exactly
- `active: true` present on all projections

**Generator Impact:**
- Column bindings are **solid and confirmed**
- Measure bindings with spaces are **STILL UNKNOWN** (must be captured from Card golden sample)
- **IMPORTANT:** Report's "Conclusion for measures with spaces" was a guess — do not bake into rules yet

### Sorting Structure (Confirmed for Slicer)

**OBSERVED from slicer `79f5f9f9ae9d08a9c70b/visual.json` (VERBATIM):**
```json
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
          "Property": "Date"
        }
      },
      "direction": "Ascending"
    }
  ],
  "isDefaultSort": true
}
```

**Observations:**
1. SortDefinition references **display column** (`Date`), not a numeric sort key
2. Sort field (`Date`) **appears in projections** (it's the visual's data field)
3. No hidden sort key column in projections

**Generator Impact:**
- Sorting object shape is **confirmed** (at least for slicers)
- Chart sorting behavior is **STILL UNKNOWN** (must be captured from Line/Stacked Column golden samples)

---

## ⚠️ CONDITIONAL RULES (Require Validation)

### 1. PBIP Dataset Artifact

**Current Observation:**
- `.pbip` contains only `"report"` artifact (no `"dataset"`)

**Conditional Rule:**
- If Power BI requires it in your build, `.pbip` must include both `report` and `dataset` artifacts in exact schema Power BI writes
- **Until proven:** Keep as conditional check, not hard blocker

### 2. Visual Mounting

**Current Observation:**
- Visuals appear to be discovered via folder structure (no explicit list found)

**Conditional Rule:**
- Mounting = create visual folder + visual.json
- **Until proven:** Must validate via rename test

---

## ❌ EXPLICIT UNKNOWNS (Blockers for Perfect Generation)

These are the remaining true blockers for "perfect visual generation":

1. **Power BI Desktop version/build** — Must be copied manually from Help → About

2. **Golden samples for:**
   - Card visual
   - Line chart
   - Donut chart
   - 100% stacked column chart

3. **Measure queryRef/nativeQueryRef** — For `Metrics[Total Views]` (measure with space)

4. **Page mounting confirmation** — Via rename test (requires manual Power BI Desktop interaction)

5. **Chart sorting behavior** — What `sortDefinition` looks like for charts and what it references

6. **Chart role buckets** — QueryState bucket names and projection role names for Line/Donut/Stacked Column

---

## 🔒 MODEL SORTING COMPLIANCE

### Current Status: FIXED ✅

**Issue Identified:**
- `Dim_Date[Year_Month]` had no `sortByColumn` property
- Risked lexical sorting instead of chronological

**Fix Applied:**
- Added `YearMonth` numeric key column (YYYYMM format, calculated via DAX)
- Set `Year_Month.sortByColumn = YearMonth` in TMDL
- Added `YearMonth` column to Power Query M source

**Evidence from `Dim_Date.tmdl` (after fix):**
```tmdl
/// Year-Month formatted as text (e.g., '2025-03'). Useful for sorting and labeling. Sorted by YearMonth for chronological ordering.
column Year_Month
	dataType: string
	lineageTag: pr-dimdate-yearmonth
	summarizeBy: none
	sourceColumn: Year_Month
	sortByColumn: YearMonth

	annotation SummarizationSetBy = Automatic

/// Numeric sort key for Year_Month column (YYYYMM format). Used to ensure chronological sorting instead of alphabetical.
column YearMonth
	dataType: int64
	formatString: 0
	isHidden
	lineageTag: pr-dimdate-yearmonth-sort
	summarizeBy: sum
	expression = YEAR(Dim_Date[Date]) * 100 + MONTH(Dim_Date[Date])

	annotation SummarizationSetBy = Automatic
```

**Generator Impact:**
- If generating time-series visuals on `Year_Month`, model now supports chronological sorting
- Visual `sortDefinition` should reference `YearMonth` (numeric key) for proper sorting

---

## 📄 VERBATIM FILE CONTENTS

### Root .pbip File

**File:** `press-room-dashboard.pbip`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
  "version": "1.0",
  "artifacts": [
    {
      "report": {
        "path": "press-room-dashboard.Report"
      }
    }
  ],
  "settings": {
    "enableAutoRecovery": true
  }
}
```

### definition.pbir

**File:** `press-room-dashboard.Report\definition.pbir`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../press-room-dashboard.SemanticModel"
    }
  }
}
```

### definition/version.json

**File:** `press-room-dashboard.Report\definition\version.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
  "version": "2.0.0"
}
```

### definition/pages/pages.json

**File:** `press-room-dashboard.Report\definition\pages\pages.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
  "pageOrder": [
    "86b448ef2a89e75fa80e"
  ],
  "activePageName": "86b448ef2a89e75fa80e"
}
```

### definition/report.json

**File:** `press-room-dashboard.Report\definition\report.json`

**Key Sections (Full file is 102 lines):**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json",
  "themeCollection": {
    "baseTheme": {
      "name": "HHS_Theme_USWDS_Aligned",
      "reportVersionAtImport": {
        "visual": "2.4.0",
        "report": "3.0.0",
        "page": "2.3.0"
      },
      "type": "SharedResources"
    },
    "customTheme": {
      "name": "HHS_USWDS_Theme5040178124888481.json",
      "reportVersionAtImport": {
        "visual": "2.4.0",
        "report": "3.0.0",
        "page": "2.3.0"
      },
      "type": "RegisteredResources"
    }
  },
  "objects": {
    "section": [
      {
        "properties": {
          "verticalAlignment": {
            "expr": {
              "Literal": {
                "Value": "'Top'"
              }
            }
          }
        }
      }
    ],
    "outspacePane": [
      {
        "properties": {
          "expanded": {
            "expr": {
              "Literal": {
                "Value": "true"
              }
            }
          }
        }
      }
    ]
  },
  "publicCustomVisuals": [
    "v27d59d9f_0c2b_4456_982c_d551f8a876be"
  ],
  "resourcePackages": [
    {
      "name": "SharedResources",
      "type": "SharedResources",
      "items": [
        {
          "name": "HHS_Theme_USWDS_Aligned",
          "path": "BaseThemes/HHS_Theme_USWDS_Aligned.json",
          "type": "BaseTheme"
        }
      ]
    },
    {
      "name": "RegisteredResources",
      "type": "RegisteredResources",
      "items": [
        {
          "name": "background_channels4943707189684421.svg",
          "path": "background_channels4943707189684421.svg",
          "type": "Image"
        },
        {
          "name": "logo-white-bg20252112630989272.svg",
          "path": "logo-white-bg20252112630989272.svg",
          "type": "Image"
        },
        {
          "name": "HHS_USWDS_Theme5040178124888481.json",
          "path": "HHS_USWDS_Theme5040178124888481.json",
          "type": "CustomTheme"
        }
      ]
    }
  ],
  "settings": {
    "useStylableVisualContainerHeader": true,
    "exportDataMode": "AllowSummarized",
    "defaultDrillFilterOtherVisuals": true,
    "allowChangeFilterTypes": true,
    "useEnhancedTooltips": true,
    "useDefaultAggregateDisplayName": true
  },
  "slowDataSourceSettings": {
    "isCrossHighlightingDisabled": false,
    "isSlicerSelectionsButtonEnabled": false,
    "isFilterSelectionsButtonEnabled": false,
    "isFieldWellButtonEnabled": false
  }
}
```

### definition/pages/86b448ef2a89e75fa80e/page.json

**File:** `press-room-dashboard.Report\definition\pages\86b448ef2a89e75fa80e\page.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
  "name": "86b448ef2a89e75fa80e",
  "displayName": "Page 2",
  "displayOption": "FitToPage",
  "height": 720,
  "width": 1280,
  "pageBinding": {
    "name": "46058fcbd51d92ced40d",
    "type": "Default",
    "parameters": []
  },
  "objects": {
    "background": [
      {
        "properties": {
          "image": {
            "image": {
              "name": {
                "expr": {
                  "Literal": {
                    "Value": "'background_channels.svg'"
                  }
                }
              },
              "url": {
                "expr": {
                  "ResourcePackageItem": {
                    "PackageName": "RegisteredResources",
                    "PackageType": 1,
                    "ItemName": "background_channels4943707189684421.svg"
                  }
                }
              },
              "scaling": {
                "expr": {
                  "Literal": {
                    "Value": "'Normal'"
                  }
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

---

## 📊 VISUAL TYPE EVIDENCE (From Current PBIP)

**STATUS: INCOMPLETE**

**Reason:** Current PBIP only contains 3 visuals (2 slicers, 1 actionButton). Missing: Card, Line Chart, Donut, 100% Stacked Column.

### Observed Visuals Table

| Visual Folder | VisualType (exact case) | QueryState Bucket | Projections Role Buckets |
|---------------|-------------------------|-------------------|--------------------------|
| `79f5f9f9ae9d08a9c70b` | `slicer` | `Values` | `Values` (single bucket) |
| `70869c336db70da0c4a2` | `slicer` | `Values` | `Values` (single bucket) |
| `43c3caa20026750d70d1` | `actionButton` | N/A (no query) | N/A |

**Evidence for slicer (`79f5f9f9ae9d08a9c70b`):**
```json
"visualType": "slicer",
"query": {
  "queryState": {
    "Values": {
      "projections": [...]
    }
  }
}
```

**Evidence for actionButton (`43c3caa20026750d70d1`):**
```json
"visualType": "actionButton"
```
(No `query` property)

---

## 📝 TMDL EVIDENCE

### Relationship Definitions (VERBATIM)

**From `relationships.tmdl` (full file):**
```tmdl
relationship 'Fact_Press_Analytics[Date] -> Dim_Date[Date]'
	fromColumn: Fact_Press_Analytics.Date
	toColumn: Dim_Date.Date

relationship 'Fact_Press_Analytics[Page_URL] -> Dim_Press_Releases[Page_URL]'
	fromColumn: Fact_Press_Analytics.Page_URL
	toColumn: Dim_Press_Releases.Page_URL
```

### Data Types (VERBATIM)

**From `Fact_Press_Analytics.tmdl` (lines 6-16):**
```tmdl
/// Date of the analytics event. Links to Dim_Date for calendar attributes and time intelligence.
column Date
	dataType: dateTime
	formatString: Long Date
	lineageTag: 4e61b3ca-560b-4054-93d7-5abce9ee53ce
	dataCategory: Time
	summarizeBy: none
	sourceColumn: Date

	annotation SummarizationSetBy = Automatic

	annotation UnderlyingDateTimeDataType = Date
```

**From `Dim_Date.tmdl` (lines 7-17):**
```tmdl
/// Primary date key for time-based analysis
column Date
	dataType: dateTime
	isKey
	formatString: Short Date
	lineageTag: pr-dimdate-date
	summarizeBy: none
	sourceColumn: Date

	annotation SummarizationSetBy = Automatic

	annotation UnderlyingDateTimeDataType = Date
```

**Conclusion:**
- `Fact_Press_Analytics[Date]`: `dataType: dateTime`
- `Dim_Date[Date]`: `dataType: dateTime`
- Both have `UnderlyingDateTimeDataType = Date` annotation
- **Data types match** (both `dateTime`)

### DAX Delimiter Evidence

**From `Metrics.tmdl` (line 6, VERBATIM):**
```tmdl
measure 'Total Views' = SUM(Fact_Press_Analytics[Views])
```

**Additional evidence (line 90):**
```tmdl
measure 'Views per User' = DIVIDE([Total Views], [Total Users], 0)
```

**Conclusion:** TMDL uses **comma** as DAX function argument delimiter (standard DAX syntax).

---

## 🎯 NEXT STEPS (Manual Actions Required)

1. **Power BI Desktop Version**
   - Open Power BI Desktop → Help → About
   - Copy exact version/build string
   - Add to this report

2. **Create GOLDEN_MIN PBIP**
   - In Power BI Desktop, create minimal PBIP with:
     - 1 page
     - 5 visuals: Card, Line Chart, Donut, 100% Stacked Column, Slicer
     - Use `Metrics[Total Views]` in Card
     - Use `Dim_Date[Year_Month]` on chart axis
     - Apply HHS theme
   - Save as PBIP in automation-system folder

3. **Rename Test**
   - Pick one visual folder in GOLDEN_MIN
   - Rename folder (append "_RENAMED")
   - Re-open PBIP in Power BI Desktop
   - Observe behavior (visual disappears? error? unchanged?)
   - Restore folder name after test

4. **Extract Golden Samples**
   - From GOLDEN_MIN, extract full `visual.json` for each of the 5 visual types
   - Document queryState bucket names
   - Document projection role bucket names
   - Document measure queryRef/nativeQueryRef patterns

---

## SUMMARY

**Confirmed Structures (Ready for Generator):**
- ✅ PBIP artifact structure (report-only in .pbip, dataset in definition.pbir)
- ✅ PBIR folder map (version.json, report.json, pages.json structure)
- ✅ Page dimensions (1280x720, stored as numbers)
- ✅ Visual position structure (floats for x, y, z, width, height, tabOrder)
- ✅ Column queryRef/nativeQueryRef patterns (dot notation, underscores preserved)
- ✅ Slicer sorting structure (sortDefinition with sort array)
- ✅ Model sorting compliance (Year_Month now has sortByColumn)

**Conditional Rules (Require Validation):**
- ⚠️ Visual mounting (likely folder-discovery, needs rename test confirmation)
- ⚠️ PBIP dataset artifact (only report in .pbip, may vary by Desktop build)

**Explicit Unknowns (Blockers):**
- ❌ Power BI Desktop version/build
- ❌ Card/Line/Donut/Stacked Column visual structures
- ❌ Measure queryRef/nativeQueryRef (measures with spaces)
- ❌ Chart sorting behavior
- ❌ Chart role buckets (queryState bucket names, projection roles)
