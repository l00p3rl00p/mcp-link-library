# WORKFLOW_INSTRUCTION.md - Document Processing Workflow

> **Purpose**: Instructions for AI systems, automation tools, and workflows (like Google Antigravity) on how to use `MD_FORMAT.md` as a reference during document creation, cleanup, and modification operations.

---

## Workflow Trigger

**ALWAYS reference `MD_FORMAT.md` when:**

- Creating any new `.md` file
- Reorganizing existing markdown files
- Appending content to existing `.md` files
- Cleaning up documentation
- Converting other formats to markdown
- Reviewing pull requests with markdown changes
- Automated documentation generation

---

## Standard Operating Procedure

### Step 1: Read MD_FORMAT.md First

Before performing ANY markdown operation:

```
1. Load and read MD_FORMAT.md
2. Identify the operation type:
   - New document creation
   - Document reorganization
   - Content appending
   - Cleanup/refactoring
3. Jump to relevant section in MD_FORMAT.md
4. Apply the guidance from that section
```

### Step 2: Detect Document Type

Use the detection rules from MD_FORMAT.md:

```
1. Check filename pattern (README.md, ARCHITECTURE.md, etc.)
2. Analyze content patterns (API endpoints, environment vars, etc.)
3. Auto-select appropriate template from MD_FORMAT.md
4. Apply document-specific formatting rules
```

### Step 3: Execute Operation

Follow the specific workflow based on operation type:

#### For New Document Creation:

```
1. Select template from MD_FORMAT.md "Common Patterns by Document Type"
2. Apply "Standard Document Structure"
3. Follow formatting standards
4. Validate with "Validation Checklist"
```

#### For Document Reorganization:

```
1. Identify current document type
2. Map sections to "Section Organization Rules" in MD_FORMAT.md
3. Apply appropriate template
4. Preserve ALL content (move, never delete without confirmation)
5. Update Table of Contents
6. Validate with checklist
```

#### For Content Appending:

```
1. Read existing document structure
2. Use "Appending Content Guidelines" decision tree from MD_FORMAT.md
3. Determine logical placement
4. Select appropriate appending method
5. Update Table of Contents if needed
6. Verify no contradictions created
```

#### For Cleanup/Refactoring:

```
1. Check against "Anti-Patterns to Avoid" in MD_FORMAT.md
2. Fix in priority order:
   a. Structure issues
   b. Formatting issues
   c. Content optimization
3. Validate against checklist
4. Preserve all meaningful content
```

### Step 4: Validate Output

Before finalizing:

```
1. Run through "Validation Checklist" in MD_FORMAT.md
2. Verify document type-specific requirements met
3. Check for anti-patterns
4. Ensure all cross-references work
5. Confirm Table of Contents is accurate
```

---

## Integration with Specific Workflows

### Google Antigravity / AI Workflow Integration

#### Workflow File Structure

```yaml
# workflow-config.yaml
name: "Markdown Document Processing"
trigger:
  - file_create: "*.md"
  - file_update: "*.md"
  - cleanup_request: true

steps:
  - name: "Load Reference"
    action: read_file
    file: "MD_FORMAT.md"
    store_as: "format_reference"
  
  - name: "Detect Operation Type"
    action: analyze
    input: "${event.type}"
    output: "operation_type"
  
  - name: "Detect Document Type"
    action: analyze
    input: "${file.name}, ${file.content}"
    reference: "${format_reference.document_type_detection}"
    output: "document_type"
  
  - name: "Apply Formatting Rules"
    action: transform
    input: "${file.content}"
    rules: "${format_reference[operation_type][document_type]}"
    output: "formatted_content"
  
  - name: "Validate Output"
    action: validate
    input: "${formatted_content}"
    checklist: "${format_reference.validation_checklist}"
    output: "validation_results"
  
  - name: "Write Result"
    action: write_file
    content: "${formatted_content}"
    condition: "${validation_results.passed == true}"
```

#### Integration Points

```python
# Example Python integration
from workflows import DocumentWorkflow

workflow = DocumentWorkflow()

# Load reference guide
workflow.load_reference("MD_FORMAT.md")

# Process document
result = workflow.process_markdown(
    operation="create",  # or "reorganize", "append", "cleanup"
    filepath="NEW_DOC.md",
    content=new_content
)

# Workflow automatically:
# 1. Detects document type
# 2. Applies appropriate template
# 3. Validates output
# 4. Returns formatted content
```

