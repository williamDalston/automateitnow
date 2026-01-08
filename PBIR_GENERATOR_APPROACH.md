# PBIR Generator Approach: Template-Driven Patching

**Status:** ✅ Production-Ready  
**Version:** 1.0  
**Last Updated:** January 8, 2026

---

## 🎯 Core Principle: Copy + Patch Templates (No Schema Guessing)

**Why this approach is production-safe:**
- We never manufacture unknown PBIR structures
- We only patch strings inside known-good, exported PBIR specimens
- Power BI schema quirks are preserved from the exported base
- Sort definitions, projection roles, container objects remain intact

---

## 📋 Implementation Steps

### Step 1: Create Base PBIR Skeleton

In Power BI Desktop:

1. Build a minimal report with:
   - 6 pages (IDs/names per `FINAL_DASHBOARD_SPEC.md`)
   - Nav rail + header/footer containers
   - One instance of each visual type you'll generate:
     - `card`
     - `table`
     - `slicer`
     - `hundredPercentStackedColumnChart`
     - `donutChart`
     - `lineChart`

2. Export to PBIP/PBIR

3. Put it in a folder: `pbir_base/`

### Step 2: Create Template Visuals

Inside `pbir_base/`, create:

```
pbir_base/
  pages/...
  report.json
  pages.json
  definition.pbir
  _templates/
    visuals/
      card/visual.json
      table/visual.json
      slicer/visual.json
      hundredPercentStackedColumnChart/visual.json
      donutChart/visual.json
      lineChart/visual.json
```

### Step 3: Insert Placeholders in Template visual.json Files

In each template `visual.json`, replace field `queryRef` strings with tokens:

**Common Placeholders:**
- `__TITLE__` → Visual title
- `__VISUAL_NAME__` → Visual folder name (must match `visual.json.name`)
- `__X_AXIS__` → X-axis field (queryRef format: `Table.Field`)
- `__LEGEND__` → Legend field
- `__Y_AXIS__` → Y-axis measure
- `__VALUES__` → Values measure (for donut/slicer)
- `__DATA__` → Data measure (for card)
- `__TOOLTIP_0__`, `__TOOLTIP_1__`, ... → Tooltip measures
- `__TABLE_COL_0__`, `__TABLE_COL_1__`, ... → Table column fields
- `__SORT_BY__` → Sort field (if templated)
- `__FILTER_FIELD__` / `__FILTER_VALUE__` → Visual-level filter (optional)

**Example (100% Stacked Column Chart):**
```json
{
  "name": "__VISUAL_NAME__",
  "visual": {
    "visualType": "hundredPercentStackedColumnChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": { "Column": { ... } },
              "queryRef": "__X_AXIS__",
              "nativeQueryRef": "__X_AXIS_NATIVE__",
              "active": true
            }
          ]
        },
        "Series": {
          "projections": [
            {
              "field": { "Column": { ... } },
              "queryRef": "__LEGEND__",
              "nativeQueryRef": "__LEGEND_NATIVE__",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": { "Measure": { ... } },
              "queryRef": "__Y_AXIS__",
              "nativeQueryRef": "__Y_AXIS_NATIVE__",
              "active": true
            }
          ]
        },
        "Tooltips": {
          "projections": [
            {
              "field": { "Measure": { ... } },
              "queryRef": "__TOOLTIP_0__",
              "nativeQueryRef": "__TOOLTIP_0_NATIVE__",
              "active": true
            }
          ]
        }
      },
      "sortDefinition": {
        "sort": [
          {
            "field": { "Column": { ... } },
            "direction": "Ascending"
          }
        ]
      }
    }
  }
}
```

---

## 🔧 Generator Script

**File:** `pbir_generate.py`

**Usage:**
```bash
python pbir_generate.py --config dashboard_config.json --base pbir_base --out pbir_out
```

**With Model Validation:**
```bash
python pbir_generate.py --config dashboard_config.json --base pbir_base --out pbir_out --model ./model
```

**What it does:**
1. Loads config JSON (from `FINAL_DASHBOARD_SPEC.md` automation-ready configuration)
2. Validates required field refs exist (optional: against model files)
3. Copies `pbir_base/` → `pbir_out/`
4. Writes/overwrites visuals per config by:
   - Copying visual templates
   - Replacing placeholders with actual field refs
