# Generator Robustness Checklist

**Purpose:** Ensure the visual generator code prevents ALL common PBIP issues documented in `COMMON_PBIP_ISSUES.md`.

**Reference:** `07_Guides/COMMON_PBIP_ISSUES.md` (comprehensive issue catalog)

---

## ✅ Schema Validation Errors

### 1. Invalid Background Properties
**Issue:** `imageFit`, `imageTransparency`, `imagePosition` at wrong level  
**Prevention:**
- [x] Generator uses nested `image.image` structure with `scaling` property
- [x] Never adds `imageFit`, `imageTransparency`, `imagePosition` to page backgrounds
- [x] Background structure matches: `objects.background[0].properties.image.image.{url, scaling}`

**Generator Code Check:**
```python
# ✅ CORRECT (in page generator)
"image": {
    "image": {
        "url": {"expr": {"ResourcePackageItem": {...}}},
        "scaling": {"expr": {"Literal": {"Value": "'Fit'"}}}
    }
}
# ❌ NEVER add: imageFit, imageTransparency, imagePosition
```

---

### 2. Invalid Visual Query Structure
**Issue:** `projections` and `queryState` at wrong level  
**Prevention:**
- [x] All visuals use `visual.query.queryState` structure
- [x] Never place `projections` or `queryState` directly under `visual`
- [x] Never place `query` property inside `queryState`

**Generator Code Check:**
```python
# ✅ CORRECT
visual = {
    "visual": {
        "visualType": "lineChart",
        "query": {
            "queryState": {
                "Category": {"projections": [...]},
                "Y": {"projections": [...]}
            }
        }
    }
}
```

---

### 3. Chart Visual Projections Structure
**Issue:** `Category`, `Y`, `Series` nested under `projections` dict  
**Prevention:**
- [x] Chart visuals use buckets as direct children of `queryState`
- [x] Each bucket has its own `projections` array
- [x] Never nest chart buckets under a `projections` dict

**Generator Code Check:**
```python
# ✅ CORRECT (chart visuals)
"queryState": {
    "Category": {"projections": [...]},  # Direct child
    "Y": {"projections": [...]},         # Direct child
    "Series": {"projections": [...]}     # Direct child
}

# ❌ WRONG
"queryState": {
    "projections": {
        "Category": [...],  # Nested - WRONG
        "Y": [...]
    }
}
```

---

### 4. Slicer Visual Projections Structure
**Issue:** Using `Field` bucket or `projections` dict  
**Prevention:**
- [x] Slicers always use `Values` bucket
- [x] Never use `Field` bucket for slicers
- [x] Never nest projections under a `projections` dict for slicers

**Generator Code Check:**
```python
# ✅ CORRECT (slicers)
"queryState": {
    "Values": {"projections": [...]}
}

# ❌ WRONG
"queryState": {
    "Field": {"projections": [...]}  # WRONG
}
# OR
"queryState": {
    "projections": {"Field": [...]}  # WRONG
}
```

---

### 5. Card Visual Projections Structure
**Issue:** Using `Values` bucket or `projections` dict  
**Prevention:**
- [x] Cards always use `Data` bucket (NOT `Values`)
- [x] Never nest projections under a `projections` dict for cards

**Generator Code Check:**
```python
# ✅ CORRECT (cards)
"queryState": {
    "Data": {"projections": [...]}  # Data, not Values
}

# ❌ WRONG
"queryState": {
    "Values": {"projections": [...]}  # WRONG for cards
}
```

---

### 6. Invalid Property in .pbip Artifacts Array
**Issue:** Using `semanticModel` instead of `dataset`  
**Prevention:**
- [x] Always use `dataset` (not `semanticModel`) in `.pbip` artifacts
- [x] Path points to `.SemanticModel` folder

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "artifacts": [
        {"report": {"path": "dashboard.Report"}},
        {"dataset": {"path": "dashboard.SemanticModel"}}  # dataset, not semanticModel
    ]
}
```

---

### 7. Invalid `drillFilterOtherVisuals` Property
**Issue:** Property doesn't exist in schema  
**Prevention:**
- [x] Never add `drillFilterOtherVisuals` to visual JSON files
- [x] Visual interactions configured in Power BI Desktop UI only

**Generator Code Check:**
```python
# ❌ NEVER add this property
visual = {
    "drillFilterOtherVisuals": True  # WRONG - doesn't exist
}
```

---

### 8. Invalid `description` in TMDL Relationships
**Issue:** `description`, `fromCardinality`, `toCardinality` not supported  
**Prevention:**
- [x] Never add `description`, `fromCardinality`, `toCardinality` to relationships
- [x] Use comments (`///`) for documentation instead

