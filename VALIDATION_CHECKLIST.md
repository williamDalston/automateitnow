# ✅ FOOLPROOF VALIDATION CHECKLIST

Quick reference for validating Power BI dashboards before and after generation.

---

## 🔍 PRE-GENERATION CHECKS

### Input Validation
- [ ] Blueprint JSON schema is valid
- [ ] All measure names exist in semantic model
- [ ] All table names exist
- [ ] All visual types are supported
- [ ] All field references are correct (Measure vs Column)

---

## 🔧 POST-GENERATION CHECKS

### File Structure
- [ ] `.pbip` file exists and is valid JSON
- [ ] `.pbip` uses `"report"` artifact (not `"dataset"`)
- [ ] `definition.pbir` exists and has `datasetReference`
- [ ] `report.json` does NOT have `datasetReference`
- [ ] `definition.pbism` exists for semantic model

### Visual Structure
- [ ] All visuals have `"active": true` in projections
- [ ] Slicers do NOT have `visualContainerObjects`
- [ ] Cards/charts DO have `visualContainerObjects` (inside `visual` object)
- [ ] All projections have correct `queryRef` format: `TableName.FieldName`
- [ ] All projections have `nativeQueryRef` matching field name
- [ ] Measure/Column types are correct

### TMDL Structure
- [ ] `relationships.tmdl` has no `description` property
- [ ] `relationships.tmdl` has no `fromCardinality` property
- [ ] `relationships.tmdl` has no `toCardinality` property
- [ ] All TMDL files are valid syntax
- [ ] No multiline measure expressions

### Data Bindings
- [ ] All measure references exist in semantic model
- [ ] All column references exist in semantic model
- [ ] Entity names match table names exactly
- [ ] Field names match measure/column names exactly

---

## 🚨 CRITICAL ISSUES (Must Fix)

1. **Missing `active: true`** → Visuals show no data
2. **Wrong `datasetReference` location** → Report can't find model
3. **Unsupported TMDL properties** → Power BI Desktop errors
4. **`visualContainerObjects` on slicers** → Schema validation errors
5. **Wrong Measure/Column type** → Visuals show errors

---

## ✅ VALIDATION COMMANDS

```bash
# Run master validator
python scripts/validators/master_pbip_validator.py "path/to/report.Report" --fix

# Check measure bindings
python scripts/validators/check_all_measure_names.py
```

---

## 📊 SUCCESS CRITERIA

✅ **All checks pass**  
✅ **Zero errors**  
✅ **File opens in Power BI Desktop**  
✅ **All visuals display data**  
✅ **No schema violations**

---

**Last Updated:** December 2024