5. Emits `validation_report.json` for failure tracking

**Field Reference Conversion:**
- Config format: `Table[Column]` or `Metrics[Measure]`
- PBIR format: `Table.Column` or `Metrics.Measure` (dot form)
- Generator automatically converts via `to_queryref()`

---

## ✅ Validation & Safety

### Pre-Generation Validation

1. **Field Reference Syntax:** Validates `Table[Field]` format
2. **Model Field Existence:** If `--model` provided, checks fields exist in model
3. **Template Availability:** Ensures all required visual type templates exist

### Post-Generation Validation

1. **JSON Syntax:** Validates patched JSON parses correctly
2. **Visual Identity:** Ensures `visual.json.name == folder name`
3. **Required Structure:** Validates `pages.json`, `report.json`, `definition.pbir` exist

**Run Validator:**
```bash
python master_pbip_validator.py pbir_out --check-only --verbose
```

---

## 🚨 Critical Guardrails (Enforced by Generator)

1. **No Schema Guessing:** Generator only does string replacement, never creates new JSON structures
2. **Template-Driven:** All PBIR structures come from exported Power BI Desktop specimens
3. **Placeholder Safety:** Missing placeholders remain as-is (validation catches them)
4. **Field Reference Validation:** Hard-fails if field refs don't match model (if model provided)

---

## 📝 Template Creation Workflow

1. **Export Base PBIR** from Power BI Desktop with one of each visual type
2. **Copy visual.json** from each visual to `_templates/visuals/<visualType>/visual.json`
3. **Replace field references** with placeholders:
   - Find: `"queryRef": "Dim_Date.Month_Year"`
   - Replace: `"queryRef": "__X_AXIS__"`
4. **Replace nativeQueryRef** similarly:
   - Find: `"nativeQueryRef": "Month_Year"`
   - Replace: `"nativeQueryRef": "__X_AXIS_NATIVE__"`
5. **Replace title** with `__TITLE__`
6. **Replace name** with `__VISUAL_NAME__`
7. **Test:** Run generator on a single visual to verify placeholder replacement

---

## 🔍 Example: Top 10 vs Remaining Chart Template

**Config:**
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

**Placeholder Mapping Generated:**
```python
{
  "TITLE": "Top 10 vs Remaining Share (Over Time)",
  "VISUAL_NAME": "top10_vs_remaining",
  "X_AXIS": "Dim_Date.Month_Year",
  "X_AXIS_NATIVE": "Month_Year",  # Extracted from field name
  "LEGEND": "Top10_Series.Series",
  "LEGEND_NATIVE": "Series",
  "Y_AXIS": "Metrics.Top10 Series Value",
  "Y_AXIS_NATIVE": "Top10 Series Value",
  "TOOLTIP_0": "Metrics.Top 10 PR Views",
  "TOOLTIP_0_NATIVE": "Top 10 PR Views",
  "TOOLTIP_1": "Metrics.Remaining PR Views",
  "TOOLTIP_1_NATIVE": "Remaining PR Views",
  "TOOLTIP_2": "Metrics.Press Release Views",
  "TOOLTIP_2_NATIVE": "Press Release Views",
  "TOOLTIP_3": "Metrics.Top 10 Share",
  "TOOLTIP_3_NATIVE": "Top 10 Share"
}
```

**Template visual.json** gets patched with these values, preserving all other PBIR structure.

---

## 🎯 Benefits of This Approach

1. **Zero Schema Guessing:** All structures come from Power BI Desktop exports
2. **Version-Safe:** PBIR version quirks are preserved in templates
3. **Validation-Friendly:** Easy to verify templates match expected structure
4. **Maintainable:** Update templates when Power BI versions change, not generator code
5. **Debuggable:** Failed generations leave placeholders visible for diagnosis

---

## 📚 Related Documents

- **`FINAL_DASHBOARD_SPEC.md`** - Complete dashboard specification
- **`PRECISE_VISUAL_GENERATION_METHOD.md`** - Detailed visual generation contracts
- **`master_pbip_validator.py`** - Post-generation validation script
- **`HARD_CONTRACTS_VALIDATION.md`** - Hard contracts enforced by validator

---

**Status:** ✅ Ready for implementation. Generator script provided. Template creation workflow documented.
