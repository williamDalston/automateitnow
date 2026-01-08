# 📋 PATTERN EXTRACTION PLAN

**Purpose:** Detailed plan to extract all working patterns from reference dashboard  
**Target:** `press-room-dashboard.pbip` in automation-system folder  
**Output:** Complete pattern library for flawless generation

---

## 🎯 EXTRACTION SCOPE

### Visual Types to Extract

1. **Card (KPI)** - `visualType: "card"`
2. **Slicer** - `visualType: "slicer"`
3. **Action Button** - `visualType: "actionButton"`
4. **Charts** - (if present in working dashboard)
   - Column charts
   - Bar charts
   - Line charts
   - Stacked charts

---

## 📊 EXTRACTION CHECKLIST

### For Each Visual Type

#### 1. Structure Extraction
- [ ] Complete `visual.json` structure
- [ ] `position` object (x, y, z, width, height)
- [ ] `visual` object structure
- [ ] `query` object structure
- [ ] `queryState` structure
- [ ] `projections` array structure
- [ ] `objects` structure (if present)
- [ ] `visualContainerObjects` structure (if present)
- [ ] `filterConfig` structure (if present)

#### 2. Query Pattern Extraction
- [ ] Projection structure
  - [ ] `field` object (Measure vs Column)
  - [ ] `queryRef` format
  - [ ] `nativeQueryRef` format
  - [ ] `active: true` presence
- [ ] Sort definitions (if present)
- [ ] Filter definitions (if present)

#### 3. Formatting Extraction
- [ ] `visualContainerObjects` structure
  - [ ] When present (cards, charts)
  - [ ] When absent (slicers)
  - [ ] Standard properties
- [ ] Color values
- [ ] Font settings
- [ ] Border settings
- [ ] Padding settings

#### 4. Position Pattern Extraction
- [ ] Grid system
- [ ] Spacing rules
- [ ] Alignment rules
- [ ] Z-index rules

---

## 🔍 SPECIFIC PATTERNS TO EXTRACT

### Pattern 1: Card (KPI) Visual

**Source:** Any working KPI card in reference dashboard

**Key Elements:**
```json
{
  "visualType": "card",
  "query": {
    "queryState": {
      "Data": {
        "projections": [
          {
            "field": {
              "Measure": {
                "Expression": {"SourceRef": {"Entity": "Metrics"}},
                "Property": "{{MEASURE_NAME}}"
              }
            },
            "queryRef": "Metrics.{{MEASURE_NAME}}",
            "nativeQueryRef": "{{MEASURE_NAME}}",
            "active": true
          }
        ]
      }
    }
  },
  "visualContainerObjects": {
    "background": [...],
    "border": [...],
    "visualHeader": [...]
  }
}
```

**Extract:**
- Complete structure
- Standard formatting
- Position patterns

---

### Pattern 2: Slicer Visual

**Source:** `79f5f9f9ae9d08a9c70b/visual.json` (date slicer)

**Key Elements:**
```json
{
  "visualType": "slicer",
  "query": {
    "queryState": {
      "Values": {
        "projections": [
          {
            "field": {
              "Column": {
                "Expression": {"SourceRef": {"Entity": "{{TABLE_NAME}}"}},
                "Property": "{{COLUMN_NAME}}"
              }
            },
            "queryRef": "{{TABLE_NAME}}.{{COLUMN_NAME}}",
            "nativeQueryRef": "{{COLUMN_NAME}}",
            "active": true
          }
        ]
      }
    }
  },
  "objects": {
    "data": [...],
    "general": [...],
    "header": [...]
  },
  "visualContainerObjects": {
    // Note: Present but minimal for slicers
  }
}
```

**Extract:**
- Complete structure
- Objects structure
- Filter configuration
- Visual container objects (minimal)

---

### Pattern 3: Action Button

**Source:** `43c3caa20026750d70d1/visual.json` (logo button)

