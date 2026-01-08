# Shell PBIP Identification & Visual Paths

**Status:** ✅ Complete  
**Date:** January 8, 2026

---

## 🎯 Best UI Shell PBIP

**Folder Name:** `press-room\press-room-dashboard.pbip`

**Full Path:** `C:\Users\farad\OneDrive\Desktop\press-room\press-room-dashboard.pbip`

**Why This One:**
- ✅ Has named pages (home, channels, landing, releases, release_detail)
- ✅ Contains actionButton visuals with image references
- ✅ Most complete structure with all page types
- ✅ Already has logo/image visuals configured
- ✅ Has proper canvas size (1280×720)

---

## 📍 Sample Visual Paths

### 1. Nav Button / Logo Visual (actionButton with image)

**Path:** 
```
press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json
```

**Full Path:**
```
C:\Users\farad\OneDrive\Desktop\press-room\press-room-dashboard.Report\definition\pages\86b448ef2a89e75fa80e\visuals\43c3caa20026750d70d1\visual.json
```

**Visual Type:** `actionButton`

**Key Properties:**
- Contains logo image reference: `'logo-white-bg.svg'`
- ResourcePackageItem: `RegisteredResources/logo-white-bg20252112630989272.svg`
- Position: `x: 31.25, y: 23.75` (header area)
- Size: `width: 295, height: 62.5`

**Use Case:** This visual can serve as both:
- Logo template (with image property)
- Nav button template (with action property)

---

### 2. Back Button Visual (actionButton with navigation)

**Path:**
```
press-room-dashboard.Report/definition/pages/release_detail/visuals/8b697bb06db35c96cb61/visual.json
```

**Full Path:**
```
C:\Users\farad\OneDrive\Desktop\press-room\press-room-dashboard.Report\definition\pages\release_detail\visuals\8b697bb06db35c96cb61\visual.json
```

**Visual Type:** `actionButton`

**Key Properties:**
- Shape type: `'back'` (built-in icon)
- Has visualLink with type: `'Back'`
- Position: `x: 20, y: 20, z: 3000` (top-left, high z-order)
- Size: `width: 44, height: 44`

**Use Case:** Template for navigation buttons (back, home, etc.)

---

## 🏗️ Generator Strategy Recommendation

**Recommended Approach:** **Clone Shell Page**

**Rationale:**
1. The `press-room` PBIP already has complete page structures
2. Header/nav/footer visuals are already positioned
3. Resource references are already configured
4. Generator only needs to swap content area visuals

**Implementation:**
1. Copy entire page structure from shell PBIP
2. Replace content visuals (KPIs, charts, tables) only
3. Patch navigation actions to correct target pages
4. Keep all image/resource references untouched

---

## 📋 Shell Components Available

From `press-room\press-room-dashboard.pbip`:

### Header Components
- ✅ Logo visual (actionButton with image) - **Path identified above**
- ✅ Background images (page-level objects.background)

### Navigation Components
- ✅ Back button (actionButton with visualLink) - **Path identified above**
- ✅ Nav buttons (can be extracted from other pages)

### Page Structure
- ✅ Named pages: `home`, `channels`, `landing`, `releases`, `release_detail`
- ✅ Canvas size: 1280×720
- ✅ Background images configured

---

## 🔧 Next Steps

1. **Extract Templates:**
   - Copy `43c3caa20026750d70d1/visual.json` → `_templates/visuals/actionButton_logo/visual.json`
   - Copy `8b697bb06db35c96cb61/visual.json` → `_templates/visuals/actionButton_nav/visual.json`
   - Extract other nav button visuals from shell pages

2. **Update Generator Config:**
   ```json
   {
     "shell": {
       "sourcePbip": "press-room/press-room-dashboard.pbip",
       "components": ["header", "nav", "footer"],
       "strategy": "clone_page"
     }
   }
   ```

3. **Test Generation:**
   - Generate one page using shell structure
   - Verify image references work
   - Verify navigation actions work

---

## 📚 Related Documents

- **`ASSET_HANDLING_GUIDE.md`** - Complete asset handling strategy
- **`PBIR_GENERATOR_APPROACH.md`** - Template-driven generation approach
- **`FINAL_DASHBOARD_SPEC.md`** - Dashboard specification

---

**Status:** ✅ Shell PBIP identified. Sample paths documented. Ready for template extraction.