**Generator Code Check:**
```tmdl
# ✅ CORRECT
/// This relationship connects dates
relationship press_room_data_Date_Dim_Date_Date
    fromColumn: press_room_data.Date
    toColumn: Dim_Date.Date

# ❌ WRONG
relationship press_room_data_Date_Dim_Date_Date
    description: "Connects dates"  # WRONG
    fromCardinality: "Many"        # WRONG
    toCardinality: "One"           # WRONG
```

---

## ✅ Visual Container Structure Errors

### 9. `visualContainerObjects` at Root Level
**Issue:** `visualContainerObjects` must be inside `visual` object  
**Prevention:**
- [x] Always place `visualContainerObjects` inside `visual` object
- [x] Never place at root level of visual container
- [x] Never add to slicers (slicers don't support it)

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "visual": {
        "visualType": "donutChart",
        "visualContainerObjects": {  # Inside visual
            "visualTooltip": [...]
        }
    }
}

# ❌ WRONG
{
    "visual": {...},
    "visualContainerObjects": {...}  # At root - WRONG
}
```

---

### 10. `visualTooltip` Uses `section` Not `page`
**Issue:** `visualTooltip` must use `section` property  
**Prevention:**
- [x] Always use `section` (not `page`) in `visualTooltip`
- [x] `section` value matches page name

**Generator Code Check:**
```python
# ✅ CORRECT
"visualTooltip": [{
    "properties": {
        "section": {"expr": {"Literal": {"Value": "'tooltip_page'"}}}
    }
}]

# ❌ WRONG
"visualTooltip": [{
    "properties": {
        "page": {"expr": {"Literal": {"Value": "'tooltip_page'"}}}  # WRONG
    }
}]
```

---

### 11. Invalid `sortDefinition` in Table Visuals
**Issue:** `tableEx` visuals don't support `sortDefinition` in `queryState`  
**Prevention:**
- [x] Never add `sortDefinition` to `queryState` for `tableEx` visuals
- [x] Use Top N filters with OrderBy for table sorting

**Generator Code Check:**
```python
# ✅ CORRECT (tableEx)
visual = {
    "visual": {
        "visualType": "tableEx",
        "query": {
            "queryState": {
                "Values": {"projections": [...]}
                # NO sortDefinition here
            }
        }
    }
}

# ❌ WRONG
"queryState": {
    "Values": {...},
    "sortDefinition": {...}  # WRONG for tableEx
}
```

---

### 12. Invalid `Top` Property in Top N Filter
**Issue:** `Top` must be in `Query` object, not filter root  
**Prevention:**
- [x] Always place `Top` inside `Subquery.Query.Top`
- [x] Never place at filter root level

**Generator Code Check:**
```python
# ✅ CORRECT
"filter": {
    "Version": 2,
    "From": [{
        "Name": "subquery",
        "Expression": {
            "Subquery": {
                "Query": {
                    "Top": 10  # Inside Query
                }
            }
        }
    }]
}

# ❌ WRONG
"filter": {
    "Top": 10  # At root - WRONG
}
```

---

### 13. Missing `nativeQueryRef` in Projections
**Issue:** Projections missing `nativeQueryRef` property  
**Prevention:**
- [x] All projections include `queryRef` AND `nativeQueryRef`
- [x] `queryRef` = full qualified (e.g., `"Metrics.Total Views"`)
- [x] `nativeQueryRef` = field name only (e.g., `"Total Views"`)

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "field": {"Measure": {...}},
    "queryRef": "Metrics.Total Views",
    "nativeQueryRef": "Total Views",
    "active": true
}
```

---