**Key Elements:**
```json
{
  "visualType": "actionButton",
  "objects": {
    "icon": [...],
    "outline": [...],
    "fill": [...]
  },
  "visualContainerObjects": {
    "title": [...],
    "visualHeader": [...],
    "background": [...],
    "border": [...],
    "lockAspect": [...]
  }
}
```

**Extract:**
- Complete structure
- Objects structure
- Visual container objects
- Image reference patterns

---

## 📁 OUTPUT STRUCTURE

```
patterns/
├── working_visuals/
│   ├── card_template.json
│   ├── slicer_template.json
│   ├── action_button_template.json
│   └── chart_templates/
│       ├── column_chart_template.json
│       ├── bar_chart_template.json
│       └── stacked_column_template.json
│
├── working_structure/
│   ├── layouts.json
│   ├── positioning_rules.json
│   └── grid_system.json
│
└── style_library/
    ├── colors.json
    ├── typography.json
    ├── spacing.json
    └── visual_container_objects.json
```

---

## 🔧 EXTRACTION SCRIPT STRUCTURE

### Script: `extract_working_patterns.py`

```python
#!/usr/bin/env python3
"""
Extract working patterns from reference dashboard.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class PatternExtractor:
    def __init__(self, dashboard_path: Path):
        self.dashboard_path = dashboard_path
        self.patterns = {}
    
    def extract_all(self):
        """Extract all patterns from dashboard."""
        # 1. Extract visual patterns
        self.extract_visual_patterns()
        
        # 2. Extract style patterns
        self.extract_style_patterns()
        
        # 3. Extract layout patterns
        self.extract_layout_patterns()
        
        # 4. Save patterns
        self.save_patterns()
    
    def extract_visual_patterns(self):
        """Extract visual structure patterns."""
        # Find all visuals
        # Extract structure for each visual type
        # Create templates
        pass
    
    def extract_style_patterns(self):
        """Extract style and formatting patterns."""
        # Extract colors
        # Extract typography
        # Extract spacing
        # Extract visual container objects
        pass
    
    def extract_layout_patterns(self):
        """Extract layout and positioning patterns."""
        # Extract grid system
        # Extract positioning rules
        # Extract layout templates
        pass
    
    def save_patterns(self):
        """Save extracted patterns to files."""
        # Save to patterns/ directory
        pass
```

---

## ✅ VALIDATION OF EXTRACTED PATTERNS

### After Extraction

1. **Structure Validation**
   - [ ] All required fields present
   - [ ] JSON valid
   - [ ] Schema compliant

2. **Completeness Check**
   - [ ] All visual types extracted
   - [ ] All formatting extracted
   - [ ] All layout patterns extracted

3. **Template Validation**
   - [ ] Templates are parameterizable
   - [ ] Placeholders clearly marked
   - [ ] Easy to use in generation

---

## 🚀 USAGE AFTER EXTRACTION

### In Generation Script

```python
# Load pattern
card_pattern = load_pattern("patterns/working_visuals/card_template.json")

# Apply pattern
visual = apply_pattern(card_pattern, {
    "measure": "Total Views",
    "label": "Total Views",
    "format": "#,0",
    "position": {"x": 100, "y": 100, "width": 200, "height": 100}
})

# Validate
assert visual_valid(visual)
```

---

## 📝 EXTRACTION NOTES

### Important Observations

1. **Slicers have `visualContainerObjects`** - But minimal (background, border, padding)
2. **Cards always have `visualContainerObjects`** - Full structure
3. **Action buttons have `visualContainerObjects`** - But different structure
4. **All projections have `active: true`** - Critical!
5. **All projections have `queryRef` and `nativeQueryRef`** - Required

### Edge Cases

- Some visuals may not have `visualContainerObjects`
- Some visuals may have different object structures
- Some visuals may have custom formatting

**Solution:** Extract multiple examples, identify common patterns, document exceptions

---

**Status:** Ready to Execute  
**Estimated Time:** 2-3 hours  
**Priority:** CRITICAL - Foundation for flawless generation
