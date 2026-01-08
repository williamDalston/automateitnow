# 🔧 TROUBLESHOOTING GUIDE

Common issues and their solutions.

---

## ❌ Visuals Not Showing Data

### Symptoms
- Visuals appear but show no data
- "No data available" message
- Visuals are blank

### Causes & Solutions

#### 1. Missing `active: true` in Projections
**Check:**
```json
{
  "projections": [
    {
      "field": {...},
      "active": true  // ← Must be present
    }
  ]
}
```

**Fix:**
```bash
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix
```

#### 2. Wrong Measure/Column Type
**Check:** Visual uses `Measure` for a column or vice versa

**Fix:** Update field type in visual.json:
```json
{
  "field": {
    "Measure": {...}  // Use Measure for measures, Column for columns
  }
}
```

#### 3. Missing or Incorrect `datasetReference`
**Check:** `definition.pbir` has `datasetReference`

**Fix:** Ensure `definition.pbir` contains:
```json
{
  "datasetReference": {
    "byPath": {
      "path": "../dashboard.SemanticModel"
    }
  }
}
```

---

## ❌ Power BI Desktop Errors

### Error: "Property 'description' is unknown"

**Cause:** Unsupported property in `relationships.tmdl`

**Fix:**
```bash
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix
```

Remove from `relationships.tmdl`:
- `description`
- `fromCardinality`
- `toCardinality`

### Error: Schema Validation Failed

**Cause:** Invalid structure in JSON files

**Fix:**
1. Run validator: `python scripts/validators/master_pbip_validator.py --fix`
2. Check for:
   - Missing `$schema` properties
   - Invalid object structures
   - Wrong property locations

---

## ❌ Visual Container Objects Errors

### Error: Slicer has visualContainerObjects

**Cause:** Slicers don't support `visualContainerObjects`

**Fix:**
```bash
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix
```

This automatically removes `visualContainerObjects` from slicers.

---

## ❌ Measure/Column Not Found

### Error: "Measure 'X' not found"

**Cause:** Measure doesn't exist in semantic model

**Check:**
```bash
python scripts/validators/check_all_measure_names.py
```

**Fix:**
1. Verify measure exists in semantic model
2. Check spelling (case-sensitive)
3. Check table name matches

---

## 🔍 DIAGNOSTIC COMMANDS

### Full Validation
```bash
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix --verbose
```

### Check Bindings Only
```bash
python scripts/validators/check_all_measure_names.py
```

### Check Specific File
```bash
# Check relationships.tmdl
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --verbose | grep relationships
```

---

## 📋 VALIDATION CHECKLIST

Before opening in Power BI Desktop:

- [ ] Run `master_pbip_validator.py --fix`
- [ ] Run `check_all_measure_names.py`
- [ ] Check `VALIDATION_CHECKLIST.md`
- [ ] Verify all errors are fixed
- [ ] Clear Power BI Desktop cache (if needed)

---

## 🆘 STILL NOT WORKING?

1. **Check Working Dashboard**
   - Compare with `press-room-dashboard.pbip`
   - Look for structural differences

2. **Review Patterns**
   - See `FOOLPROOF_AUTOMATION_PLAN.md`
   - Check pattern library

3. **Verbose Output**
   - Run validators with `--verbose`
   - Check all warnings

4. **Clear Cache**
   - Delete `.pbir` files
   - Restart Power BI Desktop

---

**Last Updated:** December 2024
