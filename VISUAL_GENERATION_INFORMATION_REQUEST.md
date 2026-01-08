# 📋 VISUAL GENERATION INFORMATION REQUEST

**Purpose:** Collect all information needed to perfect the visual generation system  
**Status:** Information Gathering  
**Version:** 2.2 (All Redlines Fixed + Missing Sections Added)

**Key Improvements (v2.0):**
- 🚨 PBIP Dataset Artifact elevated to BLOCKER status
- 📄 Page Definition Integration section added
- 🗺️ Field Alias Map section added
- 📅 Date Key Normalization check added
- 🎯 Enhanced Golden Samples (complete packages)
- ❌ Forbidden Rules section added
- 🚫 No Guessing Policy added
- ✅ Top 10 Fixed Set Validation added
- 📊 Projection Role Buckets (not just order)
- 🔍 QueryRef confirmation for measures with spaces

**Additional Improvements (v2.1):**
- 🔧 Fixed Dim_Date naming contradictions (Year_Month + numeric sort key as actual)
- 📋 PBIP schema lock (require actual file content, don't assume structure)
- 🔗 Visual mounting mechanism (explicit key mapping requirement)
- 📐 Coordinate system lock (confirm layout units from 1280×720 page)
- 🏷️ VisualType canonical strings requirement
- 📊 Data roles contract (role names + role IDs, not just order)
- 🔍 Visual-level filters check
- 🆔 Identity & stable IDs rules
- 🎯 Minimal golden report option
- ✅ Top 10 validation tightened (count + URL identity)
- 📝 Wording: "Expected" → "Observed in golden sample"
- 📝 Wording: ✅ → "Observed from current files" vs "Confirmed"

---

## 🎯 GOAL

To make the **"precise visual generation method"** work *perfectly* (meaning: generated PBIP opens cleanly, visuals render, no blank charts, no silent sorting bugs), we need to nail down specific environment details and patterns.

---

## 🚨 BLOCKER: PBIP Dataset Artifact (STOP THE LINE)

**CRITICAL:** If `.pbip` doesn't reference the dataset, Power BI can open a report shell with visuals that can't bind.

**Current observation:**
- ⚠️ `.pbip` file only contains `report` artifact
- Missing: `dataset` artifact

**Required fix:**
- `.pbip` MUST include both `report` and `dataset` paths correctly

**⚠️ CRITICAL: Do not assume schema structure**

**Please provide:**
- [ ] **Exact current `.pbip` file content** (before any modification)
  - Copy entire file content here: `___________________________`
- [ ] **Confirm exact key name(s) Power BI expects:**
  - [ ] `artifacts` (array)
  - [ ] `artifacts` (object)
  - [ ] Other key name: `___________________________`
- [ ] **Confirm dataset reference location:**
  - [ ] In `.pbip` file as artifact
  - [ ] In `definition.pbir` only (current observation)
  - [ ] Both locations
  - [ ] Other: `___________________________`

**Current observation from your files:**
- `.pbip` uses `artifacts` array with `report` only ✅ (Observed from current files)
- `definition.pbir` has `datasetReference` pointing to semantic model ✅ (Observed from current files)
- ⚠️ **Unknown:** Whether `.pbip` should also have `dataset` artifact (BLOCKER - needs confirmation)

**Generator rule:**
- ❌ **FORBIDDEN:** Assume or invent `.pbip` schema structure
- ✅ **REQUIRED:** Mirror the observed schema exactly from golden sample
- ✅ **REQUIRED:** Match key names, array vs object, and structure precisely

---

## 1️⃣ ENVIRONMENT LOCK BLOCK

### Power BI Desktop Version

**Please provide:**
- [ ] Power BI Desktop version (Help → About)
  - Example: `2.134.1234.0 (Build 23.0.12345.0)`
- [ ] Build number
- [ ] Release date (if visible)

**Why this matters:** PBIP/report JSON shape has minor but fatal differences across builds (property names, where sort lives, whether `prototypeQuery` is required, etc.).

---

### PBIP Format & Structure

**Please confirm:**
- [ ] **PBIP with TMDL** (current format) ✅
- [ ] **Classic `model.bim` style** (legacy format)

**Current observation from your files:**
- Using TMDL format (`.tmdl` files in `SemanticModel/definition/`)
- Semantic model version: `4.2` (from `definition.pbism`)
- Report schema: `2.4.0` (from visual.json `$schema`)

**Visual folder structure:**
- [ ] Visuals live under: `report/definition/pages/{page_id}/visuals/{visual_id}/visual.json` ✅
- [ ] Alternative structure (please describe)

**Please verify:**
- [ ] Is this the correct structure for your environment?
- [ ] Are there any additional folders or files required?

---

## 📐 COORDINATE SYSTEM LOCK (CRITICAL)

**Why this matters:** Layout units are not always literal pixels. Generator must match stored units.

**Please provide from a page configured to 1280×720 in Power BI Desktop:**
- [ ] Page stored `width` value (Observed: `___________________________`)
- [ ] Page stored `height` value (Observed: `___________________________`)
- [ ] Confirm units:
  - [ ] Pixels
  - [ ] Points
  - [ ] Power BI internal layout units
  - [ ] Unknown

**Please provide one visual position example from a golden `visual.json`:**
- [ ] `position.x`: `___________________________`
- [ ] `position.y`: `___________________________`
- [ ] `position.width`: `___________________________`
- [ ] `position.height`: `___________________________`

**Generator rule:**
- ✅ REQUIRED: Use the same stored unit system as golden samples
- ❌ FORBIDDEN: Assume 1280×720 equals stored width/height values

---

### DAX Locale Rules

**Please specify:**
- [ ] **DAX delimiter standard:**
  - [ ] **Comma** (en-US style): `SUM([Total Views])`
  - [ ] **Semicolon** (EU-style): `SUM([Total Views];)`

**Current observation:**
- Your TMDL files use comma separators
- Example: `SUM(Fact_Press_Analytics[Views])`

**Format strings:**
- [ ] Standard format: `#,0` (thousands separator)
- [ ] Standard format: `0.0%` (percentage)
- [ ] Other standard formats used?

**Please confirm:**
- [ ] DAX delimiter = **Comma** (LOCKED)
- [ ] Format strings follow US conventions

---

## 2️⃣ GOLDEN SAMPLE VISUALS (Enhanced)

**Request:** Please provide complete visual package for each visual type, created manually in Power BI Desktop and saved.

**Why this matters:** The true source of truth is what Power BI itself writes on your machine. Required/optional fields vary slightly, and "it looks optional" is how blank visuals are born. Power BI stores some defaults in page/report objects, so a single `visual.json` alone sometimes isn't enough.

### Required Visual Types

**For each visual type, provide:**

1. `visual.json` file
2. Any sibling files in that visual folder (if they exist)
3. The page definition file (`page.json`) that references it
4. Confirmation of how the visual is "mounted" on the page

---

- [ ] **1. Card (KPI)**
  - Visual folder path: `___________________________`
  - `visual.json` path: `___________________________`
  - Measure used: `___________________________`
  - Page definition file: `___________________________`
  - How visual is referenced in page: `___________________________`
  - Sibling files (if any): `___________________________`
  - Notes: `___________________________`

- [ ] **2. Line Chart**
  - Visual folder path: `___________________________`
  - `visual.json` path: `___________________________`
  - X-axis: `___________________________`
  - Y-axis: `___________________________`
  - Page definition file: `___________________________`
  - How visual is referenced in page: `___________________________`
  - Sibling files (if any): `___________________________`
  - Notes: `___________________________`

- [ ] **3. Donut Chart**
  - Visual folder path: `___________________________`
  - `visual.json` path: `___________________________`
  - Legend: `___________________________`
  - Values: `___________________________`
  - Page definition file: `___________________________`
  - How visual is referenced in page: `___________________________`
  - Sibling files (if any): `___________________________`
  - Notes: `___________________________`

- [ ] **4. 100% Stacked Column Chart**
  - Visual folder path: `___________________________`
  - `visual.json` path: `___________________________`
  - X-axis: `___________________________`
  - Legend: `___________________________`
  - Y-axis: `___________________________`
  - Page definition file: `___________________________`
  - How visual is referenced in page: `___________________________`
  - Sibling files (if any): `___________________________`
  - Notes: `___________________________`

- [ ] **5. Slicer**
  - Visual folder path: `___________________________`
  - `visual.json` path: `___________________________`
  - Column used: `___________________________`
  - Page definition file: `___________________________`
  - How visual is referenced in page: `___________________________`
  - Sibling files (if any): `___________________________`
  - Notes: `___________________________`

**Current observation:**
- Slicer sample exists: `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/70869c336db70da0c4a2/visual.json`
- Page definition exists: `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/page.json`
- ⚠️ **Need to verify:** How visuals are referenced in `page.json` (not immediately obvious from current sample)

**Alternative: Minimal Golden Report Option**

Instead of hunting samples across your real report, provide a **tiny "Golden PBIP"**:

- [ ] **Create minimal golden report:**
  - [ ] 1 page
  - [ ] 5 visuals (card, line, donut, 100% stacked, slicer)
  - [ ] Your theme applied
  - [ ] Saved PBIP folder
  - [ ] Complete folder structure exported

**Why this matters:** That single package becomes the master truth and avoids drift from real report complexity.

---

## 🏷️ VISUALTYPE CANONICAL STRINGS (REQUIRED)

**Why this matters:** `visual.visualType` strings must match exactly what Power BI writes.

**From golden samples, please provide the exact `visual.visualType` for:**
- [ ] Card (KPI): `___________________________`
- [ ] Line chart: `___________________________`
- [ ] Donut chart: `___________________________`
- [ ] 100% stacked column: `___________________________`
- [ ] Slicer: `slicer` ✅ (Observed from current files)

**Generator rule:**
- ✅ REQUIRED: Only use visualType strings observed in golden samples
- ❌ FORBIDDEN: Invent or "guess" a visualType name

---

## 3️⃣ MODEL MANIFEST CONTRACT

### Tables & Columns

**Please provide complete list:**

#### Fact_Press_Analytics
- [ ] **Columns:**
  - `Date` - Data type: `dateTime` ✅ (Observed from current files)
  - `Page_URL` - Data type: `string` ✅ (Observed from current files)
  - `Channel_Group` - Data type: `string` ✅ (Observed from current files)
  - `Views` - Data type: `int64` ✅ (Observed from current files)
  - `Users` - Data type: `int64` ✅ (Observed from current files)
  - `Page_Type` - Data type: `string` (calculated?) ✅ (Observed from current files)
  - Other columns: `___________________________`

#### Dim_Date
- [ ] **Columns:**
  - `Date` - Data type: `dateTime` ✅ (Observed from current files)
  - `Year_Month` - Data type: `string` ✅ (Observed from current files - actual model column)
  - `[numeric_sort_key]` - Data type: `int64` (for sorting Year_Month) ⚠️ (Unknown if exists - need confirmation)
  - Other columns: `___________________________`

**⚠️ IMPORTANT:** 
- Spec references `Month_Year` but model has `Year_Month` → Use alias map
- Spec references `YearMonth` but model may not have it → Need numeric sort key confirmation
- **Generator rule:** Use actual model names (`Year_Month`) and resolve spec names (`Month_Year`) via alias map

#### Metrics (Measures Table)
- [ ] **Measures:**
  - `Total Views` ✅ (Observed from current files)
  - `Total Users` ✅ (Observed from current files)
  - `Press Release Views` ✅ (Observed from current files)
  - `Landing Page Views` ✅ (Observed from current files)
  - `Top 10 PR Views` (exists?) `___________________________`
  - `Top10 Series Value` (exists?) `___________________________`
  - Other measures: `___________________________`

#### Top10_Series (Helper Table)
- [ ] **Columns:**
  - `Series` - Data type: `string` ✅ (Observed from current files - if exists)
  - `SortOrder` - Data type: `integer` ✅ (Observed from current files - if exists)
  - Exists? `___________________________`

#### Dim_Press_Releases
- [ ] **Columns:**
  - `Page_URL` - Data type: `string` ✅ (Observed from current files)
  - `Page_Title` - Data type: `string` ✅ (Observed from current files)
  - `Page_Type` - Data type: `string` ✅ (Observed from current files)
  - Other columns: `___________________________`

**Please provide:**
- [ ] Complete TMDL export OR
- [ ] `model_manifest.json` with:
  ```json
  {
    "entities": [
      {
        "name": "Fact_Press_Analytics",
        "columns": [
          {"name": "Date", "dataType": "dateTime"},
          ...
        ],
        "measures": []
      },
      ...
    ],
    "relationships": [...],
    "sortByColumn": [...]
  }
  ```

---

### Relationships Contract

**Critical for preventing blank charts:**

#### Relationship 1: Date
- [ ] **From:** `Fact_Press_Analytics[Date]` ✅
- [ ] **To:** `Dim_Date[Date]` ✅
- [ ] **Active:** `true` ✅
- [ ] **Cardinality:** `Many-to-One` ✅
- [ ] **Date type match:**
  - Fact date type: `dateTime` ✅
  - Dim date type: `dateTime` ✅
  - **Match?** `___________________________`

**Please verify:**
- [ ] Relationship is active
- [ ] Date types match (no datetime vs date mismatch)
- [ ] Relationship name: `___________________________`

#### Relationship 2: Page_URL
- [ ] **From:** `Fact_Press_Analytics[Page_URL]` ✅
- [ ] **To:** `Dim_Press_Releases[Page_URL]` ✅
- [ ] **Active:** `true` ✅
- [ ] **Cardinality:** `Many-to-One` ✅

**Please verify:**
- [ ] Relationship is active
- [ ] Column types match (both string)
- [ ] Relationship name: `___________________________`

**Other relationships:**
- [ ] List any other relationships: `___________________________`

---

### Sort-By Column Metadata (LOCK)

**Critical for correct sorting. Do not assume any sort key exists.**

#### Dim_Date[Year_Month] (Actual display column)
- [ ] **Column exists:** `Year_Month` ✅ (Observed from current files)
- [ ] **Sort-by numeric key column exists:** `[numeric_sort_key]` `___________________________`
  - Examples to check: `YearMonth`, `Year_Month_Sort`, `YearMonthKey`, `YearMonth_Num`
- [ ] **Model-level SortByColumn is set (TMDL):**
  - [ ] Yes, `Year_Month SortByColumn = [numeric_sort_key]` (Observed: `___________________________`)
  - [ ] No, needs to be set
  - [ ] Unknown

**Please provide from TMDL (exact line or snippet):**
- [ ] The `Year_Month` column definition including `sortByColumn` reference

**Generator rule:**
- ✅ REQUIRED: Use `Year_Month` as the display axis label column
- ✅ REQUIRED: If a numeric sort key exists and is used, set SortByColumn at model-level
- ❌ FORBIDDEN: Invent a sort key column name if it does not exist in the model

#### Top10_Series[Series] (If table exists)
- [ ] Table `Top10_Series` exists? `___________________________`
- [ ] Column `Series` exists? `___________________________`
- [ ] Column `SortOrder` exists? `___________________________`
- [ ] Model-level SortByColumn set: `Series SortByColumn = SortOrder` (Observed: `___________________________`)

---

## 4️⃣ QUERYREF PATTERNS (Critical for Field Binding)

**From your golden samples, please confirm:**

### QueryRef Format

**Current observation from your slicer (column):**
- `queryRef`: `"Dim_Press_Releases.Page_Type"` ✅
- `nativeQueryRef`: `"Page_Type"` ✅

**⚠️ CRITICAL: Need confirmation for measures with spaces**

**Please verify for each field type:**

#### Measures (with spaces in name)
- [ ] **From KPI card golden sample:** Exact `queryRef` for `Metrics[Total Views]`
  - Observed in golden sample: `___________________________`
  - Alternative formats to check: `"Metrics[Total Views]"` (bracket notation), `"Total Views"` (no table prefix)
- [ ] **From KPI card golden sample:** Exact `nativeQueryRef` for `Metrics[Total Views]`
  - Observed in golden sample: `___________________________`
  - Alternative formats to check: `"TotalViews"` (no space), other formats

#### Columns (with underscores)
- [ ] Format: `"Dim_Date.Year_Month"` (with underscore) ✅
- [ ] Alternative: `"Dim_Date[Year_Month]"` (bracket notation)
- [ ] Alternative: `"Year_Month"` (no table prefix)

**Please confirm (from golden samples):**
- [ ] Spaces in field names are preserved exactly in `queryRef` (Observed: `___________________________`)
- [ ] Spaces in field names are preserved exactly in `nativeQueryRef` (Observed: `___________________________`)
- [ ] Underscores in field names are preserved exactly (Observed: `___________________________`)
- [ ] Table prefix is always included in `queryRef` (Observed: `___________________________`)
- [ ] Format: `TableName.FieldName` (dot notation) ✅ (Observed from current files)
- [ ] `nativeQueryRef` = field name only (no table prefix) ✅ (Observed from current files)

### NativeQueryRef Format

**Current observation:**
- `nativeQueryRef`: `"Page_Type"` (just field name, no table) ✅

**Please confirm:**
- [ ] `nativeQueryRef` = field name only (no table prefix)
- [ ] Spaces/underscores preserved exactly
- [ ] Required or optional? `___________________________`

---

## 5️⃣ SORTING IMPLEMENTATION RULES

### Model-Level vs Visual-Level Sorting

**Current understanding:**
- **Best practice:** Set model-level `Year_Month` → Sort by numeric key
- **Visual sortDefinition:** Usually sorts by the *display column* (Year_Month), not by sort key directly

**⚠️ CRITICAL: Do not assume sortDefinition should reference YearMonth**

**Best rule for automation:**
- **Always set model SortByColumn.**
- **In visuals, sort by the display column** unless golden sample shows otherwise.
- **Learn from goldens, don't invent a doctrine.**

**Please confirm implementation:**

#### Option A: Model-Level Only
- [ ] Set model property: `Dim_Date[Year_Month] SortByColumn = Dim_Date[[numeric_sort_key]]` (or equivalent)
- [ ] Visual sortDefinition sorts by `Dim_Date[Year_Month]` (ascending)
- [ ] Power BI uses model-level sort automatically

#### Option B: Both Model + Visual
- [ ] Set model property: `Dim_Date[Year_Month] SortByColumn = Dim_Date[[numeric_sort_key]]` (or equivalent)
- [ ] Visual sortDefinition explicitly sorts by `Dim_Date[[numeric_sort_key]]` (ascending)
- [ ] Redundant but bulletproof

**Please specify:**
- [ ] Which approach works in your environment? `___________________________`
- [ ] Does visual sortDefinition reference the sort-by column or the display column? `___________________________`
- [ ] From golden samples, what does sortDefinition actually reference? `___________________________`

**Locked Rule (to be confirmed from goldens):**
1. Generator MUST set model property: `Dim_Date[Year_Month] SortByColumn = [numeric_sort_key]` (if sort key exists)
2. Visual MUST include a sortDefinition - **reference format to be confirmed from golden samples** (usually references display column `Year_Month`, not sort key directly)

**Please verify:**
- [ ] This rule is correct for your environment
- [ ] Any exceptions or variations? `___________________________`

---

## 6️⃣ PAGE DEFINITION INTEGRATION (CRITICAL)

**⚠️ CRITICAL:** Right now we're focused on `visuals/{visual_id}/visual.json`, but in PBIP a visual usually must also be referenced by the **page's container/layout file**.

**Current observation:**
- Page definition exists: `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/page.json`
- Page metadata exists: `press-room-dashboard.Report/definition/pages/pages.json`
- Visual folders exist: `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/{visual_id}/`
- ⚠️ **Unknown:** How visuals are referenced/mounted in page definition

**Please provide:**

- [ ] **What file enumerates visuals on a page?**
  - [ ] `page.json` (page definition file)
  - [ ] `pages.json` (pages metadata)
  - [ ] Other file: `___________________________`

- [ ] **Visual mounting mechanism - what key links a visual folder to the page?**
  - [ ] Visual folder name (e.g., `70869c336db70da0c4a2`)
  - [ ] `visual.json` `name` property
  - [ ] GUID stored in page definition
  - [ ] List of `visualContainers` in page.json
  - [ ] Auto-discovered (no explicit reference needed)
  - [ ] Other: `___________________________`

- [ ] **Exact field/path in page file that enumerates visuals:**
  - [ ] Path: `___________________________`
  - [ ] Example mapping:
    - "This page references visual id: `___________________________`"
    - "The folder path is: `___________________________`"
    - "The `name` inside visual.json is: `___________________________`"

- [ ] **When you add a new visual folder, what other file must be updated to "mount" it?**
  - [ ] `page.json` must be updated (specify which field)
  - [ ] `pages.json` must be updated
  - [ ] Visual folder is auto-discovered (no update needed)
  - [ ] Other: `___________________________`

- [ ] **Provide one complete page folder example:**
  - [ ] Page folder path: `___________________________`
  - [ ] Page definition file (`page.json`) complete content
  - [ ] One existing visual folder structure
  - [ ] Confirmation that adding a visual requires updating the page file (or not)

**Why this matters:** If you skip this, you can generate perfect `visual.json` files that Power BI never even loads.

**Current page.json structure (observed from current files):**
- Contains: `name`, `displayName`, `displayOption`, `height`, `width`, `pageBinding`, `objects.background`
- ⚠️ **Missing:** Visual references (need to confirm how visuals are mounted)

---

## 🆔 IDENTITY & STABLE IDs RULES (CRITICAL)

**Why this matters:** Page mounting can depend on IDs. Collisions break loads silently.

**Please provide observed formats from your current report folders:**
- [ ] Page folder ID format (length + charset): `___________________________`
- [ ] Visual folder ID format (length + charset): `___________________________`
- [ ] `visual.json.name` format: `___________________________`
- [ ] `tabOrder` uniqueness expectations:
  - [ ] Must be unique per page
  - [ ] Must be sequential
  - [ ] Other: `___________________________`

**Mounting reference check (must be explicit):**
- [ ] Page references visuals by:
  - [ ] Visual folder ID
  - [ ] `visual.json.name`
  - [ ] Another GUID inside page definition
  - [ ] Other: `___________________________`

**Generator rule:**
- ✅ REQUIRED: IDs must match golden format and be unique
- ❌ FORBIDDEN: Reuse visual IDs or visual `name` values across a page

---

## 7️⃣ REPORT-LEVEL DEPENDENCIES

**Why this matters:** Two visuals with identical `visual.json` can render differently depending on report-level settings.

**Please provide:**

### Theme Files
- [ ] Theme file(s) used (JSON theme path if present)
  - Current observation: `HHS_Theme_USWDS_Aligned` (baseTheme)
  - Current observation: `HHS_USWDS_Theme5040178124888481.json` (customTheme)
- [ ] Theme file locations: `___________________________`

### Auto Date/Time
- [ ] Is **Auto Date/Time** disabled? (important for date behavior)
  - [ ] Yes (disabled)
  - [ ] No (enabled)
  - [ ] Unknown

### Report-Level Filters
- [ ] Any report-level filters already defined?
  - [ ] Yes - provide details: `___________________________`
  - [ ] No

### Visual Interactions Defaults
- [ ] Cross-filter vs none defaults
  - [ ] Cross-filter enabled (default)
  - [ ] Cross-filter disabled (default)
  - [ ] Custom interactions: `___________________________`

### Preview Features
- [ ] Any preview features enabled?
  - [ ] Yes - list: `___________________________`
  - [ ] No
- [ ] Do any preview features change visual schema?
  - [ ] Yes - details: `___________________________`
  - [ ] No

---

## 8️⃣ FIELD ALIAS MAP (Prevent Hardcoding)

**Why this matters:** You found `Month_Year` vs `Year_Month`. This will happen again. Never hardcode spec names directly into visuals; always resolve via aliases first.

**Please provide canonical naming layer:**

```json
{
  "aliases": {
    "Dim_Date.Month_Year": "Dim_Date.Year_Month",
    "Dim_Date.YearMonth": "Dim_Date.[numeric_sort_key]",
    "Metrics.Top 10 PR Views": "Metrics.[actual_measure_name]",
    ...
  }
}
```

**Current discrepancies:**
- Spec references: `Dim_Date[Month_Year]`
- Model has: `Dim_Date[Year_Month]`
- Spec references: `Dim_Date[YearMonth]` (sort key)
- Model: Unknown if exists

**Please provide:**
- [ ] Complete alias mapping table
- [ ] All spec names → actual model names
- [ ] All measure names → actual measure names
- [ ] All column names → actual column names

**Generator rule:**
- ❌ **FORBIDDEN:** Hardcode spec names directly into visuals
- ✅ **REQUIRED:** Always resolve via aliases first

---

## 9️⃣ DATE KEY NORMALIZATION CHECK

**Why this matters:** If Fact dates include time-of-day and Dim_Date is midnight-only, joins can silently fail.

**Please confirm:**

- [ ] **Does `Fact_Press_Analytics[Date]` contain time components?**
  - [ ] Yes (includes time-of-day)
  - [ ] No (date-only, midnight)
  - [ ] Unknown

- [ ] **Does `Dim_Date[Date]` contain time components?**
  - [ ] Yes (includes time-of-day)
  - [ ] No (date-only, midnight)
  - [ ] Unknown

- [ ] **If Fact has time components, is there a normalized `Fact[DateKey]` (date-only) used for relationship?**
  - [ ] Yes - column name: `___________________________`
  - [ ] No - relationship uses `Fact[Date]` directly
  - [ ] Unknown

**Current observation:**
- Both columns are `dateTime` type ✅
- Relationship: `Fact_Press_Analytics[Date] → Dim_Date[Date]` ✅
- ⚠️ **Unknown:** Whether time components match

**Required confirmation:**
- [ ] Relationship column granularity matches (date-only vs datetime)
- [ ] If mismatch exists, how is it handled? `___________________________`

**Generator rule:**
- ✅ **REQUIRED:** Relationship column must match at the same granularity
- ❌ **FORBIDDEN:** Create relationship with mismatched granularity

---

## 🔟 VISUAL-SPECIFIC REQUIREMENTS

### Card (KPI) Visual

**From golden sample, please confirm:**
- [ ] Query state bucket: `Data` (not `Values`)
- [ ] Projection count: `1` (single measure)
- [ ] `visualContainerObjects` required: `background`, `border`, `visualHeader`
- [ ] `active: true` required: `Yes` ✅
- [ ] Other required properties: `___________________________`

### Slicer Visual

**From golden sample (observed from current files):**
- [ ] Query state bucket: `Values` (not `Data`) ✅ (Observed from current files)
- [ ] Projection count: `1` (single column) ✅ (Observed from current files)
- [ ] `visualContainerObjects` minimal (most `show: false`) ✅ (Observed from current files)
- [ ] `filterConfig` required ✅ (Observed from current files)
- [ ] `sortDefinition` present ✅ (Observed from current files)
- [ ] `active: true` required: `Yes` ✅ (Observed from current files)
- [ ] `drillFilterOtherVisuals: true` present ✅ (Observed from current files)

**Please confirm:**
- [ ] All observations correct?
- [ ] Any additional required properties? `___________________________`

### Line Chart

**Please provide from golden sample:**
- [ ] Query state bucket: `Data` ✅ (Observed from current files)
- [ ] **Data roles contract (role bucket names + role IDs):**
  - [ ] Category/X-axis role name: `___________________________`
  - [ ] Values/Y-axis role name: `___________________________`
  - [ ] Legend role name (if present): `___________________________`
  - [ ] Tooltips role name (if present): `___________________________`
  - [ ] Role keys are singular or arrays? `___________________________`
  - [ ] Fields appear under `projections` only, or also under `select`/`from`/`where`? `___________________________`
- [ ] **Projection order within each role:** `___________________________`
- [ ] `sortDefinition` required: `Yes` ✅ (Observed from current files)
- [ ] `visualContainerObjects` required: `background`, `border`, `visualHeader`, `title`
- [ ] **Visual-level filters:**
  - [ ] Does golden contain a `filters` array? `___________________________`
  - [ ] Does it contain any `filter` objects inside query state? `___________________________`
- [ ] Other required properties: `___________________________`

**⚠️ Important:** Generator must match the *role buckets and role names* exactly as written in golden samples, not rely on "index 0 means x-axis" as a universal law.

**Generator rule:**
- ✅ **REQUIRED:** If goldens include `filters`, replicate structure exactly
- ❌ **FORBIDDEN:** If goldens omit `filters`, do not add them

### 100% Stacked Column Chart

**Please provide from golden sample:**
- [ ] Query state bucket: `Data` ✅ (Observed from current files)
- [ ] **Data roles contract (role bucket names + role IDs):**
  - [ ] Category/X-axis role name: `___________________________`
  - [ ] Values/Y-axis role name: `___________________________`
  - [ ] Legend role name (if present): `___________________________`
  - [ ] Tooltips role name (if present): `___________________________`
  - [ ] Role keys are singular or arrays? `___________________________`
  - [ ] Fields appear under `projections` only, or also under `select`/`from`/`where`? `___________________________`
- [ ] **Projection order within each role:** `___________________________`
- [ ] `sortDefinition` required: `Yes` ✅ (Observed from current files)
- [ ] `visualContainerObjects` required: `background`, `border`, `visualHeader`, `title`
- [ ] **Visual-level filters:**
  - [ ] Does golden contain a `filters` array? `___________________________`
  - [ ] Does it contain any `filter` objects inside query state? `___________________________`
- [ ] Other required properties: `___________________________`

**⚠️ Important:** Generator must match the *role buckets and role names* exactly as written in golden samples.

**Generator rule:**
- ✅ **REQUIRED:** If goldens include `filters`, replicate structure exactly
- ❌ **FORBIDDEN:** If goldens omit `filters`, do not add them

### Donut Chart

**Please provide from golden sample:**
- [ ] Query state bucket: `Data` ✅ (Observed from current files)
- [ ] **Data roles contract (role bucket names + role IDs):**
  - [ ] Legend role name: `___________________________`
  - [ ] Values role name: `___________________________`
  - [ ] Tooltips role name (if present): `___________________________`
  - [ ] Role keys are singular or arrays? `___________________________`
  - [ ] Fields appear under `projections` only, or also under `select`/`from`/`where`? `___________________________`
- [ ] **Projection order within each role:** `___________________________`
- [ ] `sortDefinition` required: `No` (Power BI handles automatically) ✅ (Observed from current files)
- [ ] `visualContainerObjects` required: `background`, `border`, `visualHeader`, `title`
- [ ] **Visual-level filters:**
  - [ ] Does golden contain a `filters` array? `___________________________`
  - [ ] Does it contain any `filter` objects inside query state? `___________________________`
- [ ] Other required properties: `___________________________`

**⚠️ Important:** Generator must match the *role buckets and role names* exactly as written in golden samples.

**Generator rule:**
- ✅ **REQUIRED:** If goldens include `filters`, replicate structure exactly
- ❌ **FORBIDDEN:** If goldens omit `filters`, do not add them

---

## 1️⃣1️⃣ TOP 10 FIXED SET VALIDATION

**Why this matters:** Your Top 10 "fixed set" can still accidentally float per month even when visuals generate perfectly. This will show up as "why does Top 10 change every month?" even when visuals are correct.

**Please provide validation:**

- [ ] **Top 10 set must be constant across Year_Month points when slicer range is fixed**
- [ ] **Manual test confirmation (two assertions):**
  - [ ] **Assertion 1:** Create table visual with `Year_Month` and Top 10 URLs count
    - [ ] Top 10 URLs count should stay 10 across all months
  - [ ] **Assertion 2:** Create table visual with:
    - [ ] `Year_Month` column
    - [ ] `Page_URL` column
    - [ ] `IsTop10` flag (calculated)
    - [ ] Filter to `IsTop10 = true`
    - [ ] **Verify:** The same URLs persist across months (not just count stays 10)
  - [ ] If either assertion fails, the measure needs to explicitly remove axis filter while preserving slicer filters

**Current Top 10 DAX approach:**
- Uses `ALLSELECTED(Fact_Press_Analytics)` inside measure
- Evaluated under month axis context
- ⚠️ **Risk:** Month filter may still apply depending on context

**Please confirm:**
- [ ] Does current Top 10 DAX produce constant set across months? (Yes/No)
- [ ] Does current Top 10 DAX produce same URLs across months? (Yes/No)
- [ ] If either fails, what fix is needed? `___________________________`

**Generator rule:**
- ✅ **REQUIRED:** Top 10 set must be constant across date axis points
- ✅ **REQUIRED:** Top 10 URLs must be identical across date axis points (not just count)
- ✅ **VALIDATION:** Include test to verify both count and URL identity

---

## 1️⃣2️⃣ FORBIDDEN RULES (Prevent "Improvements")

**Why this matters:** Cursor might "improve" the model by creating dimensions that don't exist. Explicitly forbid this.

### Dim_Channel Forbidden

- ❌ **FORBIDDEN:** Do not create `Dim_Channel` table
- ❌ **FORBIDDEN:** Do not reference `Dim_Channel` anywhere
- ✅ **REQUIRED:** Use `Fact_Press_Analytics[Channel_Group]` everywhere

**Current spec consistency:**
- ✅ Channel references use `Fact_Press_Analytics[Channel_Group]` everywhere
- ✅ No `Dim_Channel` references remain

**Generator rule:**
- ❌ **FORBIDDEN:** Generate any `Dim_Channel` references
- ✅ **REQUIRED:** All channel visuals bind to `Fact_Press_Analytics[Channel_Group]`

---

## 1️⃣3️⃣ NO GUESSING POLICY

**Why this matters:** Right now Cursor could still "infer" optional fields. This single rule prevents 90% of "looks right but breaks" failures.

**Generation Rule (LOCKED):**

1. ✅ **If a property appears in the golden sample for a visual type, include it.**
2. ❌ **If it does not appear in the golden sample, do not invent it.**
3. ✅ **If Power BI requires something that isn't in goldens, update goldens first.**

**Please confirm:**
- [ ] This rule is acceptable for your environment
- [ ] Any exceptions? `___________________________`

**Generator implementation:**
- ✅ **REQUIRED:** Match golden sample structure exactly
- ❌ **FORBIDDEN:** Add properties not in golden sample
- ❌ **FORBIDDEN:** Omit properties present in golden sample

---

## 1️⃣4️⃣ GOLDEN DIFF TEST REQUIREMENTS

**To validate generated visuals match Power BI's expectations:**

### Test Checklist

For each generated visual, compare to golden sample:

- [ ] **Required keys present:**
  - [ ] `$schema`
  - [ ] `name`
  - [ ] `position` (x, y, z, width, height, tabOrder)
  - [ ] `visual.visualType`
  - [ ] `visual.query.queryState`
  - [ ] `visual.query.queryState.Data` or `Values`
  - [ ] `projections[]` array
  - [ ] `projections[].field`
  - [ ] `projections[].queryRef`
  - [ ] `projections[].nativeQueryRef`
  - [ ] `projections[].active: true`

- [ ] **Projections active:**
  - [ ] All projections have `active: true`
  - [ ] No missing `active` properties

- [ ] **QueryRef format matches:**
  - [ ] Format: `TableName.FieldName` (dot notation)
  - [ ] Spaces preserved exactly
  - [ ] Underscores preserved exactly
  - [ ] Table prefix always included

- [ ] **Visual type IDs correct:**
  - [ ] `visualType` matches Power BI's expected value
  - [ ] No typos or case mismatches

- [ ] **Folder placement correct:**
  - [ ] Visual folder: `pages/{page_id}/visuals/{visual_id}/`
  - [ ] File name: `visual.json`
  - [ ] Page folder structure correct

- [ ] **Page/Visual IDs unique:**
  - [ ] Page IDs are unique
  - [ ] Visual IDs are unique
  - [ ] No collisions

---

## 1️⃣8️⃣ ADDITIONAL GOTCHAS TO ENCODE

### A) PrototypeQuery Requirement

**Question:**
- [ ] Is `prototypeQuery` required in visual.json?
- [ ] If yes, what structure?
- [ ] If no, can it be omitted?

**Current observation:**
- Not present in your slicer sample
- Unknown for other visual types

**Please confirm:**
- [ ] Required for all visuals?
- [ ] Required for specific visual types only?
- [ ] Can be omitted?

---

### B) FilterConfig Structure

**From your slicer sample:**
- `filterConfig.filters[].name` - unique ID ✅
- `filterConfig.filters[].field` - field reference ✅
- `filterConfig.filters[].type` - "Categorical" ✅
- `filterConfig.filters[].isHiddenInViewMode` - boolean ✅

**Please confirm:**
- [ ] This structure is correct for all slicers?
- [ ] Any variations for different column types?
- [ ] Date slicers have different structure?

---

### C) Visual Container Objects Structure

**From your samples:**
- Slicers: Minimal (most `show: false`)
- Action buttons: Minimal (most `show: false`)
- Cards/Charts: Full structure (background, border, visualHeader, title)

**Please confirm:**
- [ ] Cards require: `background`, `border`, `visualHeader`
- [ ] Charts require: `background`, `border`, `visualHeader`, `title`
- [ ] Slicers require: Minimal structure only
- [ ] Any visual types with different requirements?

---

## 1️⃣7️⃣ INFORMATION DELIVERY FORMAT

**Please provide information in one of these formats:**

### Option 1: Fill This Document
- [ ] Fill in all `___________________________` fields
- [ ] Check all relevant boxes
- [ ] Add notes where needed

### Option 2: Export Files
- [ ] Export complete TMDL model
- [ ] Export one `visual.json` per visual type
- [ ] Export `definition.pbism` and `definition.pbir`
- [ ] Provide Power BI Desktop version info

### Option 3: Hybrid
- [ ] Fill critical sections (Environment, Relationships, QueryRef patterns)
- [ ] Provide golden sample files for visual types
- [ ] Export model manifest

---

## 1️⃣8️⃣ NEXT STEPS

Once this information is provided:

1. **Update** `PRECISE_VISUAL_GENERATION_METHOD.md` with:
   - Environment Lock Block
   - Model Manifest Contract
   - Golden Diff Test section
   - Verified QueryRef patterns
   - Verified sorting rules

2. **Create** generation script that:
   - Validates against model manifest
   - Uses exact golden sample patterns
   - Implements verified sorting rules
   - Matches QueryRef format exactly

3. **Test** generated visuals:
   - Compare to golden samples
   - Verify all required properties
   - Test in Power BI Desktop

---

**Status:** ⏳ Awaiting Information  
**Priority:** High - Required for perfect generation

---

## 📊 CURRENT OBSERVATIONS SUMMARY

### ✅ Observed from current files (not assumptions)

**PBIP (.pbip):**
- Schema: `https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json`
- Version: `1.0`
- Observed: `.pbip` includes `report` artifact only
- Observed: dataset is referenced via `definition.pbir.datasetReference`
- Unknown: whether `.pbip` must also include a `dataset` artifact in your environment (BLOCKER)

**Semantic Model:**
- Format: TMDL ✅ (Observed from current files)
- Version: `4.2` (from `definition.pbism`) ✅ (Observed from current files)
- Compatibility level: `1601` ✅ (Observed from current files)

**Report:**
- Visual schema: `2.4.0` (from visual.json `$schema`) ✅ (Observed from current files)
- Report schema: `4.0` (from `definition.pbir`) ✅ (Observed from current files)
- Page structure: `pages/{page_id}/visuals/{visual_id}/visual.json` ✅ (Observed from current files)

**QueryRef Pattern (from slicer sample):**
- Format: `TableName.FieldName` (dot notation) ✅ (Observed from current files)
- Example: `"Dim_Press_Releases.Page_Type"` ✅ (Observed from current files)
- Spaces/underscores preserved exactly ✅ (Observed from current files)

**NativeQueryRef Pattern (from slicer sample):**
- Format: `FieldName` (no table prefix) ✅ (Observed from current files)
- Example: `"Page_Type"` ✅ (Observed from current files)

**Relationships:**
- `Fact_Press_Analytics[Date] → Dim_Date[Date]` ✅ (Observed from current files - active, many-to-one)
- `Fact_Press_Analytics[Page_URL] → Dim_Press_Releases[Page_URL]` ✅ (Observed from current files - active, many-to-one)

**Date Column Types:**
- `Fact_Press_Analytics[Date]`: `dateTime` ✅ (Observed from current files)
- `Dim_Date[Date]`: `dateTime` ✅ (Observed from current files)
- **Match:** Yes ✅ (Observed from current files)

**Dim_Date:**
- Observed: `Year_Month` exists (display month label) ✅
- Observed: `Month_Year` does not exist
- Observed: `YearMonth` sort key not found (needs confirmation or alternative numeric sort key)

**DAX Locale:**
- Comma separators used in TMDL ✅ (Observed from current files)
- Format strings: `#,0`, `0.0%` ✅ (Observed from current files)

### ⚠️ Discrepancies to Resolve

1. **Spec references `Month_Year` but model has `Year_Month`**
   - Resolution: Use `Year_Month` (actual model column) and resolve `Month_Year` via alias map

2. **Spec references `YearMonth` sort key but not found in model**
   - Resolution: Need to confirm if numeric sort key exists, or create one, or use alternative approach

3. **PBIP dataset artifact location**
   - Observed: Dataset referenced in `definition.pbir` only
   - Unknown: Whether `.pbip` must also include `dataset` artifact (BLOCKER)

4. **Need golden samples for:**
   - Card visual
   - Line chart
   - Donut chart
   - 100% stacked column chart

### ✅ Available Samples

- **Slicer:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/70869c336db70da0c4a2/visual.json`
- **Action Button:** `press-room-dashboard.Report/definition/pages/86b448ef2a89e75fa80e/visuals/43c3caa20026750d70d1/visual.json`

---

## 🎯 MINIMUM PACK (What Cursor Must Deliver)

**If Cursor delivers these, you're basically done:**

1. ✅ **Power BI Desktop version/build**
   - Help → About information

2. ✅ **One golden sample for each visual type:**
   - Card (KPI)
   - Line Chart
   - Donut Chart
   - 100% Stacked Column Chart
   - Slicer (already have, but confirm complete package)

3. ✅ **One full page folder example:**
   - Complete page folder structure
   - Page definition file (`page.json`) that mounts visuals
   - At least one visual folder with `visual.json`
   - Confirmation of how visuals are referenced

4. ✅ **TMDL export OR `model_manifest.json`:**
   - Complete table/column/measure list
   - Relationship definitions
   - SortByColumn metadata
   - Data types

5. ✅ **Confirmed mapping:**
   - `Dim_Date.Year_Month` (actual column name)
   - Chosen numeric sort key strategy
   - Field alias map (spec names → model names)

6. ✅ **QueryRef confirmation:**
   - Measure with spaces: `Metrics[Total Views]` exact format
   - Column format confirmation

7. ✅ **PBIP dataset artifact:**
   - Confirmation of required structure
   - Correct path format

---

## 🎯 PRIORITY INFORMATION NEEDED

**High Priority (Blockers):**
1. 🚨 PBIP dataset artifact confirmation (STOP THE LINE)
2. Power BI Desktop version/build
3. Golden sample visuals (Card, Line, Donut, 100% Stacked Column) - complete packages
4. Page definition integration (how visuals are mounted)
5. QueryRef format for measures with spaces (`Metrics[Total Views]`)

**Medium Priority:**
6. Month_Year vs Year_Month resolution + alias map
7. YearMonth sort key confirmation
8. Model manifest export
9. Sort-by column implementation details (from goldens)
10. Date key normalization check

**Low Priority:**
11. Report-level dependencies (theme, filters, interactions)
12. Visual-specific requirements confirmation
13. Additional gotchas
14. PrototypeQuery requirements