### Manual Workflow (Human-Readable)

When manually creating or editing markdown:

```
┌─────────────────────────────────────────┐
│ 1. Open MD_FORMAT.md                    │
├─────────────────────────────────────────┤
│ 2. Find your document type:             │
│    - Check filename patterns table      │
│    - Check content patterns table       │
├─────────────────────────────────────────┤
│ 3. Navigate to template section:        │
│    "Common Patterns by Document Type"   │
├─────────────────────────────────────────┤
│ 4. Copy template structure              │
├─────────────────────────────────────────┤
│ 5. Fill in your content                 │
├─────────────────────────────────────────┤
│ 6. Apply formatting standards:          │
│    - Code blocks with language          │
│    - Proper heading hierarchy           │
│    - Table formatting                   │
├─────────────────────────────────────────┤
│ 7. Run validation checklist             │
├─────────────────────────────────────────┤
│ 8. Fix any issues found                 │
└─────────────────────────────────────────┘
```

### For Changelog Files (CHANGELOG.md)

When creating or updating changelogs, apply these additional rules:

```
┌─────────────────────────────────────────────────────────────┐
│ CHANGELOG.md SPECIFIC REQUIREMENTS                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Format References (REQUIRED):                            │
│    - Include Keep a Changelog link                          │
│    - Include Semantic Versioning link                       │
├─────────────────────────────────────────────────────────────┤
│ 2. Standard Categories ONLY:                                │
│    ✓ Added       - New features                             │
│    ✓ Changed     - Changes to existing functionality        │
│    ✓ Deprecated  - Soon-to-be removed features              │
│    ✓ Removed     - Removed features                         │
│    ✓ Fixed       - Bug fixes                                │
│    ✓ Security    - Security improvements                    │
│    ✗ Do NOT use: Improvements, Patches, Updates, etc.       │
├─────────────────────────────────────────────────────────────┤
│ 3. Version Format:                                          │
│    - Semver: MAJOR.MINOR.PATCH (e.g., 1.2.3)                │
│    - Date: YYYY-MM-DD (e.g., 2024-02-06)                    │
│    - Format: ## [1.2.0] - 2024-02-06                        │
├─────────────────────────────────────────────────────────────┤
│ 4. Structure:                                               │
│    - [Unreleased] section always at top                     │
│    - Versions in descending order (newest first)            │
│    - Each version must have a date                          │
├─────────────────────────────────────────────────────────────┤
│ 5. When Appending to CHANGELOG.md:                          │
│    - Add to [Unreleased] section under correct category     │
│    - Use bullet points with clear descriptions              │
│    - When releasing: move [Unreleased] items to new version │
│    - Update version number following semver rules           │
└─────────────────────────────────────────────────────────────┘
```

**Changelog Category Decision Tree:**

```
What type of change is this?
├─ New feature/capability → Added
├─ Modification to existing feature → Changed
├─ Marking feature for future removal → Deprecated
├─ Feature no longer available → Removed
├─ Bug fix → Fixed
└─ Security-related → Security
```

---

## AI Prompt Templates

### For New Document Creation

```
I need to create a new markdown file. Please follow these steps:

1. Read MD_FORMAT.md for reference
2. Detect the appropriate document type based on:
   - Filename: [FILENAME]
   - Purpose: [DESCRIPTION]
3. Apply the template from "Common Patterns by Document Type"
4. Use the content I provide: [CONTENT]
5. Validate against the "Validation Checklist"
6. Present the formatted markdown

Do not deviate from the MD_FORMAT.md standards unless I explicitly request it.
```

### For Document Reorganization

```
I need to reorganize this markdown file. Please follow these steps:

1. Read MD_FORMAT.md for reference
2. Detect the document type
3. Map existing sections to "Section Organization Rules"
4. Apply the appropriate template structure
5. PRESERVE ALL EXISTING CONTENT (move, don't delete)
6. Update the Table of Contents
7. Validate against the "Validation Checklist"

Document to reorganize: [PASTE OR ATTACH DOCUMENT]

Do not remove any content unless it's truly redundant.
```

### For Content Appending

