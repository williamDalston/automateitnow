# 🚀 Quick Start: Generate Your First PBIR

**Time Estimate:** 30-45 minutes  
**Prerequisites:** Python 3.8+, Power BI Desktop

---

## Step 1: Extract Templates (15 min)

### A. Copy Shell PBIP

```powershell
# Navigate to automation-system
cd C:\Users\farad\OneDrive\Desktop\automation-system

# Create pbir_base directory
New-Item -ItemType Directory -Path "pbir_base" -Force

# Copy shell PBIP
Copy-Item -Path "C:\Users\farad\OneDrive\Desktop\press-room\press-room-dashboard.pbip" -Destination "pbir_base\" -Recurse
```

### B. Create Template Structure

```powershell
# Create template directories
$templateBase = "pbir_base\_templates\visuals"
New-Item -ItemType Directory -Path "$templateBase\card" -Force
New-Item -ItemType Directory -Path "$templateBase\table" -Force
New-Item -ItemType Directory -Path "$templateBase\slicer" -Force
New-Item -ItemType Directory -Path "$templateBase\hundredPercentStackedColumnChart" -Force
New-Item -ItemType Directory -Path "$templateBase\donutChart" -Force
New-Item -ItemType Directory -Path "$templateBase\lineChart" -Force
New-Item -ItemType Directory -Path "$templateBase\actionButton_logo" -Force
New-Item -ItemType Directory -Path "$templateBase\actionButton_nav" -Force
```

### C. Extract One Visual of Each Type

**From shell PBIP, copy one visual.json of each type:**

1. **Card:** Copy from `home/visuals/kpi_total_views/visual.json`
2. **Table:** Copy from `home/visuals/top10_table/visual.json`
3. **Slicer:** Copy from `home/visuals/date_slicer/visual.json`
4. **Stacked Chart:** Copy from `home/visuals/top10_vs_remaining/visual.json`
5. **Donut:** Copy from `home/visuals/channel_share/visual.json` (if exists)
6. **Line Chart:** Copy from `channels/visuals/channel_over_time/visual.json` (if exists)
7. **Logo Button:** Copy from `86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json`
8. **Nav Button:** Copy from `release_detail/visuals/8b697bb06db35c96cb61/visual.json`

**Save each to:** `pbir_base\_templates\visuals\<visualType>\visual.json`

### D. Insert Placeholders

**For each template, replace field references with placeholders:**

- `"queryRef": "Metrics.Total Views"` → `"queryRef": "__Y_AXIS__"`
- `"nativeQueryRef": "Total Views"` → `"nativeQueryRef": "__Y_AXIS_NATIVE__"`
- `"name": "kpi_total_views"` → `"name": "__VISUAL_NAME__"`
- Title text → `__TITLE__`

**See `PBIR_GENERATOR_APPROACH.md` for complete placeholder list.**

---

## Step 2: Create Config JSON (5 min)

### A. Extract from Spec

Copy the "AUTOMATION-READY CONFIGURATION" JSON from `FINAL_DASHBOARD_SPEC.md`

### B. Save as dashboard_config.json

```json
{
  "shell": {
    "sourcePbip": "press-room/press-room-dashboard.pbip",
    "components": ["header", "nav", "footer"],
    "strategy": "clone_page"
  },
  "pages": [
    {
      "id": "home",
      "displayName": "Executive Overview",
      "kpis": [ ... ],
      "visuals": [ ... ]
    }
  ]
}
```

---

## Step 3: Run Generator (2 min)

```bash
python pbir_generate.py \
  --config dashboard_config.json \
  --base pbir_base \
  --out pbir_out
```

**Expected Output:**
```
✅ Generated PBIR into: pbir_out
🧾 Validation report: pbir_out/validation_report.json
```

---

## Step 4: Validate (2 min)

```bash
python master_pbip_validator.py pbir_out --check-only --verbose
```

**Fix any errors before proceeding.**

---

## Step 5: Test in Power BI Desktop (10 min)

1. **Open PBIR:**
   - Open Power BI Desktop
   - File → Open → Browse
   - Navigate to `pbir_out/press-room-dashboard.pbip`
   - Click Open

2. **Verify:**
   - ✅ All visuals render
   - ✅ No error messages
   - ✅ Images/icons display
   - ✅ Navigation works
   - ✅ Measures calculate

3. **Test Navigation:**
   - Click nav buttons
   - Verify page transitions
   - Check drillthrough (if configured)

---

## Step 6: Iterate (As Needed)

**If issues found:**

1. **Check Validation Report:**
   - Review `pbir_out/validation_report.json`
   - Fix template placeholders
   - Re-run generator

2. **Check Visual Contracts:**
   - Review `PRECISE_VISUAL_GENERATION_METHOD.md`
   - Verify queryState structure
   - Check sortDefinition

3. **Check Common Issues:**
   - Review `COMMON_PBIP_ISSUES.md`
   - Apply fixes
   - Re-validate

---

## 🎯 Success Checklist

After generation, verify:

- [ ] All pages exist and open
- [ ] All visuals render (no blank visuals)
- [ ] KPI cards show values
- [ ] Charts display data
- [ ] Slicers work
- [ ] Navigation buttons work
- [ ] Images/icons display
- [ ] No validation errors
- [ ] Measures calculate correctly

---

## 🚨 Troubleshooting

### "Missing template" error
**Fix:** Ensure all visual types have templates in `pbir_base/_templates/visuals/`

### "Invalid field ref" error
**Fix:** Check `Table[Field]` format in config JSON matches model

### "JSON parse error" in validator
**Fix:** Check for JSON comments (`/* */` or `//`) in generated files

### Visuals don't render
**Fix:** 
1. Check `datasetReference` in `report.json`
2. Verify field references match model
3. Check `queryState` structure matches templates

### Images don't display
**Fix:**
1. Verify ResourcePackageItem references match shell PBIP
2. Check StaticResources folder exists
3. Ensure image files are in RegisteredResources

---

## 📚 Next Steps

Once generation works:

1. **Generate All Pages:** Update config with all 6 pages
2. **Add Drillthrough:** Configure drillthrough actions
3. **Polish UI:** Adjust positions, colors, formatting
4. **Connect Real Data:** Point to production semantic model
5. **Deploy:** Publish to Power BI Service

---

## 🎉 You're Ready!

Follow these steps and you'll have a working PBIR in under an hour.

**Questions?** Check:
- `FINAL_DASHBOARD_SPEC.md` - Complete specification
- `PRECISE_VISUAL_GENERATION_METHOD.md` - Visual contracts
- `PBIR_GENERATOR_APPROACH.md` - Generation methodology
- `ASSET_HANDLING_GUIDE.md` - Asset strategy

---

**Status:** ✅ Ready to generate your first PBIR!
