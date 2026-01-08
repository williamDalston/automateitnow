#!/usr/bin/env python3
"""
Check all measure names in visuals against the semantic model.

This script:
1. Extracts all measure names from visual.json files
2. Extracts all measure names from the semantic model (TMDL files)
3. Compares them to find mismatches
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_measures_from_visual(visual_json_path: Path) -> list:
    """Extract all measure names from a visual.json file."""
    try:
        with open(visual_json_path, 'r', encoding='utf-8') as f:
            visual_data = json.load(f)
        
        measures = []
        visual = visual_data.get("visual", {})
        
        # Check queryState for measures
        if "query" in visual and "queryState" in visual["query"]:
            query_state = visual["query"]["queryState"]
            
            for bucket_name, bucket_data in query_state.items():
                if isinstance(bucket_data, dict) and "projections" in bucket_data:
                    for proj in bucket_data["projections"]:
                        if "field" in proj:
                            field = proj["field"]
                            if "Measure" in field:
                                entity = field["Measure"]["Expression"]["SourceRef"]["Entity"]
                                measure_name = field["Measure"]["Property"]
                                measures.append({
                                    "entity": entity,
                                    "measure": measure_name,
                                    "visual": visual_json_path.parent.name,
                                    "page": visual_json_path.parent.parent.parent.name
                                })
                            elif "Column" in field:
                                entity = field["Column"]["Expression"]["SourceRef"]["Entity"]
                                column_name = field["Column"]["Property"]
                                measures.append({
                                    "entity": entity,
                                    "column": column_name,
                                    "visual": visual_json_path.parent.name,
                                    "page": visual_json_path.parent.parent.parent.name
                                })
        
        return measures
    except Exception as e:
        print(f"  [ERROR] Failed to read {visual_json_path}: {e}")
        return []

def extract_measures_from_tmdl(tmdl_file: Path) -> dict:
    """Extract all measure names from a TMDL file."""
    measures = {}
    columns = {}
    
    try:
        content = tmdl_file.read_text(encoding='utf-8')
        
        # Extract table name from file path or content
        table_name = tmdl_file.stem
        
        # Find all measure definitions
        # TMDL format: measure 'Measure Name' = ... (with tabs, single quotes)
        # Pattern matches: measure 'Name' or measure "Name" (both single and double quotes)
        measure_pattern = r'measure\s+[\'"]([^\'"]+)[\'"]\s*='
        for match in re.finditer(measure_pattern, content, re.IGNORECASE | re.MULTILINE):
            measure_name = match.group(1)
            measures[measure_name] = {
                "table": table_name,
                "line": content[:match.start()].count('\n') + 1
            }
        
        # Find all column definitions
        # TMDL format: column 'Column Name' = ... or column "Column Name"
        column_pattern = r'column\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(column_pattern, content, re.IGNORECASE | re.MULTILINE):
            column_name = match.group(1)
            columns[column_name] = {
                "table": table_name,
                "line": content[:match.start()].count('\n') + 1
            }
        
    except Exception as e:
        print(f"  [ERROR] Failed to read {tmdl_file}: {e}")
    
    return measures, columns

def main():
    report_path = Path("C:/Users/farad/OneDrive/Desktop/press-room-fresh/press-room-dashboard.Report")
    semantic_model_path = Path("C:/Users/farad/OneDrive/Desktop/press-room-fresh/press-room-dashboard.SemanticModel")
    
    print("="*80)
    print("Check All Measure Names".center(80))
    print("="*80)
    print()
    
    # Step 1: Extract measures from visuals
    print("STEP 1: Extracting measures from visuals...")
    print("-" * 80)
    visual_measures = []
    visual_columns = []
    pages_dir = report_path / "definition" / "pages"
    
    visual_json_files = list(pages_dir.rglob("visuals/*/visual.json"))
    print(f"Found {len(visual_json_files)} visuals to check")
    
    for visual_json_path in visual_json_files:
        measures = extract_measures_from_visual(visual_json_path)
        for m in measures:
            if "measure" in m:
                visual_measures.append(m)
            if "column" in m:
                visual_columns.append(m)
    
    print(f"  Found {len(visual_measures)} measure references")
    print(f"  Found {len(visual_columns)} column references")
    print()
    
    # Step 2: Extract measures from semantic model
    print("STEP 2: Extracting measures from semantic model...")
    print("-" * 80)
    semantic_measures = {}
    semantic_columns = {}
    
    tmdl_files = list(semantic_model_path.rglob("*.tmdl"))
    print(f"Found {len(tmdl_files)} TMDL files")
    
    for tmdl_file in tmdl_files:
        measures, columns = extract_measures_from_tmdl(tmdl_file)
        semantic_measures.update(measures)
        semantic_columns.update(columns)
    
    print(f"  Found {len(semantic_measures)} measures in semantic model")
    print(f"  Found {len(semantic_columns)} columns in semantic model")
    print()
    
    # Step 3: Compare
    print("STEP 3: Comparing visuals vs semantic model...")
    print("-" * 80)
    
    # Group visual measures by entity
    visual_by_entity = defaultdict(list)
    for vm in visual_measures:
        entity = vm.get("entity", "Unknown")
        measure_name = vm.get("measure", "Unknown")
        visual_by_entity[entity].append({
            "measure": measure_name,
            "visual": vm.get("visual"),
            "page": vm.get("page")
        })
    
    # Check for mismatches
    issues = []
    all_measures_used = set()
    
    for entity, measures_list in visual_by_entity.items():
        for item in measures_list:
            measure_name = item["measure"]
            all_measures_used.add(measure_name)
            
            if measure_name not in semantic_measures:
                issues.append({
                    "type": "missing_measure",
                    "entity": entity,
                    "measure": measure_name,
                    "visual": item["visual"],
                    "page": item["page"]
                })
    
    # Check for columns
    visual_columns_by_entity = defaultdict(list)
    for vc in visual_columns:
        entity = vc.get("entity", "Unknown")
        column_name = vc.get("column", "Unknown")
        visual_columns_by_entity[entity].append({
            "column": column_name,
            "visual": vc.get("visual"),
            "page": vc.get("page")
        })
    
    for entity, columns_list in visual_columns_by_entity.items():
        for item in columns_list:
            column_name = item["column"]
            if column_name not in semantic_columns:
                issues.append({
                    "type": "missing_column",
                    "entity": entity,
                    "column": column_name,
                    "visual": item["visual"],
                    "page": item["page"]
                })
    
    # Step 4: Report
    print()
    print("="*80)
    print("RESULTS".center(80))
    print("="*80)
    print()
    
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        print()
        
        missing_measures = [i for i in issues if i["type"] == "missing_measure"]
        missing_columns = [i for i in issues if i["type"] == "missing_column"]
        
        if missing_measures:
            print(f"Missing Measures ({len(missing_measures)}):")
            print("-" * 80)
            for issue in missing_measures:
                print(f"  ❌ Measure '{issue['measure']}' in entity '{issue['entity']}'")
                print(f"     Used in: {issue['page']}/visuals/{issue['visual']}")
            print()
        
        if missing_columns:
            print(f"Missing Columns ({len(missing_columns)}):")
            print("-" * 80)
            for issue in missing_columns:
                print(f"  ❌ Column '{issue['column']}' in entity '{issue['entity']}'")
                print(f"     Used in: {issue['page']}/visuals/{issue['visual']}")
            print()
    else:
        print("✅ All measure and column names match!")
        print()
    
    # Show summary of what's being used
    print("SUMMARY:")
    print("-" * 80)
    print(f"  Unique measures referenced: {len(all_measures_used)}")
    print(f"  Measures in semantic model: {len(semantic_measures)}")
    print(f"  Columns referenced: {len(set(vc.get('column') for vc in visual_columns))}")
    print(f"  Columns in semantic model: {len(semantic_columns)}")
    print()
    
    # List all measures being used
    if all_measures_used:
        print("Measures being used in visuals:")
        for measure in sorted(all_measures_used):
            status = "✅" if measure in semantic_measures else "❌"
            print(f"  {status} {measure}")
        print()
    
    # List all measures in semantic model (for reference)
    if semantic_measures:
        print("All measures in semantic model:")
        for measure in sorted(semantic_measures.keys()):
            table = semantic_measures[measure]["table"]
            used = "✓" if measure in all_measures_used else " "
            print(f"  [{used}] {measure} (in {table})")
        print()

if __name__ == "__main__":
    main()