```
I need to append content to an existing markdown file. Please follow these steps:

1. Read MD_FORMAT.md for reference
2. Analyze the existing document structure
3. Use the "Appending Content Guidelines" decision tree
4. Determine the logical placement for: [NEW CONTENT]
5. Select the appropriate appending method
6. Update Table of Contents if needed
7. Check for contradictions with existing content
8. Validate the result

Existing document: [PASTE OR ATTACH DOCUMENT]
Content to append: [NEW CONTENT]
```

### For Cleanup/Refactoring

```
I need to clean up this markdown file. Please follow these steps:

1. Read MD_FORMAT.md for reference
2. Check against "Anti-Patterns to Avoid"
3. Fix issues in priority order:
   - Structure issues first
   - Formatting issues second
   - Content optimization third
4. Validate against the "Validation Checklist"
5. Preserve all meaningful content

Document to clean up: [PASTE OR ATTACH DOCUMENT]
```

---

## Quality Gates

Every markdown operation should pass these gates:

### Gate 1: Structure Compliance
```
✓ Single H1 heading
✓ Quick Start present (if actionable doc)
✓ Table of Contents with working links
✓ Logical section progression
✓ No skipped heading levels
```

### Gate 2: Format Compliance
```
✓ Code blocks specify language
✓ Tables properly formatted
✓ Links are descriptive
✓ Consistent list markers
✓ Appropriate emphasis usage
```

### Gate 3: Content Quality
```
✓ Clear value proposition
✓ Prerequisites listed
✓ Examples demonstrate usage
✓ No contradictions
✓ Troubleshooting included
```

### Gate 4: Document Type Compliance
```
✓ Matches template for document type
✓ Includes required sections
✓ Follows type-specific patterns
✓ Uses appropriate structure
```

### Gate 5: CHANGELOG.md Specific Compliance
```
✓ References Keep a Changelog format (https://keepachangelog.com/)
✓ References Semantic Versioning (https://semver.org/)
✓ Uses only standard six categories: Added, Changed, Deprecated, Removed, Fixed, Security
✓ Dates in ISO 8601 format (YYYY-MM-DD)
✓ Version numbers follow semver (MAJOR.MINOR.PATCH)
✓ [Unreleased] section present at top
✓ Versions in descending order (newest first)
✓ Each version has a release date
```

---

## Error Handling

### If MD_FORMAT.md is Missing

```
ERROR: Reference file MD_FORMAT.md not found.

Fallback action:
1. Alert user that formatting reference is missing
2. Apply minimal safe defaults:
   - Single H1 title
   - Table of Contents
   - Logical section order
   - Basic formatting
3. Suggest downloading MD_FORMAT.md
4. Log warning for review
```

### If Document Type Cannot Be Detected

```
WARNING: Could not auto-detect document type.

Fallback action:
1. Prompt user to specify document type
2. Options:
   - README
   - Architecture
   - Security
   - Environment
   - API
   - Tutorial
   - Contributing
   - Other (use generic template)
3. Apply selected template
4. Continue workflow
```

### If Validation Fails

```
ERROR: Validation failed.

Action:
1. Report which checklist items failed
2. Provide specific fixes needed
3. Offer to auto-fix common issues
4. Ask user to review manual fixes
5. Re-run validation after fixes
```

---

## Continuous Improvement

### Feedback Loop

When encountering edge cases or new patterns:

```
1. Document the issue
2. Determine if MD_FORMAT.md should be updated
3. Propose addition to MD_FORMAT.md
4. Update this workflow if needed
5. Share learnings with team
```

### Metrics to Track

```
- Documents processed
- Validation pass rate
- Common anti-patterns found
- Time saved vs manual formatting
- Document type distribution
- Most common appending locations
```

---

## Examples

### Example 1: Creating New Security Documentation

```bash
# User request: "Create security documentation for our API"

# Workflow executes:
1. Reads MD_FORMAT.md
2. Detects type: Security Documentation (from filename SECURITY.md)
3. Applies template from "For Security Documentation"
4. Includes required sections:
   - Security Principles
   - Threat Model
   - Security Controls
   - Audit & Logging
   - Vulnerability Disclosure
   - etc.
5. Validates output
6. Presents formatted SECURITY.md
```

### Example 2: Appending Configuration Option

