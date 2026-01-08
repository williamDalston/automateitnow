# 📋 DASHBOARD STRUCTURE & NAMING - FINAL PLAN

**Purpose:** Central document defining all page names, titles, structure, and layout choices for the Press Room Dashboard.

**Status:** ✅ **SUPERSEDED** - See `FINAL_DASHBOARD_SPEC.md` for locked decisions

**Note:** This document was used for iteration. Final decisions are now in:
- `FINAL_DASHBOARD_SPEC.md` - Complete specification
- `DECISIONS_LOG.md` - Record of all decisions and rationale
- `QUICK_REFERENCE.md` - One-page reference card

---

## 🎯 DESIGN PRINCIPLES

1. **Professional & Clear** - Names should be immediately understandable
2. **Concise** - Short but descriptive
3. **Consistent** - Follow naming patterns throughout
4. **User-Focused** - What users actually call these things
5. **HHS Standards** - Align with HHS.gov terminology

---

## 📄 PAGE STRUCTURE & NAMING

### **Page 1: Home/Overview**

**Current Options Found:**
- "Executive Summary" (from blueprint)
- "Press Releases Analytics" (from spec database)
- "Executive Overview" (from implementation plan)
- "HOME: Executive Summary" ❌ (user doesn't like this format)

**Recommended Options:**
1. **"Executive Overview"** ✅
   - Professional, clear purpose
   - Common in federal dashboards
   - Implies high-level summary
   
2. **"Press Room Performance"**
   - Direct, descriptive
   - Clear about scope
   
3. **"Performance Summary"**
   - Concise
   - Universal term
   
4. **"Dashboard Overview"**
   - Clear and standard
   - Not specific enough?

**🎯 RECOMMENDED:** **"Executive Overview"**

**Rationale:** 
- Professional and commonly used in federal/executive reporting
- Implies high-level strategic view
- Not too long, not too short
- Clear distinction from detailed pages

---

### **Page 2: Releases**

**Current Options Found:**
- "All Press Releases" (from spec database)
- "All Releases" (from implementation plan)
- "Releases" (short form)

**Recommended Options:**
1. **"All Press Releases"** ✅
   - Complete and clear
   - Matches HHS terminology
   
2. **"Press Releases"**
   - Shorter, still clear
   - Implies all releases
   
3. **"Release Catalog"**
   - More formal
   - Sounds like a directory

**🎯 RECOMMENDED:** **"Press Releases"**

**Rationale:**
- Concise and clear
- Users understand "Press Releases" means all of them
- Matches common HHS.gov navigation patterns
- Shorter names work better in navigation

---

### **Page 3: Channels**

**Current Options Found:**
- "Channel Attribution Analysis" (from spec database)
- "Channel Analysis" (from implementation plan)
- "Channels" (short form)

**Recommended Options:**
1. **"Channel Performance"** ✅
   - Professional, clear purpose
   - Aligns with "Performance" theme
   
2. **"Traffic Sources"**
   - Web analytics standard term
   - Clear about what it shows
   
3. **"Channel Analysis"**
   - Formal, academic tone
   - Slightly longer

4. **"Channel Attribution"**
   - Technical, precise
   - May be too jargon-heavy

**🎯 RECOMMENDED:** **"Channel Performance"**

**Rationale:**
- Professional and clear
- Consistent with performance theme
- Users understand "channels" in web context
- Concise

---

### **Page 4: Landing Page**

**Current Options Found:**
- "Press Room Landing Page" (from spec database)
- "Landing Page Detail" (from implementation plan)
- "Landing Page" (short form)

**Recommended Options:**
1. **"Landing Page Performance"** ✅
   - Consistent with other page names
   - Clear about what's being analyzed
   
2. **"Entry Point Analysis"**
   - More descriptive
   - Technical but clear
   
3. **"Press Room Landing"**
   - Concise
   - Context is clear

4. **"Home Page Performance"**
   - Alternative terminology
   - May confuse with Page 1

**🎯 RECOMMENDED:** **"Landing Page Performance"**

**Rationale:**
- Consistent with naming pattern (Performance theme)
- Clear about analyzing the landing page
- Professional tone
- Not too long

---

### **Page 5: Release Detail (Drillthrough)**

**Current Options Found:**
- "Release Detail" (from spec database)
- "Release Detail" (from implementation plan)

**Recommended Options:**
1. **"Release Detail"** ✅
   - Clear, standard terminology
   - Common in drillthrough pages
   
2. **"Press Release Detail"**
   - More explicit
   - Slightly redundant

3. **"Release Analytics"**
   - Consistent with analytics theme
   - Clear purpose

**🎯 RECOMMENDED:** **"Release Detail"**

**Rationale:**
- Standard drillthrough page naming
- Clear and concise
- Context is clear (it's a detail page)

---

## 📋 COMPLETE PAGE STRUCTURE

### Main Navigation Pages (4)

| Page ID | Display Name | Internal Name | Purpose |
|---------|--------------|---------------|---------|
| 1 | **Executive Overview** | `home` | High-level KPIs and performance summary |
| 2 | **Press Releases** | `releases` | All press releases with search and filters |
| 3 | **Channel Performance** | `channels` | Traffic source analysis and attribution |
| 4 | **Landing Page Performance** | `landing` | Landing page specific analytics |

### Supporting Pages

| Page ID | Display Name | Internal Name | Purpose |
|---------|--------------|---------------|---------|
| 5 | **Release Detail** | `release_detail` | Drillthrough page for individual releases |
| 6 | **Metric Dictionary** | `metric_dictionary` | Definitions and glossary (optional) |

### Hidden/Utility Pages

| Page ID | Display Name | Internal Name | Purpose |
|---------|--------------|---------------|---------|
| Tooltip Pages | Various | `tooltip_*` | Enhanced tooltip content |

---

## 🎨 NAVIGATION BUTTON LABELS

**Navigation Rail (Left Side):**

| Button | Label | Icon | Links To |
|--------|-------|------|----------|
| 1 | **Overview** | Home icon | Executive Overview |
| 2 | **Releases** | Releases icon | Press Releases |
| 3 | **Channels** | Channels icon | Channel Performance |
| 4 | **Landing** | Landing icon | Landing Page Performance |

**Rationale:**
- Short labels for compact navigation
- Icon + label for clarity
- "Overview" instead of "Home" (more professional)
- Single-word labels where possible

---

## 📊 SECTION HEADERS & SUBTITLES

### Page 1: Executive Overview

**Main Title:** "Press Room Analytics"

**Optional Subtitle Options:**
1. "Performance Overview"
2. "Executive Dashboard"  
3. "Strategic Overview"
4. None (let visuals speak)

**🎯 RECOMMENDED:** No subtitle (cleaner, more modern)

---

### Page 2: Press Releases

**Main Title:** "Press Releases"

**Optional Subtitle:**
1. "All Releases"
2. "Search and Filter"
3. None

**🎯 RECOMMENDED:** None

---

### Page 3: Channel Performance

**Main Title:** "Channel Performance"

**Optional Subtitle:**
1. "Traffic Source Analysis"
2. "Attribution Analysis"
3. None

**🎯 RECOMMENDED:** None

---

### Page 4: Landing Page Performance

**Main Title:** "Landing Page Performance"

**Optional Subtitle:**
1. "Entry Point Analytics"
2. "Press Room Homepage"
3. None

**🎯 RECOMMENDED:** None

---

## 🔤 TYPOGRAPHY & LABELING

### KPI Card Labels

**Page 1 - Executive Overview (6 KPIs):**

1. **"Total Views"** ✅
   - Clear, standard metric
   
2. **"Total Users"** ✅
   - Clear, standard metric
   
3. **"Landing Page Share"** 
   - OR "Landing Page %"
   - OR "% Landing Page"
   - **🎯 RECOMMENDED:** "Landing Page %"
   
4. **"Press Releases"**
   - OR "# Press Releases"
   - **🎯 RECOMMENDED:** "Press Releases" (count implied)
   
5. **"Avg Views/Release"**
   - OR "Avg per Release"
   - **🎯 RECOMMENDED:** "Avg per Release"
   
6. **"Top 10 Share"**
   - OR "Top 10 %"
   - **🎯 RECOMMENDED:** "Top 10 %"

---

### Chart Titles

**Naming Convention:**
- Use title case
- Be specific but concise
- Include time period if relevant
- Avoid abbreviations where possible

**Examples:**
- ✅ "Views Trend (Last 30 Days)"
- ✅ "Channel Share Distribution"
- ❌ "Views Trnd"
- ❌ "Chan Share"

---

## 📐 LAYOUT & STRUCTURE

### Canvas Size
- **Width:** 1280 pixels
- **Height:** 720 pixels
- **Aspect Ratio:** 16:9
- **Display:** FitToPage

### Grid System
- **Margins:** 20px (all sides)
- **Spacing:** 20px between elements
- **Z-index Range:** 1000-5000

### Header Band
- **Height:** 40px
- **Position:** Top of canvas
- **Contains:**
  - Page title (left)
  - Date context (right, top)
  - Last refreshed (right, bottom)

### Footer Band
- **Height:** 24px
- **Position:** Bottom of canvas
- **Contains:**
  - Data source (left)
  - Page number (center)
  - Generated date (right)

---

## 🎯 RECOMMENDED FINAL STRUCTURE

### Complete Page List (Priority Order)

1. **Executive Overview** (`home`)
   - Main landing page
   - 6 KPI cards
   - 3 hero tiles
   - Top 10 table

2. **Press Releases** (`releases`)
   - 4 KPI cards
   - Search box
   - Filter panel
   - All releases table

3. **Channel Performance** (`channels`)
   - 5 channel KPI cards
   - Channel over time chart
   - Channel performance matrix

4. **Landing Page Performance** (`landing`)
   - Landing page performance card
   - Traffic sources breakdown
   - Daily trend chart

5. **Release Detail** (`release_detail`)
   - Drillthrough page
   - Individual release analytics

---

## ✅ DECISION CHECKLIST

### Page Names
- [ ] Page 1: "Executive Overview" ✅ (Recommended)
- [ ] Page 2: "Press Releases" ✅ (Recommended)
- [ ] Page 3: "Channel Performance" ✅ (Recommended)
- [ ] Page 4: "Landing Page Performance" ✅ (Recommended)
- [ ] Page 5: "Release Detail" ✅ (Recommended)

### Navigation Labels
- [ ] Button 1: "Overview" ✅ (Recommended)
- [ ] Button 2: "Releases" ✅ (Recommended)
- [ ] Button 3: "Channels" ✅ (Recommended)
- [ ] Button 4: "Landing" ✅ (Recommended)

### KPI Labels
- [ ] Review all KPI labels above
- [ ] Finalize formatting preferences

---

## 🔄 NEXT STEPS

1. **Review all recommendations above**
2. **Make final decisions on page names**
3. **Update implementation documents**
4. **Update code/generation scripts**
5. **Validate in working dashboard**

---

## 📝 NOTES FOR ITERATION

**User Feedback:**
- ❌ Don't like "HOME: Executive Summary" format
- ✅ Want professional, thoughtful choices
- ✅ Need best possible final plan

**Current Status:**
- This document consolidates all naming options
- Recommendations provided for each choice
- Ready for final review and decision

---

**Last Updated:** December 2024  
**Status:** Ready for Review & Decision