### 14. Missing `active: true` in Projections
**Issue:** Projections without `active: true` don't display data  
**Prevention:**
- [x] ALL projections must have `active: true`
- [x] Generator sets this automatically for all projections

**Generator Code Check:**
```python
# ✅ CORRECT
"projections": [
    {
        "field": {...},
        "queryRef": "...",
        "nativeQueryRef": "...",
        "active": True  # REQUIRED
    }
]
```

---

### 15. `filterConfig` at Wrong Position
**Issue:** `filterConfig` must be at root level, not inside `visual`  
**Prevention:**
- [x] Always place `filterConfig` at root level of visual container
- [x] Never place inside `visual` object

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "visual": {...},
    "filterConfig": {...}  # At root
}

# ❌ WRONG
{
    "visual": {
        "filterConfig": {...}  # Inside visual - WRONG
    }
}
```

---

## ✅ Page Structure Errors

### 16. Invalid Visual Definitions in `objects` Section
**Issue:** Visuals in `page.json` `objects` section  
**Prevention:**
- [x] Never place visual definitions in `objects` section
- [x] Visuals must be in separate folders under `visuals/`
- [x] `objects` only contains `background`, `outspace`, etc.

**Generator Code Check:**
```python
# ✅ CORRECT
page_json = {
    "objects": {
        "background": [...]  # Only predefined types
    }
}
# Visuals created in: pages/{page_id}/visuals/{visual_name}/visual.json

# ❌ WRONG
page_json = {
    "objects": {
        "background": [...],
        "my_visual": [...]  # WRONG - visuals don't go here
    }
}
```

---

### 17. Missing `pages.json` or Invalid Structure
**Issue:** Missing `pages.json` or using `sections` instead of `pageOrder`  
**Prevention:**
- [x] Always create `pages.json` with `pageOrder` (array of strings)
- [x] Use `activePageName` (not `activeSectionName`)
- [x] Include `$schema` property

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
    "pageOrder": ["home", "releases", "channels"],
    "activePageName": "home"
}

# ❌ WRONG
{
    "sections": [...],           # WRONG
    "activeSectionName": "home"  # WRONG
}
```

---

## ✅ Cache Issues

### 18. Missing `definition.pbism` File
**Issue:** Required metadata file missing  
**Prevention:**
- [x] Always create `definition.pbism` in `.SemanticModel` folder
- [x] Include correct schema and version

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "4.2",
    "settings": {}
}
```

---

## ✅ Field Type Errors

### 19. Incorrect Field Type in Visual Queries
**Issue:** Using `Measure` for columns or `Column` for measures  
**Prevention:**
- [x] Validate field types against semantic model before generating
- [x] Use `Column` for table columns
- [x] Use `Measure` for calculated measures

**Generator Code Check:**
```python
# ✅ CORRECT
if field_type == "measure":
    field = {"Measure": {"Expression": {"SourceRef": {"Entity": table}}, "Property": field_name}}
