# Asset Handling Guide: UI Shell & Resource References

**Status:** ✅ Production-Ready  
**Version:** 1.0  
**Last Updated:** January 8, 2026

---

## 🎯 Golden Rule: No Schema Guessing for Images

**Do not hand-invent how PBIR stores images.**  
Power BI uses resource references that are easy to break if you "approximate" the JSON.

**Solution:** Import/place assets once in ONE "shell template PBIP", then reuse those exact visual.json blocks.

---

## 📋 Best UI Shell PBIP

**Recommended:** `press-room\press-room-dashboard.pbip`

**Why:**
- ✅ Has named pages (home, channels, landing, releases, release_detail)
- ✅ Contains actionButton visuals with image references
- ✅ Most complete structure with all page types
- ✅ Already has logo/image visuals configured

**Alternative:** `press-room-final\press-room-dashboard.pbip` (6 pages, similar structure)

---

## 🖼️ Asset-to-UI Mapping (Locked)

### Header Band (56px)

| Asset | Usage | Visual Type |
|-------|-------|-------------|
| `hhs_logo.svg` or `hhs-website-logo.svg` | Left side near title | actionButton (with image) |
| `hhs_federal_header.svg` | Subtle header ornament (optional) | actionButton or image visual |
| `hhs_accent_line.svg` | Thin underline separator (optional) | actionButton or image visual |
| `icon_info.svg` | Metric Dictionary link (right side) | actionButton (with navigation action) |

### Nav Rail (56px)

| Asset | Usage | Visual Type |
|-------|-------|-------------|
| `icon_home.svg` | Overview page button | actionButton (with navigation action) |
| `icon_releases.svg` | Releases page button | actionButton (with navigation action) |
| `icon_channels.svg` or `icon_chart.svg` | Channels page button | actionButton (with navigation action) |
| `icon_chart.svg` | Press Home page button | actionButton (with navigation action) |
| `icon_dictionary.svg` or `icon_info.svg` | Metric Dictionary link (bottom) | actionButton (with navigation action) |

### Footer (24px)

- **Text only:** "INTERNAL USE ONLY" (centered)
- **No seals** (unless formal requirement exists)

---

## 📍 Sample Visual Paths (From press-room PBIP)

### Nav Button Visual (actionButton)
**Path:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json`

**Key Properties:**
- `visualType: "actionButton"`
- `objects.icon[].properties.image.image` → ResourcePackageItem reference
- `objects.actionButton[].properties.action` → Navigation action to target page

### Logo Visual (actionButton with image)
**Path:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json`

**Key Properties:**
- `visualType: "actionButton"`
- `objects.icon[].properties.image.image.name` → `'logo-white-bg.svg'`
- `objects.icon[].properties.image.image.url` → ResourcePackageItem with PackageName/ItemName

**Example Resource Reference:**
```json
{
  "ResourcePackageItem": {
    "PackageName": "RegisteredResources",
    "PackageType": 1,
    "ItemName": "logo-white-bg20252112630989272.svg"
  }
}
```

---

## 🔧 Generator Asset Strategy

### Option A: Clone Shell Page (Recommended)

**If shell PBIP already has:**
- Header visuals placed
- Nav rail icons as buttons
- Footer text

**Generator behavior:**
1. Copy entire shell page structure to each generated page
2. Replace content area visuals (KPIs, charts) only
3. Patch navigation actions to correct target pages
4. Keep all image resource references untouched

**Advantages:**
- Zero schema guessing
- Resource references preserved exactly
- Header/footer/nav consistent across all pages

### Option B: Reusable Shell Components

**If shell visuals are separate components:**

**Generator behavior:**
1. On every generated page, create shell visuals first:
   - `header_logo` (deterministic ID or same ID each time)
   - `header_info_icon`
   - `nav_overview_btn`, `nav_releases_btn`, etc.
   - `footer_text`
2. Then add page-specific content visuals

**Template Structure:**
```
_templates/
  visuals/
    actionButton_logo/visual.json
    actionButton_nav/visual.json
    actionButton_info/visual.json
```

---

## 📝 Generator Config Extension

Add to your dashboard config JSON:

```json
{
  "uiAssets": {
    "logo": "assets/hhs_logo.svg",
    "icons": {
      "home": "assets/icon_home.svg",
      "releases": "assets/icon_releases.svg",
      "channels": "assets/icon_channels.svg",
      "press_home": "assets/icon_chart.svg",
      "info": "assets/icon_info.svg",
      "dictionary": "assets/icon_dictionary.svg"
    },
    "decor": {
      "header_line": "assets/hhs_accent_line.svg",
      "header_banner": "assets/hhs_federal_header.svg"
    }
  },
  "shell": {
    "sourcePbip": "press-room/press-room-dashboard.pbip",
    "components": ["header", "nav", "footer"],
    "strategy": "clone_page"  // or "inject_components"
  }
}
```

**Note:** Even if generator doesn't directly reference these paths, it's useful as a human-readable contract for which PBIP is the UI source.

---

## ✅ Template Checklist (Before Generation)

**Templates Required (visual.json specimens):**
- [x] card KPI template
- [x] table template
- [x] slicer template
- [x] 100% stacked column template
- [x] line chart template
- [x] donut/bar template
- [x] **actionButton template (nav button)**
- [x] **actionButton template (logo/image)**

**Shell Components Required:**
- [x] Header band visuals (logo, info icon)
- [x] Footer band visuals (text)
- [x] Nav rail visuals (5 buttons)
- [x] Canvas size: 1280×720

**Shell PBIP Identified:**
- ✅ **Best Shell:** `press-room\press-room-dashboard.pbip`
- ✅ **Nav Button Sample:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json`
- ✅ **Logo Sample:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json` (same visual, contains logo image)

---

## 🔍 Resource Reference Pattern

**Power BI stores images as:**
1. **File in StaticResources/RegisteredResources/** (actual file)
2. **Reference in visual.json** via ResourcePackageItem:
   ```json
   {
     "ResourcePackageItem": {
       "PackageName": "RegisteredResources",
       "PackageType": 1,
       "ItemName": "logo-white-bg20252112630989272.svg"
     }
   }
   ```

**Generator Rule:**
- **Never create ResourcePackageItem references manually**
- **Always copy from exported PBIP specimens**
- **Reuse exact visual.json blocks that contain image references**

---

## 🚀 Implementation Steps

1. **Identify Shell PBIP:** `press-room\press-room-dashboard.pbip` ✅
2. **Extract Shell Visuals:**
   - Copy actionButton visuals from shell pages
   - Extract logo visual (actionButton with image)
   - Extract nav button visuals (actionButton with navigation actions)
3. **Create Templates:**
   - `_templates/visuals/actionButton_logo/visual.json`
   - `_templates/visuals/actionButton_nav/visual.json`
   - `_templates/visuals/actionButton_info/visual.json`
4. **Update Generator:**
   - Add shell component injection logic
   - Reuse exact visual.json blocks (no schema modification)
   - Patch only navigation target pages

---

## 📚 Related Documents

- **`PBIR_GENERATOR_APPROACH.md`** - Template-driven generation approach
- **`FINAL_DASHBOARD_SPEC.md`** - Complete dashboard specification
- **`pbir_generate.py`** - Generator script

---

**Status:** ✅ Shell PBIP identified. Sample paths documented. Ready for template extraction.