```bash
# User request: "Add new DATABASE_POOL_SIZE config option to ENVIRONMENT.md"

# Workflow executes:
1. Reads MD_FORMAT.md
2. Reads existing ENVIRONMENT.md
3. Uses "Appending Content Guidelines"
4. Determines location: "Optional Variables" section
5. Appending method: Table Row Addition
6. Adds row to table:
   | DATABASE_POOL_SIZE | Connection pool size | 10 |
7. Updates TOC if needed
8. Validates output
9. Presents updated ENVIRONMENT.md
```

### Example 3: Cleaning Up Legacy Documentation

```bash
# User request: "Clean up old README.md - it's a mess"

# Workflow executes:
1. Reads MD_FORMAT.md
2. Analyzes existing README.md
3. Checks against "Anti-Patterns to Avoid"
4. Finds issues:
   - Multiple H1 headings → Fix: Use single H1
   - Missing Quick Start → Fix: Add Quick Start section
   - Code blocks without language → Fix: Add language specs
   - No Table of Contents → Fix: Generate TOC
5. Applies fixes in priority order
6. Validates against checklist
7. Presents cleaned README.md
```

### Example 4: Updating CHANGELOG.md with New Changes

```bash
# User request: "Add these changes to the changelog: added new API endpoint, fixed login bug"

# Workflow executes:
1. Reads MD_FORMAT.md
2. Reads existing CHANGELOG.md
3. Validates current format:
   - Keep a Changelog reference: ✓
   - Semantic Versioning reference: ✓
   - Standard categories present: ✓
4. Determines correct categories:
   - "added new API endpoint" → Added section
   - "fixed login bug" → Fixed section
5. Appends to [Unreleased] section:
   ### Added
   - New API endpoint for user preferences
   
   ### Fixed
   - Login authentication timeout bug
6. Validates changelog-specific rules (Gate 5)
7. Presents updated CHANGELOG.md
```

### Example 5: Creating New CHANGELOG.md

```bash
# User request: "Create a changelog for this project"

# Workflow executes:
1. Reads MD_FORMAT.md
2. Detects type: Changelog (from filename CHANGELOG.md)
3. Applies template from "For Changelogs"
4. Includes required elements:
   - Keep a Changelog reference link
   - Semantic Versioning reference link
   - [Unreleased] section with all six categories
   - Example version entry with proper date format
5. Validates against Gate 5 (CHANGELOG.md specific)
6. Presents formatted CHANGELOG.md
```

---

## Quick Reference Card

Keep this handy when working with markdown:

```
┌─────────────────────────────────────────────────────────────┐
│                  MARKDOWN WORKFLOW CHEAT SHEET              │
├─────────────────────────────────────────────────────────────┤
│ BEFORE ANY MARKDOWN OPERATION:                              │
│ 1. Read MD_FORMAT.md                                        │
│ 2. Detect document type                                     │
│ 3. Apply appropriate template                               │
│ 4. Validate output                                          │
├─────────────────────────────────────────────────────────────┤
│ CREATING NEW DOC:                                           │
│ → Use template from "Common Patterns by Document Type"      │
├─────────────────────────────────────────────────────────────┤
│ REORGANIZING:                                               │
│ → Follow "Section Organization Rules"                       │
│ → PRESERVE all content (move, don't delete)                 │
├─────────────────────────────────────────────────────────────┤
│ APPENDING:                                                  │
│ → Use "Appending Content Guidelines" decision tree          │
│ → Update Table of Contents                                  │
├─────────────────────────────────────────────────────────────┤
│ CLEANING UP:                                                │
│ → Check "Anti-Patterns to Avoid"                            │
│ → Fix: Structure → Format → Content                         │
├─────────────────────────────────────────────────────────────┤
│ ALWAYS VALIDATE WITH CHECKLIST BEFORE FINALIZING            │
└─────────────────────────────────────────────────────────────┘
```

---

## Support & Questions

If you encounter situations not covered by MD_FORMAT.md or this workflow:

1. **Document the edge case** with example
2. **Determine best practice** through team discussion
3. **Update MD_FORMAT.md** with new pattern
4. **Update this workflow** if needed
5. **Share with team** for consistency

---

**Version**: 1.0.0  
**Last Updated**: 2024-02-06  
**Maintained by**: Documentation Team  
**Questions**: Open an issue or contact documentation team