elif field_type == "column":
    field = {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": field_name}}
```

---

## ✅ Bookmark Errors

### 20. Missing `explorationState` in Bookmarks
**Issue:** Bookmarks require `explorationState` property  
**Prevention:**
- [x] Always include `explorationState` in bookmark files
- [x] Include `options` property
- [x] Use schema version 1.4.0

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.4.0/schema.json",
    "name": "Bookmark_Clear_All_Filters",
    "displayName": "Clear All Filters",
    "options": {...},
    "explorationState": {
        "version": "1.0",
        "activeSection": "home",
        "sections": {...}
    }
}
```

---

## ✅ Encoding Issues

### 21. UTF-8 BOM in JSON Files
**Issue:** Power BI requires UTF-8 without BOM  
**Prevention:**
- [x] Always write JSON files with UTF-8 encoding (no BOM)
- [x] Python's `json.dump()` with `encoding='utf-8'` is correct
- [x] Never use PowerShell's `Set-Content -Encoding UTF8` (adds BOM)

**Generator Code Check:**
```python
# ✅ CORRECT (Python)
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# ❌ WRONG (PowerShell)
Set-Content -Encoding UTF8  # Adds BOM
```

---

## ✅ Visual-Specific Rules

### 22. Slicers Don't Support `visualContainerObjects`
**Issue:** Slicers cannot have `visualContainerObjects`  
**Prevention:**
- [x] Never add `visualContainerObjects` to slicer visuals
- [x] Use `objects.header.title` for slicer labels instead

**Generator Code Check:**
```python
# ✅ CORRECT (slicers)
if visual_type == "slicer":
    # NO visualContainerObjects
    visual = {
        "visual": {
            "visualType": "slicer",
            "objects": {
                "header": {
                    "title": {"text": "Channel"}
                }
            }
        }
    }
```

---

### 23. `altText` Not Supported in Visual JSON
**Issue:** Alt text cannot be set programmatically  
**Prevention:**
- [x] Never add `altText` to visual JSON files
- [x] Document that alt text must be configured manually in Power BI Desktop

**Generator Code Check:**
```python
# ❌ NEVER add
visual["visualContainerObjects"]["altText"] = "..."  # WRONG
```

---

## ✅ Sort Definition Rules

### 24. Sort Field Must Appear in Projections
**Issue:** `sortDefinition` references field not in projections  
**Prevention:**
- [x] If `sortDefinition` uses a different field than display (e.g., `YearMonth` for `Month_Year`), add both to projections
- [x] Sort field must be in the same bucket as display field

**Generator Code Check:**
```python
# ✅ CORRECT (Line Chart sorting by YearMonth, displaying Month_Year)
"Category": {
    "projections": [
        {"field": {"Column": {...}, "Property": "Month_Year"}, ...},  # Display
        {"field": {"Column": {...}, "Property": "YearMonth"}, ...}    # Sort key
    ]
},
"sortDefinition": {
    "sort": [{
        "field": {"Column": {...}, "Property": "YearMonth"},
        "direction": "Ascending"
    }]
}
```

---

## ✅ QueryRef Patterns

### 25. Measures with Spaces in `queryRef`/`nativeQueryRef`
**Issue:** Spaces must be preserved in measure names  
**Prevention:**
- [x] Preserve spaces in measure names exactly as they appear in model
- [x] `queryRef` = `"Table.Measure Name"` (spaces preserved)
- [x] `nativeQueryRef` = `"Measure Name"` (spaces preserved)

**Generator Code Check:**
```python
# ✅ CORRECT
{
    "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "Metrics"}}, "Property": "Total Views YTD"}},
    "queryRef": "Metrics.Total Views YTD",      # Spaces preserved
    "nativeQueryRef": "Total Views YTD"         # Spaces preserved
}
```

---

## 📋 Generator Validation Checklist

Before generating any visual, ensure:

- [ ] Visual type is valid Power BI visual type
- [ ] Query structure matches visual type (chart vs card vs slicer vs table)
- [ ] All projections have `active: true`
- [ ] All projections have both `queryRef` and `nativeQueryRef`
- [ ] Field types match semantic model (Column vs Measure)
- [ ] `visualContainerObjects` is inside `visual` object (if used)
- [ ] `visualContainerObjects` is NOT added to slicers
- [ ] `filterConfig` is at root level (if used)
- [ ] `sortDefinition` field appears in projections (if used)
- [ ] `sortDefinition` is NOT added to `tableEx` visuals
- [ ] Bucket names match visual type (Category/Y/Series for charts, Values for slicers/tables, Data for cards)
- [ ] No invalid properties (`drillFilterOtherVisuals`, `altText`, etc.)
- [ ] UTF-8 encoding without BOM for all JSON files

---

## 🔧 Post-Generation Validation

After generation, run:

```bash
# Comprehensive validation
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix

# Check measure/column bindings
python scripts/validators/check_all_measure_names.py
```

---

## 📚 Reference Documents

- **Common Issues:** `07_Guides/COMMON_PBIP_ISSUES.md`
- **Visual Generation Method:** `PRECISE_VISUAL_GENERATION_METHOD.md`
- **Visual Contracts:** `EXTRACTED_VISUAL_CONTRACTS.md`
- **Troubleshooting:** `docs/TROUBLESHOOTING.md`

---

**Last Updated:** January 2025  
**Status:** ✅ All 25 common issues mapped to generator prevention strategies
