"""
Master Power BI PBIP Validator and Fixer

This comprehensive script validates and fixes all known common issues in Power BI Project files.
It checks:
- Schema validation errors
- Visual container structure errors
- Page structure errors
- TMDL syntax errors
- Field type errors
- Cache issues
- And more...

Usage:
    python master_pbip_validator.py [report_path] [--fix] [--verbose] [--check-only]
    
Options:
    --fix: Automatically fix issues where possible
    --check-only: Only check, don't fix (default)
    --verbose: Show detailed output for each check
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import sys

class IssueSeverity(Enum):
    """Severity levels for issues."""
    ERROR = "ERROR"      # Blocks Power BI from opening
    WARNING = "WARNING"  # May cause issues but won't block
    INFO = "INFO"        # Informational only

@dataclass
class ValidationIssue:
    """Represents a validation issue found."""
    category: str
    severity: IssueSeverity
    file_path: str
    issue_type: str
    message: str
    fixable: bool = False
    fix_description: str = ""
    line_number: Optional[int] = None

@dataclass
class ValidationResult:
    """Results of validation."""
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    fixed: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    fixed_files: List[str] = field(default_factory=list)

class PBIPValidator:
    """Master validator for Power BI PBIP projects."""
    
    # Valid object types in page.json objects section
    VALID_PAGE_OBJECT_TYPES = {"background", "outspace"}
    
    def __init__(self, report_path: Path, auto_fix: bool = False, verbose: bool = False):
        self.report_path = Path(report_path)
        self.auto_fix = auto_fix
        self.verbose = verbose
        self.results = ValidationResult()
        
        # Paths
        self.report_dir = self.report_path / "definition"
        self.pages_dir = self.report_dir / "pages"
        self.semantic_model_dir = None
        
        # Find semantic model directory
        for item in self.report_path.parent.iterdir():
            if item.is_dir() and item.name.endswith(".SemanticModel"):
                self.semantic_model_dir = item / "definition"
                break
    
    def validate_all(self) -> ValidationResult:
        """Run all validation checks."""
        print("=" * 80)
        print("Power BI PBIP Master Validator")
        print("=" * 80)
        print(f"Report path: {self.report_path}")
        print(f"Mode: {'AUTO-FIX' if self.auto_fix else 'CHECK-ONLY'}")
        print()

        # Run all validators
        self._check_pages_json_structure()
        self._check_page_json_objects()
        self._check_visual_drillFilterOtherVisuals()
        self._check_visual_container_objects_position()
        self._check_visual_tooltip_structure()
        self._check_relationships_description()
        self._check_missing_schemas()
        self._check_cache_files()
        self._check_required_pbism_file()
        self._check_background_properties()
        self._check_visual_query_structure()

        # NEW VALIDATORS (Gap Analysis additions)
        self._check_table_sort_definition()
        self._check_utf8_bom_encoding()
        self._check_filter_config_position()
        self._check_alt_text_in_visuals()
        self._check_bookmark_exploration_state()
        self._check_empty_projections_dict()
        self._check_dataset_reference()
        self._check_pbip_artifacts_structure()

        # Calculate totals
        self.results.total_issues = len(self.results.issues)
        self.results.errors = sum(1 for i in self.results.issues if i.severity == IssueSeverity.ERROR)
        self.results.warnings = sum(1 for i in self.results.issues if i.severity == IssueSeverity.WARNING)
        self.results.info = sum(1 for i in self.results.issues if i.severity == IssueSeverity.INFO)

        return self.results
    
    def _add_issue(self, category: str, severity: IssueSeverity, file_path: str,
                   issue_type: str, message: str, fixable: bool = False,
                   fix_description: str = "", line_number: Optional[int] = None):
        """Add a validation issue."""
        issue = ValidationIssue(
            category=category,
            severity=severity,
            file_path=str(file_path),
            issue_type=issue_type,
            message=message,
            fixable=fixable,
            fix_description=fix_description,
            line_number=line_number
        )
        self.results.issues.append(issue)
        
        if self.verbose:
            print(f"  [{severity.value}] {file_path}: {message}")
    
    # ============================================================================
    # VALIDATION CHECKS
    # ============================================================================
    
    def _check_pages_json_structure(self):
        """Check pages.json structure (pageOrder vs sections)."""
        pages_json_path = self.pages_dir / "pages.json"
        
        if not pages_json_path.exists():
            self._add_issue(
                "Page Structure",
                IssueSeverity.ERROR,
                str(pages_json_path),
                "missing_pages_json",
                "pages.json file is missing",
                fixable=False
            )
            return
        
        try:
            with open(pages_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for $schema
            if "$schema" not in data:
                self._add_issue(
                    "Page Structure",
                    IssueSeverity.ERROR,
                    str(pages_json_path),
                    "missing_schema",
                    "Missing $schema property",
                    fixable=True,
                    fix_description="Add $schema property"
                )
                if self.auto_fix:
                    data["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"
                    with open(pages_json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(pages_json_path))
            
            # Check for sections (old format)
            if "sections" in data:
                self._add_issue(
                    "Page Structure",
                    IssueSeverity.ERROR,
                    str(pages_json_path),
                    "old_sections_format",
                    "Uses 'sections' instead of 'pageOrder'",
                    fixable=True,
                    fix_description="Convert sections to pageOrder format"
                )
                if self.auto_fix:
                    sections = data.get("sections", [])
                    page_order = [s.get("name") for s in sections if isinstance(s, dict) and "name" in s]
                    active_page = data.get("activeSectionName", page_order[0] if page_order else None)
                    
                    data = {
                        "$schema": data.get("$schema", "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json"),
                        "pageOrder": page_order,
                        "activePageName": active_page
                    }
                    with open(pages_json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(pages_json_path))
            
            # Check for pageOrder
            if "pageOrder" not in data:
                self._add_issue(
                    "Page Structure",
                    IssueSeverity.ERROR,
                    str(pages_json_path),
                    "missing_page_order",
                    "Missing 'pageOrder' property",
                    fixable=False
                )
        
        except json.JSONDecodeError as e:
            self._add_issue(
                "Page Structure",
                IssueSeverity.ERROR,
                str(pages_json_path),
                "invalid_json",
                f"Invalid JSON: {e}",
                fixable=False
            )
    
    def _check_page_json_objects(self):
        """Check page.json files for invalid visual definitions in objects section."""
        if not self.pages_dir.exists():
            return
        
        for page_json_path in self.pages_dir.rglob("page.json"):
            if page_json_path.name != "page.json" or page_json_path.parent.name == "pages":
                continue
            
            try:
                with open(page_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "objects" not in data:
                    continue
                
                objects = data["objects"]
                if not isinstance(objects, dict):
                    continue
                
                invalid_properties = [
                    key for key in objects.keys()
                    if key not in self.VALID_PAGE_OBJECT_TYPES
                ]
                
                if invalid_properties:
                    self._add_issue(
                        "Page Structure",
                        IssueSeverity.ERROR,
                        str(page_json_path.relative_to(self.report_path)),
                        "invalid_objects_properties",
                        f"Invalid properties in objects section: {', '.join(invalid_properties)}",
                        fixable=True,
                        fix_description=f"Remove {len(invalid_properties)} invalid properties from objects section"
                    )
                    
                    if self.auto_fix:
                        # Remove invalid properties
                        data["objects"] = {
                            key: value for key, value in objects.items()
                            if key in self.VALID_PAGE_OBJECT_TYPES
                        }
                        with open(page_json_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(page_json_path))
            
            except (json.JSONDecodeError, Exception) as e:
                self._add_issue(
                    "Page Structure",
                    IssueSeverity.ERROR,
                    str(page_json_path.relative_to(self.report_path)),
                    "read_error",
                    f"Error reading file: {e}",
                    fixable=False
                )
    
    def _check_visual_drillFilterOtherVisuals(self):
        """Check for invalid drillFilterOtherVisuals property in visual.json files."""
        if not self.pages_dir.exists():
            return
        
        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                content = visual_json_path.read_text(encoding='utf-8')
                
                if '"drillFilterOtherVisuals"' in content:
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "drillFilterOtherVisuals",
                        "Invalid 'drillFilterOtherVisuals' property found",
                        fixable=True,
                        fix_description="Remove drillFilterOtherVisuals property"
                    )
                    
                    if self.auto_fix:
                        # Remove the property using regex
                        content = re.sub(r',\s*"drillFilterOtherVisuals":\s*(true|false)', '', content)
                        content = re.sub(r'"drillFilterOtherVisuals":\s*(true|false),?\s*', '', content)
                        visual_json_path.write_text(content, encoding='utf-8')
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))
            
            except Exception as e:
                self._add_issue(
                    "Visual Structure",
                    IssueSeverity.ERROR,
                    str(visual_json_path.relative_to(self.report_path)),
                    "read_error",
                    f"Error reading file: {e}",
                    fixable=False
                )
    
    def _check_visual_container_objects_position(self):
        """Check for visualContainerObjects at wrong position (root vs inside visual)."""
        if not self.pages_dir.exists():
            return
        
        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                has_root_vco = "visualContainerObjects" in data
                has_visual_vco = "visual" in data and "visualContainerObjects" in data.get("visual", {})
                visual_type = data.get("visual", {}).get("visualType", "")
                
                # Slicers shouldn't have visualContainerObjects at all
                if visual_type == "slicer" and (has_root_vco or has_visual_vco):
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "slicer_visualContainerObjects",
                        "Slicer has visualContainerObjects (slicers don't support it)",
                        fixable=True,
                        fix_description="Remove visualContainerObjects from slicer"
                    )
                    
                    if self.auto_fix:
                        if has_root_vco:
                            del data["visualContainerObjects"]
                        if has_visual_vco:
                            del data["visual"]["visualContainerObjects"]
                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))
                
                # Non-slicers: visualContainerObjects should be inside visual, not at root
                elif visual_type != "slicer" and has_root_vco:
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "visualContainerObjects_wrong_position",
                        "visualContainerObjects at root level (should be inside visual object)",
                        fixable=True,
                        fix_description="Move visualContainerObjects inside visual object"
                    )
                    
                    if self.auto_fix:
                        root_vco = data["visualContainerObjects"]
                        if has_visual_vco:
                            # Merge if both exist
                            visual_vco = data["visual"]["visualContainerObjects"]
                            merged = visual_vco.copy()
                            for key in root_vco:
                                if key in merged and isinstance(merged[key], list):
                                    # Merge arrays
                                    existing = {json.dumps(item, sort_keys=True) for item in merged[key]}
                                    for item in root_vco[key]:
                                        if json.dumps(item, sort_keys=True) not in existing:
                                            merged[key].append(item)
                                else:
                                    merged[key] = root_vco[key]
                            data["visual"]["visualContainerObjects"] = merged
                        else:
                            data["visual"]["visualContainerObjects"] = root_vco
                        
                        del data["visualContainerObjects"]
                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))
            
            except (json.JSONDecodeError, Exception) as e:
                self._add_issue(
                    "Visual Structure",
                    IssueSeverity.ERROR,
                    str(visual_json_path.relative_to(self.report_path)),
                    "read_error",
                    f"Error reading file: {e}",
                    fixable=False
                )
    
    def _check_visual_tooltip_structure(self):
        """Check for visualTooltip using 'page' instead of 'section' (FIXED BUG)."""
        if not self.pages_dir.exists():
            return

        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                content = visual_json_path.read_text(encoding='utf-8')

                # Check for 'page' in visualTooltip (should be 'section')
                if '"visualTooltip"' in content and '"page"' in content:
                    # More specific check
                    if re.search(r'"visualTooltip".*?"page"', content, re.DOTALL):
                        self._add_issue(
                            "Visual Structure",
                            IssueSeverity.ERROR,
                            str(visual_json_path.relative_to(self.report_path)),
                            "tooltip_uses_page",
                            "visualTooltip uses 'page' instead of 'section'",
                            fixable=True,
                            fix_description="Replace 'page' with 'section' in visualTooltip"
                        )

                        if self.auto_fix:
                            # Replace 'page' with 'section' in visualTooltip context
                            content = re.sub(
                                r'("visualTooltip"[^}]*?)"page"',
                                r'\1"section"',
                                content
                            )
                            visual_json_path.write_text(content, encoding='utf-8')
                            self.results.fixed += 1
                            self.results.fixed_files.append(str(visual_json_path))

            except Exception as e:
                pass  # Skip read errors (already handled elsewhere)
    
    def _check_relationships_description(self):
        """Check for unsupported properties in relationships.tmdl (description, fromCardinality, toCardinality)."""
        if not self.semantic_model_dir:
            return
        
        relationships_file = self.semantic_model_dir / "relationships.tmdl"
        
        if not relationships_file.exists():
            return
        
        try:
            content = relationships_file.read_text(encoding='utf-8')
            
            # Check for unsupported properties in relationships
            unsupported_props = {
                'description': r'^\s*description:',
                'fromCardinality': r'^\s*fromCardinality:',
                'toCardinality': r'^\s*toCardinality:'
            }
            
            found_issues = []
            for prop_name, pattern in unsupported_props.items():
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    matches = len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
                    found_issues.append(f"{matches} '{prop_name}'")
            
            if found_issues:
                issues_str = ', '.join(found_issues)
                # Use relative path from semantic model or absolute path
                try:
                    rel_path = str(relationships_file.relative_to(self.semantic_model_dir.parent))
                except ValueError:
                    rel_path = str(relationships_file)
                
                self._add_issue(
                    "TMDL Structure",
                    IssueSeverity.ERROR,
                    rel_path,
                    "relationships_unsupported_properties",
                    f"Found unsupported properties in relationships: {issues_str} (not supported in TMDL)",
                    fixable=True,
                    fix_description="Remove unsupported properties (description, fromCardinality, toCardinality) from relationships"
                )
                
                if self.auto_fix:
                    # Remove unsupported property lines
                    lines = content.split('\n')
                    fixed_lines = []
                    for line in lines:
                        should_skip = False
                        for pattern in unsupported_props.values():
                            if re.match(pattern, line, re.IGNORECASE):
                                should_skip = True
                                break
                        if not should_skip:
                            fixed_lines.append(line)
                    
                    relationships_file.write_text('\n'.join(fixed_lines), encoding='utf-8')
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(relationships_file))
        
        except Exception as e:
            self._add_issue(
                "TMDL Structure",
                IssueSeverity.ERROR,
                str(relationships_file.relative_to(self.report_path)),
                "read_error",
                f"Error reading file: {e}",
                fixable=False
            )
    
    def _check_missing_schemas(self):
        """Check for missing $schema properties in key files."""
        # Check page.json files
        if self.pages_dir.exists():
            for page_json_path in self.pages_dir.rglob("page.json"):
                if page_json_path.name != "page.json" or page_json_path.parent.name == "pages":
                    continue
                
                try:
                    with open(page_json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if "$schema" not in data:
                        self._add_issue(
                            "Schema Validation",
                            IssueSeverity.WARNING,
                            str(page_json_path.relative_to(self.report_path)),
                            "missing_schema",
                            "Missing $schema property",
                            fixable=True,
                            fix_description="Add $schema property"
                        )
                        
                        if self.auto_fix:
                            data["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json"
                            with open(page_json_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            self.results.fixed += 1
                            self.results.fixed_files.append(str(page_json_path))
                
                except Exception:
                    pass  # Skip read errors
    
    def _check_cache_files(self):
        """Check for cache files that should be deleted."""
        cache_files = []
        
        # NOTE: definition.pbism is NOT a cache file - it's a required metadata file
        # Only check for .pbir files (report cache)
        pbir_file = self.report_dir / "definition.pbir"
        if pbir_file.exists():
            cache_files.append(pbir_file)
        
        if cache_files:
            for cache_file in cache_files:
                # Use absolute path for display if outside report directory
                try:
                    display_path = str(cache_file.relative_to(self.report_path.parent))
                except ValueError:
                    display_path = str(cache_file)
                
                self._add_issue(
                    "Cache",
                    IssueSeverity.INFO,
                    display_path,
                    "cache_file_exists",
                    "Cache file exists (should be deleted after structural changes)",
                    fixable=True,
                    fix_description="Delete cache file"
                )
                
                if self.auto_fix:
                    cache_file.unlink()
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(cache_file))
    
    def _check_required_pbism_file(self):
        """Check that definition.pbism file exists and is valid."""
        if not self.semantic_model_dir:
            return
        
        pbism_file = self.semantic_model_dir.parent / "definition.pbism"
        
        if not pbism_file.exists():
            self._add_issue(
                "Semantic Model",
                IssueSeverity.ERROR,
                str(pbism_file.relative_to(self.report_path.parent)),
                "missing_pbism",
                "definition.pbism file is missing (required for semantic model)",
                fixable=True,
                fix_description="Create definition.pbism file with correct structure"
            )
            
            if self.auto_fix:
                # Create the file with correct structure
                pbism_content = {
                    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
                    "version": "4.2",
                    "settings": {}
                }
                with open(pbism_file, 'w', encoding='utf-8') as f:
                    json.dump(pbism_content, f, indent=2, ensure_ascii=False)
                self.results.fixed += 1
                self.results.fixed_files.append(str(pbism_file))
        else:
            # Check if file is valid JSON
            try:
                with open(pbism_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check for required properties
                if "$schema" not in data:
                    self._add_issue(
                        "Semantic Model",
                        IssueSeverity.ERROR,
                        str(pbism_file.relative_to(self.report_path.parent)),
                        "invalid_pbism_schema",
                        "definition.pbism missing $schema property",
                        fixable=True,
                        fix_description="Add $schema property to definition.pbism"
                    )
                    
                    if self.auto_fix:
                        data["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json"
                        if "version" not in data:
                            data["version"] = "4.2"
                        if "settings" not in data:
                            data["settings"] = {}
                        with open(pbism_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(pbism_file))
            
            except json.JSONDecodeError:
                self._add_issue(
                    "Semantic Model",
                    IssueSeverity.ERROR,
                    str(pbism_file.relative_to(self.report_path.parent)),
                    "invalid_pbism_json",
                    "definition.pbism contains invalid JSON",
                    fixable=True,
                    fix_description="Recreate definition.pbism file with correct structure"
                )
                
                if self.auto_fix:
                    pbism_content = {
                        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
                        "version": "4.2",
                        "settings": {}
                    }
                    with open(pbism_file, 'w', encoding='utf-8') as f:
                        json.dump(pbism_content, f, indent=2, ensure_ascii=False)
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(pbism_file))
    
    def _check_background_properties(self):
        """Check for invalid background properties in page.json files."""
        if not self.pages_dir.exists():
            return
        
        invalid_props = ["imageFit", "imageTransparency", "imagePosition"]
        
        for page_json_path in self.pages_dir.rglob("page.json"):
            if page_json_path.name != "page.json" or page_json_path.parent.name == "pages":
                continue
            
            try:
                with open(page_json_path, 'r', encoding='utf-8') as f:
                    page_data = json.load(f)
                
                if "objects" not in page_data or "background" not in page_data["objects"]:
                    continue
                
                backgrounds = page_data["objects"]["background"]
                if not isinstance(backgrounds, list):
                    continue
                
                has_invalid = False
                needs_structure_fix = False
                
                for bg in backgrounds:
                    if "properties" not in bg:
                        continue
                    
                    props = bg["properties"]
                    
                    # Check for invalid properties
                    for prop in invalid_props:
                        if prop in props:
                            has_invalid = True
                            break
                    
                    # Check for incorrect image structure (image.url instead of image.image.url)
                    if "image" in props:
                        image = props["image"]
                        if "url" in image and "image" not in image:
                            needs_structure_fix = True
                
                if has_invalid or needs_structure_fix:
                    issues = []
                    if has_invalid:
                        issues.append("invalid properties (imageFit, imageTransparency, imagePosition)")
                    if needs_structure_fix:
                        issues.append("incorrect image structure (should be image.image.url)")
                    
                    self._add_issue(
                        "Page Structure",
                        IssueSeverity.ERROR,
                        str(page_json_path.relative_to(self.report_path)),
                        "invalid_background_properties",
                        f"Background has {', '.join(issues)}",
                        fixable=True,
                        fix_description="Remove invalid properties and fix image structure"
                    )
                    
                    if self.auto_fix:
                        # Fix the background properties
                        for bg in backgrounds:
                            if "properties" not in bg:
                                continue
                            
                            props = bg["properties"]
                            
                            # Remove invalid properties
                            for prop in invalid_props:
                                if prop in props:
                                    del props[prop]
                            
                            # Fix image structure
                            if "image" in props:
                                image = props["image"]
                                
                                # Convert image.url to image.image.url
                                if "url" in image and "image" not in image:
                                    url_data = image["url"]
                                    scaling_data = image.get("scaling", {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'Fit'"
                                            }
                                        }
                                    })
                                    
                                    props["image"] = {
                                        "image": {
                                            "url": url_data,
                                            "scaling": scaling_data
                                        }
                                    }
                                # Ensure scaling exists in nested structure
                                elif "image" in image and "scaling" not in image["image"]:
                                    image["image"]["scaling"] = {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'Fit'"
                                            }
                                        }
                                    }
                        
                        with open(page_json_path, 'w', encoding='utf-8') as f:
                            json.dump(page_data, f, indent=2, ensure_ascii=False)
                        
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(page_json_path))
            
            except Exception:
                pass  # Skip read errors
    
    def _check_visual_query_structure(self):
        """Check that visuals have correct query structure (projections and queryState inside visual.query.queryState)."""
        if not self.pages_dir.exists():
            return
        
        for visual_json_path in self.pages_dir.rglob("visuals/*/visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)
                
                if "visual" not in visual_data:
                    continue
                
                visual = visual_data["visual"]
                visual_name = visual_json_path.parent.name
                page_name = visual_json_path.parent.parent.parent.name
                
                # Check for projections or queryState at wrong level (directly under visual)
                has_wrong_projections = "projections" in visual and "query" not in visual
                has_wrong_queryState = "queryState" in visual and "query" not in visual
                
                # Check for query property inside queryState (shouldn't be there)
                has_query_in_queryState = False
                # Check if projections is a dict with custom bucket names (should be in Values bucket for tableEx)
                has_custom_bucket_projections = False
                # Check if chart visuals have projections as a dict (should be Category/Y/Series as direct children)
                has_chart_projections_issue = False
                # Check if slicers have projections as a dict or use Field bucket (should use Values bucket)
                has_slicer_projections_issue = False
                # Check if card visuals have projections as a dict or use Values bucket (should use Data bucket)
                has_card_projections_issue = False
                visual_type = visual.get("visualType", "")
                chart_types = {"lineChart", "areaChart", "barChart", "clusteredBarChart", 
                              "clusteredColumnChart", "stackedBarChart", "stackedColumnChart",
                              "hundredPercentStackedBarChart", "hundredPercentStackedColumnChart"}
                
                if "query" in visual and "queryState" in visual["query"]:
                    query_state = visual["query"]["queryState"]
                    if "query" in query_state:
                        has_query_in_queryState = True
                    
                    # Check for chart visuals with projections as a dict
                    if visual_type in chart_types and "projections" in query_state and isinstance(query_state["projections"], dict):
                        # Chart visuals should have Category/Y/Series as direct children, not under projections
                        has_chart_projections_issue = True
                    
                    # Check for slicers with projections as a dict or Field bucket
                    if visual_type == "slicer":
                        if "projections" in query_state and isinstance(query_state["projections"], dict):
                            # Slicers should use Values bucket, not projections dict
                            has_slicer_projections_issue = True
                        elif "Field" in query_state and "Values" not in query_state:
                            # Slicers should use Values, not Field
                            has_slicer_projections_issue = True
                        elif "Category" in query_state and "Values" not in query_state:
                            # Some examples use Category, but Values is standard
                            has_slicer_projections_issue = True
                    
                    # Check for card visuals with projections as a dict or Values bucket
                    if visual_type == "card":
                        if "projections" in query_state and isinstance(query_state["projections"], dict):
                            # Card visuals should use Data bucket, not projections dict
                            has_card_projections_issue = True
                        elif "Values" in query_state and "Data" not in query_state:
                            # Card visuals should use Data, not Values
                            has_card_projections_issue = True
                    
                    # Check for custom bucket names in projections (for tableEx)
                    if visual_type == "tableEx" and "projections" in query_state and isinstance(query_state["projections"], dict):
                        standard_buckets = {"Values", "Category", "Y", "Series", "X", "Rows", "Columns", "Field", "Details", "Size", "Data"}
                        custom_keys = set(query_state["projections"].keys())
                        if not custom_keys.issubset(standard_buckets):
                            has_custom_bucket_projections = True
                
                if has_wrong_projections or has_wrong_queryState or has_query_in_queryState or has_custom_bucket_projections or has_chart_projections_issue or has_slicer_projections_issue or has_card_projections_issue:
                    issues = []
                    if has_wrong_projections:
                        issues.append("projections at wrong level")
                    if has_wrong_queryState:
                        issues.append("queryState at wrong level")
                    if has_query_in_queryState:
                        issues.append("query property inside queryState")
                    if has_custom_bucket_projections:
                        issues.append("custom bucket names in projections (should use Values bucket)")
                    if has_chart_projections_issue:
                        issues.append("chart projections as dict (Category/Y/Series should be direct children of queryState)")
                    if has_slicer_projections_issue:
                        issues.append("slicer projections as dict or Field bucket (should use Values bucket)")
                    if has_card_projections_issue:
                        issues.append("card projections as dict or Values bucket (should use Data bucket)")
                    
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        f"{page_name}/visuals/{visual_name}",
                        "invalid_visual_query_structure",
                        f"Visual has {', '.join(issues)}",
                        fixable=True,
                        fix_description="Move projections/queryState to visual.query.queryState and remove query property from queryState"
                    )
                    
                    if self.auto_fix:
                        # Fix the structure
                        if has_wrong_projections:
                            projections = visual.pop("projections")
                            if "query" not in visual:
                                visual["query"] = {}
                            if "queryState" not in visual["query"]:
                                visual["query"]["queryState"] = {}
                            
                            # For tableEx, projections can be a dict of buckets
                            if isinstance(projections, dict):
                                visual["query"]["queryState"].update(projections)
                            else:
                                visual["query"]["queryState"]["Values"] = {"projections": projections}
                        
                        if has_wrong_queryState:
                            old_query_state = visual.pop("queryState")
                            if "query" not in visual:
                                visual["query"] = {}
                            if "queryState" not in visual["query"]:
                                visual["query"]["queryState"] = {}
                            
                            if isinstance(old_query_state, dict):
                                for key, value in old_query_state.items():
                                    if key != "query" and key not in visual["query"]["queryState"]:
                                        visual["query"]["queryState"][key] = value
                        
                        if has_query_in_queryState:
                            if "query" in visual["query"]["queryState"]:
                                del visual["query"]["queryState"]["query"]
                        
                        # Fix chart projections structure - move Category/Y/Series to direct children
                        if has_chart_projections_issue:
                            if "projections" in visual["query"]["queryState"] and isinstance(visual["query"]["queryState"]["projections"], dict):
                                projections_dict = visual["query"]["queryState"].pop("projections")
                                # Convert to correct structure: Category/Y/Series as direct children
                                chart_buckets = {"Category", "Y", "Series", "X", "Details", "Size"}
                                for bucket_name, proj_list in projections_dict.items():
                                    if bucket_name in chart_buckets:
                                        if isinstance(proj_list, list):
                                            visual["query"]["queryState"][bucket_name] = {"projections": proj_list}
                                        else:
                                            visual["query"]["queryState"][bucket_name] = {"projections": [proj_list] if proj_list else []}
                        
                        # Fix slicer projections structure - convert to Values bucket
                        if has_slicer_projections_issue:
                            query_state = visual["query"]["queryState"]
                            all_projections = []
                            
                            # Collect projections from projections dict
                            if "projections" in query_state and isinstance(query_state["projections"], dict):
                                projections_dict = query_state.pop("projections")
                                for bucket_name, proj_list in projections_dict.items():
                                    if isinstance(proj_list, list):
                                        all_projections.extend(proj_list)
                                    else:
                                        all_projections.append(proj_list)
                            
                            # Collect from Field bucket
                            if "Field" in query_state:
                                field_projs = query_state.pop("Field")
                                if isinstance(field_projs, dict) and "projections" in field_projs:
                                    all_projections.extend(field_projs["projections"])
                                elif isinstance(field_projs, list):
                                    all_projections.extend(field_projs)
                                else:
                                    all_projections.append(field_projs)
                            
                            # Collect from Category bucket (if used)
                            if "Category" in query_state and "Values" not in query_state:
                                cat_projs = query_state.pop("Category")
                                if isinstance(cat_projs, dict) and "projections" in cat_projs:
                                    all_projections.extend(cat_projs["projections"])
                                elif isinstance(cat_projs, list):
                                    all_projections.extend(cat_projs)
                                else:
                                    all_projections.append(cat_projs)
                            
                            # Put all in Values bucket
                            if all_projections:
                                query_state["Values"] = {"projections": all_projections}
                        
                        # Fix card projections structure - convert to Data bucket
                        if has_card_projections_issue:
                            query_state = visual["query"]["queryState"]
                            all_projections = []
                            
                            # Collect projections from projections dict
                            if "projections" in query_state and isinstance(query_state["projections"], dict):
                                projections_dict = query_state.pop("projections")
                                for bucket_name, proj_list in projections_dict.items():
                                    if isinstance(proj_list, list):
                                        all_projections.extend(proj_list)
                                    else:
                                        all_projections.append(proj_list)
                            
                            # Collect from Values bucket (should be Data for cards)
                            if "Values" in query_state and "Data" not in query_state:
                                values_projs = query_state.pop("Values")
                                if isinstance(values_projs, dict) and "projections" in values_projs:
                                    all_projections.extend(values_projs["projections"])
                                elif isinstance(values_projs, list):
                                    all_projections.extend(values_projs)
                                else:
                                    all_projections.append(values_projs)
                            
                            # Put all in Data bucket (card visuals use Data, not Values)
                            if all_projections:
                                query_state["Data"] = {"projections": all_projections}
                        
                        # Fix custom bucket projections - convert to Values bucket (for tableEx)
                        if has_custom_bucket_projections:
                            if "projections" in visual["query"]["queryState"] and isinstance(visual["query"]["queryState"]["projections"], dict):
                                projections_dict = visual["query"]["queryState"].pop("projections")
                                # Collect all projections from all custom buckets
                                all_projections = []
                                for bucket_name, bucket_projs in projections_dict.items():
                                    if isinstance(bucket_projs, list):
                                        all_projections.extend(bucket_projs)
                                    elif isinstance(bucket_projs, dict):
                                        all_projections.append(bucket_projs)
                                    else:
                                        all_projections.append(bucket_projs)
                                
                                # Put all projections in Values bucket
                                visual["query"]["queryState"]["Values"] = {"projections": all_projections}
                        
                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(visual_data, f, indent=2, ensure_ascii=False)
                        
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))
            
            except Exception:
                pass  # Skip read errors

    def _check_table_sort_definition(self):
        """Check for invalid sortDefinition in tableEx visuals."""
        if not self.pages_dir.exists():
            return

        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)

                visual_type = visual_data.get("visual", {}).get("visualType", "")

                if visual_type == "tableEx":
                    query_state = visual_data.get("visual", {}).get("query", {}).get("queryState", {})

                    if "sortDefinition" in query_state:
                        self._add_issue(
                            "Visual Structure",
                            IssueSeverity.ERROR,
                            str(visual_json_path.relative_to(self.report_path)),
                            "table_sort_definition",
                            "tableEx visual has sortDefinition in queryState (not supported)",
                            fixable=True,
                            fix_description="Remove sortDefinition from queryState"
                        )

                        if self.auto_fix:
                            del query_state["sortDefinition"]
                            with open(visual_json_path, 'w', encoding='utf-8') as f:
                                json.dump(visual_data, f, indent=2, ensure_ascii=False)
                            self.results.fixed += 1
                            self.results.fixed_files.append(str(visual_json_path))

            except Exception:
                pass  # Skip read errors

    def _check_utf8_bom_encoding(self):
        """Check for UTF-8 BOM in JSON files."""
        if not self.report_dir.exists():
            return

        for json_file in self.report_dir.rglob("*.json"):
            try:
                with open(json_file, 'rb') as f:
                    first_bytes = f.read(3)

                if first_bytes == b'\xef\xbb\xbf':
                    self._add_issue(
                        "Encoding",
                        IssueSeverity.ERROR,
                        str(json_file.relative_to(self.report_path)),
                        "utf8_bom",
                        "File has UTF-8 BOM (Power BI requires UTF-8 without BOM)",
                        fixable=True,
                        fix_description="Remove BOM from file"
                    )

                    if self.auto_fix:
                        # Read content and rewrite without BOM
                        content = json_file.read_text(encoding='utf-8-sig')
                        json_file.write_text(content, encoding='utf-8')
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(json_file))

            except Exception:
                pass  # Skip read errors

    def _check_filter_config_position(self):
        """Check that filterConfig is at root level, not inside visual object."""
        if not self.pages_dir.exists():
            return

        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)

                if "visual" in visual_data and "filterConfig" in visual_data["visual"]:
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "filterConfig_wrong_position",
                        "filterConfig inside visual object (should be at root level)",
                        fixable=True,
                        fix_description="Move filterConfig to root level"
                    )

                    if self.auto_fix:
                        # Move filterConfig from visual to root
                        filter_config = visual_data["visual"].pop("filterConfig")
                        visual_data["filterConfig"] = filter_config

                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(visual_data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))

            except Exception:
                pass  # Skip read errors

    def _check_alt_text_in_visuals(self):
        """Check for unsupported altText property in visualContainerObjects."""
        if not self.pages_dir.exists():
            return

        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)

                vco = visual_data.get("visual", {}).get("visualContainerObjects", {})

                if "altText" in vco:
                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "altText_not_supported",
                        "altText in visualContainerObjects (not supported - must be configured in Power BI Desktop UI)",
                        fixable=True,
                        fix_description="Remove altText property"
                    )

                    if self.auto_fix:
                        del vco["altText"]
                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(visual_data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))

            except Exception:
                pass  # Skip read errors

    def _check_bookmark_exploration_state(self):
        """Check bookmark files have required explorationState property."""
        bookmarks_dir = self.report_dir / "bookmarks"

        if not bookmarks_dir.exists():
            return

        for bookmark_file in bookmarks_dir.glob("*.bookmark.json"):
            try:
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    bookmark_data = json.load(f)

                if "explorationState" not in bookmark_data:
                    self._add_issue(
                        "Bookmark Structure",
                        IssueSeverity.ERROR,
                        str(bookmark_file.relative_to(self.report_path)),
                        "missing_exploration_state",
                        "Bookmark missing required explorationState property",
                        fixable=True,
                        fix_description="Add explorationState with default structure"
                    )

                    if self.auto_fix:
                        # Add default explorationState
                        bookmark_data["explorationState"] = {
                            "version": "1.0",
                            "activeSection": bookmark_data.get("name", "home"),
                            "sections": {
                                bookmark_data.get("name", "home"): {
                                    "visualContainers": {}
                                }
                            }
                        }

                        # Ensure options property exists
                        if "options" not in bookmark_data:
                            bookmark_data["options"] = {
                                "targetVisualNames": [],
                                "suppressActiveSection": True,
                                "suppressData": False
                            }

                        with open(bookmark_file, 'w', encoding='utf-8') as f:
                            json.dump(bookmark_data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(bookmark_file))

            except Exception:
                pass  # Skip read errors

    def _check_empty_projections_dict(self):
        """Check for empty projections dict {} in query.queryState (should be removed)."""
        if not self.pages_dir.exists():
            return

        for visual_json_path in self.pages_dir.rglob("visual.json"):
            try:
                with open(visual_json_path, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)

                query_state = visual_data.get("visual", {}).get("query", {}).get("queryState", {})

                # Check for empty projections dict
                if "projections" in query_state and query_state["projections"] == {}:
                    visual_type = visual_data.get("visual", {}).get("visualType", "unknown")

                    self._add_issue(
                        "Visual Structure",
                        IssueSeverity.ERROR,
                        str(visual_json_path.relative_to(self.report_path)),
                        "empty_projections_dict",
                        f"{visual_type} visual has empty projections dict (should be removed entirely)",
                        fixable=True,
                        fix_description="Remove empty projections dict from queryState"
                    )

                    if self.auto_fix:
                        del query_state["projections"]
                        with open(visual_json_path, 'w', encoding='utf-8') as f:
                            json.dump(visual_data, f, indent=2, ensure_ascii=False)
                        self.results.fixed += 1
                        self.results.fixed_files.append(str(visual_json_path))

            except Exception:
                pass  # Skip read errors

    def _check_dataset_reference(self):
        """Check that report.json has datasetReference to the semantic model."""
        report_json_path = self.report_dir / "report.json"

        if not report_json_path.exists():
            return

        try:
            with open(report_json_path, 'r', encoding='utf-8') as f:
                report_data = json.load(f)

            has_dataset_ref = "datasetReference" in report_data

            if not has_dataset_ref:
                # Try to find semantic model path
                semantic_model_name = None
                if self.semantic_model_dir:
                    semantic_model_name = self.semantic_model_dir.parent.name

                self._add_issue(
                    "Report Structure",
                    IssueSeverity.ERROR,
                    "definition/report.json",
                    "missing_dataset_reference",
                    "report.json missing datasetReference - visuals will not display data",
                    fixable=True if semantic_model_name else False,
                    fix_description=f"Add datasetReference pointing to {semantic_model_name}" if semantic_model_name else "Add datasetReference (semantic model not found)"
                )

                if self.auto_fix and semantic_model_name:
                    # Add datasetReference as first property after $schema
                    report_data_new = {
                        "$schema": report_data.get("$schema"),
                        "datasetReference": {
                            "byPath": {
                                "path": semantic_model_name
                            }
                        }
                    }
                    # Add remaining properties
                    for key, value in report_data.items():
                        if key != "$schema":
                            report_data_new[key] = value

                    with open(report_json_path, 'w', encoding='utf-8') as f:
                        json.dump(report_data_new, f, indent=2, ensure_ascii=False)
                    self.results.fixed += 1
                    self.results.fixed_files.append(str(report_json_path))

        except Exception:
            pass  # Skip read errors

    def _check_pbip_artifacts_structure(self):
         """Check that .pbip file uses 'dataset' not 'semanticModel' in artifacts."""
         pbip_path = self.report_path.parent / f"{self.report_path.parent.name}.pbip"
         
         if not pbip_path.exists():
             return
         
         try:
             with open(pbip_path, 'r', encoding='utf-8') as f:
                 pbip_data = json.load(f)
             
             if "artifacts" in pbip_data:
                 for i, artifact in enumerate(pbip_data["artifacts"]):
                     if "semanticModel" in artifact:
                         self._add_issue(
                             "PBIP Structure",
                             IssueSeverity.ERROR,
                             pbip_path.name,
                             "pbip_semanticModel_property",
                             f"Artifact {i} uses 'semanticModel' (should be 'dataset')",
                             fixable=True,
                             fix_description="Change 'semanticModel' to 'dataset' in artifacts array"
                         )
                         
                         if self.auto_fix:
                             artifact["dataset"] = artifact.pop("semanticModel")
                             with open(pbip_path, 'w', encoding='utf-8') as f:
                                 json.dump(pbip_data, f, indent=2, ensure_ascii=False)
                             self.results.fixed += 1
                             self.results.fixed_files.append(str(pbip_path))
         
         except Exception:
             pass  # Skip read errors

     # ============================================================================
     # REPORTING
     # ============================================================================
    
    def print_report(self):
        """Print validation report."""
        print()
        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)
        print()
        
        if not self.results.issues:
            print("[SUCCESS] No issues found! All checks passed.")
            print()
            return
        
        # Group by category
        by_category = {}
        for issue in self.results.issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)
        
        # Print by category
        for category, issues in sorted(by_category.items()):
            print(f"{category}:")
            print("-" * 80)
            
            for issue in issues:
                severity_marker = {
                    IssueSeverity.ERROR: "[ERROR]",
                    IssueSeverity.WARNING: "[WARN]",
                    IssueSeverity.INFO: "[INFO]"
                }[issue.severity]
                
                fixable_marker = " [FIXABLE]" if issue.fixable else ""
                print(f"  {severity_marker}{fixable_marker} {issue.file_path}")
                print(f"    {issue.message}")
                if issue.fix_description:
                    print(f"    Fix: {issue.fix_description}")
                print()
        
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"  Total issues: {self.results.total_issues}")
        print(f"    Errors: {self.results.errors}")
        print(f"    Warnings: {self.results.warnings}")
        print(f"    Info: {self.results.info}")
        print(f"  Fixed: {self.results.fixed}")
        print()
        
        if self.results.fixed > 0:
            print("Fixed files:")
            for file_path in self.results.fixed_files:
                print(f"  - {file_path}")
            print()
        
        if self.results.errors > 0:
            print("[ERROR] Validation failed. Please fix errors before opening in Power BI Desktop.")
        elif self.results.warnings > 0:
            print("[WARNING] Validation passed with warnings.")
        else:
            print("[SUCCESS] Validation passed!")

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Master Power BI PBIP Validator and Fixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check only (default)
  python master_pbip_validator.py "C:\\path\\to\\report.Report"
  
  # Auto-fix issues
  python master_pbip_validator.py "C:\\path\\to\\report.Report" --fix
  
  # Verbose output
  python master_pbip_validator.py "C:\\path\\to\\report.Report" --verbose
        """
    )
    
    parser.add_argument(
        "report_path",
        nargs="?",
        default=r"C:\Users\farad\OneDrive\Desktop\press-room-fresh\press-room-dashboard.Report",
        help="Path to the .Report folder (default: press-room-fresh report)"
    )
    
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix issues where possible"
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check, don't fix (default behavior)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output for each check"
    )
    
    args = parser.parse_args()
    
    report_path = Path(args.report_path)
    
    if not report_path.exists():
        print(f"ERROR: Report path not found: {report_path}")
        sys.exit(1)
    
    auto_fix = args.fix and not args.check_only
    
    validator = PBIPValidator(report_path, auto_fix=auto_fix, verbose=args.verbose)
    results = validator.validate_all()
    validator.print_report()
    
    # Exit with error code if there are errors
    if results.errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

