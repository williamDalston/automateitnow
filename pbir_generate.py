#!/usr/bin/env python3
"""
PBIR Generator (Template-Patching, No Schema Guessing)

How it works:
- You export a "base" PBIR (PBIP) folder from Power BI Desktop: pbir_base/
- Inside that base, you keep template visuals (one per type) whose visual.json contains placeholder tokens:
    __TITLE__, __X_AXIS__, __LEGEND__, __Y_AXIS__, __TOOLTIP_0__, ...
- This script copies pbir_base -> out_dir, then copies/creates visual folders and replaces placeholders.

Why this is production-safe:
- We never manufacture unknown PBIR structures.
- We only patch strings inside known-good, exported PBIR specimens.

Usage:
  python pbir_generate.py --config dashboard_config.json --base pbir_base --out pbir_out

Optional model validation (recommended):
  python pbir_generate.py --config dashboard_config.json --base pbir_base --out pbir_out --model ./model

Where --model can be:
- A directory containing .tmdl files, or
- A model.bim file

Notes:
- Field refs in config: Table[Column] or Metrics[Measure]
- PBIR queryRef commonly uses Table.Column / Table.Measure (dot form)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# -----------------------------
# Helpers: FieldRef + queryRef
# -----------------------------

FIELDREF_RE = re.compile(r"^(?P<table>[A-Za-z0-9_]+)\[(?P<field>.+)\]$")

def parse_fieldref(s: str) -> Tuple[str, str]:
    """
    Parse Table[Column] or Metrics[Measure Name]
    Returns (table, field)
    """
    m = FIELDREF_RE.match(s.strip())
    if not m:
        raise ValueError(f"Invalid field ref: {s!r}. Expected Table[Column] or Metrics[Measure].")
    return m.group("table"), m.group("field")

def to_queryref(fieldref: str) -> str:
    """
    Convert Table[Field] -> Table.Field for PBIR queryRef usage.
    """
    table, field = parse_fieldref(fieldref)
    return f"{table}.{field}"


# -----------------------------
# Optional model validation
# -----------------------------

def collect_model_fields(model_path: Path) -> Dict[str, Set[str]]:
    """
    Best-effort model introspection.
    Returns { table_name: {field_names...} } aggregated across:
      - model.bim (JSON)
      - .tmdl files (loose regex)
    """
    fields: Dict[str, Set[str]] = {}

    if model_path.is_file() and model_path.name.lower().endswith(".bim"):
        data = json.loads(model_path.read_text(encoding="utf-8"))
        for t in data.get("model", {}).get("tables", []):
            tname = t.get("name")
            if not tname:
                continue
            fields.setdefault(tname, set())
            for c in t.get("columns", []):
                cname = c.get("name")
                if cname:
                    fields[tname].add(cname)
            for m in t.get("measures", []):
                mname = m.get("name")
                if mname:
                    fields[tname].add(mname)
        return fields

    if model_path.is_dir():
        # TMDL is commonly split across many .tmdl files
        # We'll do a conservative regex scrape: table/column/measure declarations.
        table_re = re.compile(r"^\s*table\s+(?P<name>.+?)\s*$", re.IGNORECASE)
        col_re   = re.compile(r"^\s*column\s+(?P<name>.+?)\s*$", re.IGNORECASE)
        meas_re  = re.compile(r"^\s*measure\s+(?P<name>.+?)\s*=\s*", re.IGNORECASE)

        current_table: Optional[str] = None
        for fp in model_path.rglob("*.tmdl"):
            for line in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
                mt = table_re.match(line)
                if mt:
                    current_table = mt.group("name").strip().strip('"')
                    fields.setdefault(current_table, set())
                    continue

                if current_table:
                    mc = col_re.match(line)
                    if mc:
                        fields[current_table].add(mc.group("name").strip().strip('"'))
                        continue
                    mm = meas_re.match(line)
                    if mm:
                        fields[current_table].add(mm.group("name").strip().strip('"'))
                        continue
        return fields

    raise ValueError(f"--model must be a directory of .tmdl files or a model.bim file. Got: {model_path}")


# -----------------------------
# Placeholder patching
# -----------------------------

PLACEHOLDER_RE = re.compile(r"__([A-Z0-9_]+)__")

def replace_placeholders_in_text(text: str, mapping: Dict[str, str]) -> str:
    """
    Replace placeholders like __X_AXIS__ with mapping["X_AXIS"].
    We keep placeholders if missing (so validation can catch).
    """
    def repl(m: re.Match) -> str:
        key = m.group(1)
        return mapping.get(key, m.group(0))
    return PLACEHOLDER_RE.sub(repl, text)


def patch_json_file(src: Path, dst: Path, mapping: Dict[str, str]) -> None:
    """
    Read JSON as text, replace placeholders, then validate JSON parses.
    """
    raw = src.read_text(encoding="utf-8")
    patched = replace_placeholders_in_text(raw, mapping)

    # Validate JSON (hard fail early)
    try:
        json.loads(patched)
    except json.JSONDecodeError as e:
        raise ValueError(f"Patched JSON is invalid for {dst}.\nOriginal: {src}\nError: {e}") from e

    dst.write_text(patched, encoding="utf-8")


# -----------------------------
# Config structures
# -----------------------------

@dataclass
class VisualSpec:
    id: str
    type: str
    title: str
    recipe: Optional[str] = None
    # Optional for table-style visuals
    columns: Optional[List[Dict[str, Any]]] = None
    filter: Optional[str] = None


def load_config(config_path: Path) -> Dict[str, Any]:
    return json.loads(config_path.read_text(encoding="utf-8"))


# -----------------------------
# Generator core
# -----------------------------

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def copy_base(base_dir: Path, out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(base_dir, out_dir)


def find_template_visual(base_dir: Path, visual_type: str) -> Path:
    """
    Convention: store templates at:
      pbir_base/_templates/visuals/<visualType>/visual.json
    """
    fp = base_dir / "_templates" / "visuals" / visual_type / "visual.json"
    if not fp.exists():
        raise FileNotFoundError(
            f"Missing template for visualType={visual_type!r}. Expected: {fp}\n"
            f"Create it by exporting PBIR, copying a known-good visual.json, and inserting placeholders."
        )
    return fp


def build_placeholder_map_for_visual(v: Dict[str, Any]) -> Dict[str, str]:
    """
    Create placeholder key->value mapping from config.
    Expected binding fields in config follow your recipes.
    For template placeholders:
      __TITLE__ -> visual title
      __X_AXIS__ / __LEGEND__ / __Y_AXIS__
      __TOOLTIP_0__..N
      __TABLE_COL_0__..N
      __SORT_BY__ (if you place it in templates)
      __FILTER_FIELD__ / __FILTER_VALUE__ (optional)
    """
    mapping: Dict[str, str] = {}
    mapping["TITLE"] = v.get("title", "")

    # Recipe-driven bindings block (if you include it)
    bindings = v.get("bindings", {})
    if "xAxis" in bindings:
        mapping["X_AXIS"] = to_queryref(bindings["xAxis"])
    if "legend" in bindings:
        mapping["LEGEND"] = to_queryref(bindings["legend"])
    if "yAxis" in bindings:
        mapping["Y_AXIS"] = to_queryref(bindings["yAxis"])
    if "values" in bindings:
        mapping["VALUES"] = to_queryref(bindings["values"])
    if "data" in bindings:
        mapping["DATA"] = to_queryref(bindings["data"])

    tooltips = bindings.get("tooltips", [])
    for i, t in enumerate(tooltips):
        mapping[f"TOOLTIP_{i}"] = to_queryref(t)

    # Table columns (your v2.4 top releases table includes columns in config)
    cols = v.get("columns", [])
    for i, c in enumerate(cols):
        # Allow raw fields like "Page_Title" for dimension fallback logic.
        # If the config passes a full field ref, convert it; otherwise treat as already-dot or tokenized.
        field = c.get("field", "")
        if "[" in field and "]" in field:
            mapping[f"TABLE_COL_{i}"] = to_queryref(field)
        else:
            # If you put placeholders like "Page_Title" in template, you can map it yourself.
            mapping[f"TABLE_COL_{i}"] = field

    # Optional: visual-level filter tokenization if you template it
    # Example filter: "Metrics[Is Top 10 Release] = 1"
    flt = v.get("filter")
    if isinstance(flt, str):
        # crude parse; recommended is structured format, but this will work for your locked case
        m = re.match(r'^(?P<lhs>.+?)\s*=\s*(?P<rhs>\d+|".*?")\s*$', flt.strip())
        if m:
            lhs = m.group("lhs").strip()
            rhs = m.group("rhs").strip().strip('"')
            if "[" in lhs and "]" in lhs:
                mapping["FILTER_FIELD"] = to_queryref(lhs)
            else:
                mapping["FILTER_FIELD"] = lhs
            mapping["FILTER_VALUE"] = rhs

    return mapping


def validate_fieldrefs_in_config(cfg: Dict[str, Any], model_fields: Optional[Dict[str, Set[str]]]) -> List[str]:
    """
    Validates that Table[Field] references exist in the provided model inventory.
    If no model_fields provided, only validates syntax.
    """
    errors: List[str] = []

    def check_ref(ref: str, where: str) -> None:
        try:
            t, f = parse_fieldref(ref)
        except Exception as e:
            errors.append(f"{where}: invalid field ref {ref!r} ({e})")
            return

        if model_fields is None:
            return

        if t not in model_fields:
            errors.append(f"{where}: table {t!r} not found in model for ref {ref!r}")
            return
        if f not in model_fields[t]:
            errors.append(f"{where}: field {t}[{f}] not found in model")

    # Scan kpis and visuals for measure/field refs
    for p in cfg.get("pages", []):
        pid = p.get("id", "?")
        for k in p.get("kpis", []):
            mref = k.get("measure")
            if mref:
                check_ref(mref, f"page={pid} kpi={k.get('label','?')}")

        for v in p.get("visuals", []):
            vid = v.get("id", "?")
            # bindings
            bindings = v.get("bindings", {})
            for key, val in bindings.items():
                if isinstance(val, str):
                    check_ref(val, f"page={pid} visual={vid} binding={key}")
                elif isinstance(val, list):
                    for i, x in enumerate(val):
                        if isinstance(x, str):
                            check_ref(x, f"page={pid} visual={vid} binding={key}[{i}]")
            # columns
            for i, c in enumerate(v.get("columns", []) or []):
                fref = c.get("field")
                if fref and "[" in fref and "]" in fref:
                    check_ref(fref, f"page={pid} visual={vid} column[{i}]")

            # drillthroughField in page configs
        dt = p.get("drillthroughField")
        if dt:
            check_ref(dt, f"page={pid} drillthroughField")

    return errors


def write_validation_report(out_dir: Path, report: Dict[str, Any]) -> None:
    (out_dir / "validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


def generate_visual(out_dir: Path, page_id: str, visual_cfg: Dict[str, Any], base_dir: Path) -> None:
    """
    Writes:
      pages/<pageId>/visuals/<visualId>/visual.json
    using the template for visualType and placeholder replacement.
    """
    visual_id = visual_cfg["id"]
    visual_type = visual_cfg["type"]

    target_dir = out_dir / "pages" / page_id / "visuals" / visual_id
    ensure_dir(target_dir)

    template_visual_json = find_template_visual(base_dir, visual_type)

    # Build placeholder mapping (title + bindings + tooltips + table columns)
    mapping = build_placeholder_map_for_visual(visual_cfg)

    # Required identity contract
    # Your exported template should already have a "name" placeholder; you patch it by replacing __VISUAL_NAME__ if you use it.
    mapping.setdefault("VISUAL_NAME", visual_id)

    patch_json_file(template_visual_json, target_dir / "visual.json", mapping)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to dashboard config JSON")
    ap.add_argument("--base", required=True, help="Path to base PBIR folder (exported PBIP/PBIR)")
    ap.add_argument("--out", required=True, help="Output folder for generated PBIR")
    ap.add_argument("--model", required=False, help="Optional: model.bim or directory of .tmdl files for validation")
    args = ap.parse_args()

    config_path = Path(args.config).resolve()
    base_dir = Path(args.base).resolve()
    out_dir = Path(args.out).resolve()
    model_path = Path(args.model).resolve() if args.model else None

    if not base_dir.exists():
        raise FileNotFoundError(f"Base dir not found: {base_dir}")
    if not (base_dir / "pages").exists():
        raise FileNotFoundError(f"Base dir does not look like a PBIR folder (missing pages/): {base_dir}")
    if not (base_dir / "_templates" / "visuals").exists():
        raise FileNotFoundError(
            f"Missing templates folder: {base_dir / '_templates' / 'visuals'}\n"
            f"Create it and place one template visual.json per visual type."
        )

    cfg = load_config(config_path)

    model_fields: Optional[Dict[str, Set[str]]] = None
    if model_path:
        model_fields = collect_model_fields(model_path)

    # Validate fieldrefs
    errors = validate_fieldrefs_in_config(cfg, model_fields)
    if errors:
        raise SystemExit("CONFIG VALIDATION FAILED:\n- " + "\n- ".join(errors))

    # Copy base -> out
    copy_base(base_dir, out_dir)

    # Generate visuals per page
    for p in cfg.get("pages", []):
        page_id = p.get("id")
        if not page_id:
            continue
        for v in p.get("visuals", []):
            generate_visual(out_dir, page_id, v, base_dir)

    report = {
        "status": "ok",
        "generatedPages": [p.get("id") for p in cfg.get("pages", []) if p.get("id")],
        "notes": [
            "Generation is template-based. Ensure your templates contain placeholders matching your config bindings.",
            "If Power BI ignores a sortDefinition, confirm the sort field exists in projections (your locked guardrail)."
        ]
    }
    write_validation_report(out_dir, report)
    print(f"✅ Generated PBIR into: {out_dir}")
    print(f"🧾 Validation report: {out_dir / 'validation_report.json'}")


if __name__ == "__main__":
    main()
