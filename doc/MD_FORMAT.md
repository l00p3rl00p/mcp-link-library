# MD_FORMAT.md - Markdown Best Practices Reference

> **Purpose**: This document serves as the authoritative reference for structuring, formatting, and appending to markdown files. AI workflows, document cleanup processes, and automated tools should consult this file before creating or modifying any `.md` file.

---

## When to Use This Guide

**Trigger Conditions** - Reference this document when:
- Creating any new `.md` file
- Reorganizing existing markdown documentation
- Appending content to existing `.md` files
- Cleaning up or refactoring documentation
- Converting other formats to markdown
- Automated documentation generation

---

## Table of Contents

1. [Standard Document Structure](#standard-document-structure)
2. [Document Type Detection](#document-type-detection)
3. [Section Organization Rules](#section-organization-rules)
4. [Appending Content Guidelines](#appending-content-guidelines)
5. [Formatting Standards](#formatting-standards)
6. [Common Patterns by Document Type](#common-patterns-by-document-type)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
8. [Validation Checklist](#validation-checklist)

---

## Standard Document Structure

Every markdown file should follow this hierarchy:

```markdown
# Document Title
[Logo/Image - if applicable]
[2-3 sentence value proposition]
[Optional: "Why this matters" explanation]

---

## ⚡ Quick Start / Get Started Now
[3-5 minimal steps to achieve primary goal]
[Next step pointer to detailed guide]

---

## 📋 Table of Contents
1. [Section One](#section-one)
2. [Section Two](#section-two)
...

---

## [First Major Section]
[Content organized logically]

## [Second Major Section]
[Content organized logically]

...

## [Metadata Section - License, Author, etc.]
```

### Hierarchy Rules

1. **Only ONE H1 (`#`)** - The document title
2. **H2 (`##`)** for major sections
3. **H3 (`###`)** for subsections
4. **H4 (`####`)** for sub-subsections (use sparingly)
5. **Never skip heading levels** (don't go from H2 to H4)

---

## Document Type Detection

**Auto-detect document type based on:**

### Filename Patterns

| Pattern | Document Type | Apply Template |
|---------|---------------|----------------|
| `README.md` | Project README | [Project README](#for-project-readmes) |
| `ARCHITECTURE.md`, `DESIGN.md` | Architecture | [Architecture](#for-architecture-documentation) |
| `SECURITY.md`, `THREAT_MODEL.md` | Security | [Security](#for-security-documentation) |
| `ENVIRONMENT.md`, `.env.example`, `CONFIG.md` | Environment | [Environment](#for-environmentconfiguration-documentation) |
| `API.md`, `ENDPOINTS.md` | API Documentation | [API](#for-api-documentation) |
| `CONTRIBUTING.md` | Contribution Guide | [Contributing](#for-contributing-guides) |
| `CHANGELOG.md` | Changelog | [Changelog](#for-changelogs) |
| `TUTORIAL.md`, `GUIDE.md`, `GETTING_STARTED.md` | Tutorial | [Tutorial](#for-tutorialsguides) |
| `LICENSE.md` | License | [License](#for-license-files) |

### Content Pattern Detection

| Content Contains | Likely Type | Apply Template |
|------------------|-------------|----------------|
| API endpoints, HTTP methods, request/response | API Documentation | [API](#for-api-documentation) |
| `pip install`, `npm install`, code examples | Library/Package | [Library](#for-librariespackages) |
| "Step 1", "Next", numbered instructions | Tutorial | [Tutorial](#for-tutorialsguides) |
| Environment variables, configuration keys | Environment | [Environment](#for-environmentconfiguration-documentation) |
| Threat model, security controls, compliance | Security | [Security](#for-security-documentation) |
| Component diagrams, system design, data flow | Architecture | [Architecture](#for-architecture-documentation) |

---

## Section Organization Rules

### Universal Section Order

Apply this order unless document type requires different structure:

1. **Title & Introduction** (always first)
2. **Quick Start** (for actionable docs)
3. **Table of Contents** (always after Quick Start)
4. **Overview/Background** (context setting)
5. **Prerequisites** (requirements)
6. **Installation/Setup** (how to get started)
7. **Basic Usage** (common use cases)
8. **Configuration** (customization options)
9. **Advanced Features** (power user content)
10. **API Reference** (detailed technical docs)
11. **Examples** (real-world scenarios)
12. **Troubleshooting** (common issues)
13. **Architecture/Design** (technical deep-dive)
14. **Contributing** (for open source)
15. **FAQ** (common questions)
16. **Related Resources** (links to other docs)
17. **Metadata** (license, author, changelog link)
18. **Git Optional Dependencies** (cross repo options, links to other repos for better execution or package completeness, Pro and Cons of the dependency)

### Section Emojis (Recommended)

Use these emojis for visual hierarchy:

- ⚡ Quick Start / Get Started
- 📋 Table of Contents
- 🔍 Overview / About
- 🌟 Features / Highlights
- 🔌 Integration / Plugins
- 🔐 Security / Authentication
- 💻 Usage / Examples
- 🛠 Configuration / Setup
- ⚙️ Advanced / Technical
- 🐛 Troubleshooting / Debugging
- 📚 Documentation / Resources
- 🤝 Contributing
- 📝 License / Legal

---

## Appending Content Guidelines

### Before Appending - Decision Tree

```
Is the content new information?
├─ YES: Determine where it belongs (see Section Organization Rules)
│   ├─ Does a relevant section exist?
│   │   ├─ YES: Append to that section as a subsection
│   │   └─ NO: Create new section in logical position
│   └─ Is it a variation/alternative?
│       ├─ YES: Use <details> collapsible section
│       └─ NO: Add as new subsection
└─ NO: Is it redundant?
    ├─ YES: Don't append, update existing content instead
    └─ NO: Determine if it's a different perspective
        ├─ YES: Add as "Alternative Approach" subsection
        └─ NO: Skip appending
```

### Where to Append Based on Content Type

| Content Type | Append Location | Method |
|--------------|----------------|---------|
| New feature/capability | Features section | Add as new bullet or subsection |
| Installation method | Installation section | Add as `<details>` for alternative methods |
| Configuration option | Configuration section | Add to existing table or create subsection |
| Code example | Examples section | Add with clear heading describing use case |
| Troubleshooting tip | Troubleshooting section | Add as new subsection with problem/solution format |
| API endpoint | API Reference | Add to endpoint table or create new subsection |
| Security consideration | Security section | Add under relevant security category |
| Architecture detail | Architecture section | Add to relevant component description |

### Appending Methods

#### Method 1: Subsection Addition
```markdown
## Existing Section

### Existing Content
[original content]

### New Addition - [Descriptive Title]
[new content]
```

#### Method 2: Collapsible Section (for optional/advanced content)
```markdown
## Existing Section

[main content]

<details>
<summary><b>Alternative Method / Advanced Usage</b></summary>

[new content that's optional or advanced]

</details>
```

#### Method 3: Table Row Addition
```markdown
## Existing Section

| Column 1 | Column 2 |
|----------|----------|
| Existing | Data     |
| New Row  | New Data |
```

#### Method 4: List Extension
```markdown
## Existing Section

* Existing item
* Another existing item
* **New item** - [clear description]
```

### Appending Anti-Patterns

**DON'T:**
- ❌ Append at the end of the document without considering structure
- ❌ Create duplicate sections with slightly different names
- ❌ Break the Table of Contents by not updating it
- ❌ Append without checking if content already exists
- ❌ Add content that contradicts existing information without reconciling
- ❌ Create orphaned sections that don't fit the logical flow
- ❌ fix or update code within explanation sections as they maybe explantions of bad code

**DO:**
- ✅ Find the most logical section for the content
- ✅ Update the Table of Contents
- ✅ Maintain consistent heading levels
- ✅ Use collapsible sections for optional content
- ✅ Reconcile contradictions before appending
- ✅ Preserve the document's logical flow
- ✅ Preserve code or code examples which explain functionality (error on the side of keeping) 

---

## Formatting Standards

### Code Blocks

Always specify the language:

```markdown
```bash
command here
```

```python
code here
```

```yaml
config here
```
```

### Tables

Use markdown tables with proper alignment:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

For long tables, consider using `<details>`:

```markdown
<details>
<summary><b>Full Configuration Reference (Click to expand)</b></summary>

| Variable | Description | Default |
|----------|-------------|---------|
| ...      | ...         | ...     |

</details>
```

### Links

- **Anchor links**: Use lowercase with hyphens: `[Section](#section-name)`
- **External links**: Include description: `[LiteLLM Documentation](https://docs.litellm.ai)`
- **Relative links**: For files in repo: `[Architecture](./ARCHITECTURE.md)`

### Lists

- Use `*` for unordered lists (consistency)
- Use `1.` for ordered lists (auto-numbering)
- Indent nested lists with 2 spaces

### Emphasis

- **Bold** for important terms, UI elements: `**important**`
- *Italic* for emphasis, technical terms: `*emphasis*`
- `Code formatting` for: commands, variables, filenames, code: `` `code` ``
- **Bold + code** for critical commands: `` **`pip install`** ``

### Callouts

Use blockquotes for important notes:

```markdown
> **Note**: Important information here

> **Warning**: Critical warning here

> **Tip**: Helpful tip here
```

---

## Common Patterns by Document Type

### For Project READMEs

```markdown
# Project Name
[Logo]
[Value proposition]

## ⚡ Quick Start
[Minimal installation + first command]

## 📋 Table of Contents
[Sections...]

## 🔍 Overview
[What it does, why it exists]

## 🌟 Features
[Key capabilities]

## Prerequisites
[Requirements]

## Installation
[Step-by-step]

## Quick Example
[Simple code example]

## Configuration
[How to customize]

## Documentation
[Links to detailed docs]

## Contributing
[How to contribute]

## License
[License info]

## Author
[Author/maintainer info]
```

### For Architecture Documentation

```markdown
# Architecture / System Design

[High-level overview diagram/description]

## 📋 Table of Contents
[Sections...]

## Design Principles
[Core architectural principles]

## System Overview
[High-level component description]

## Technology Stack
[Technologies and justification]

## Components
### Component A
[Description, responsibilities, interfaces]

### Component B
[Description, responsibilities, interfaces]

## Data Flow
[How data moves through the system]

## Component Interactions
[How components communicate]

## Design Decisions
[ADRs or key architectural choices]

## Scalability Considerations
[How system scales]

## Performance Considerations
[Performance characteristics]

## Security Architecture
[Security design]

## Known Limitations
[Current constraints]

## Future Considerations
[Planned improvements]
```

### For Security Documentation

```markdown
# Security Model / Security Guide

[Overview of security approach]

## 📋 Table of Contents
[Sections...]

## Security Principles
[Core security principles]

## Threat Model
[Potential threats and attack vectors]

## Security Controls
### Authentication
[How authentication works]

### Authorization
[Access control mechanisms]

### Data Protection
[Encryption, PII handling, data retention]

## Audit & Logging
[What's logged, where, retention]

## Security Best Practices
[Deployment security checklist]

## Compliance
[Relevant standards: SOC2, GDPR, HIPAA, etc.]

## Vulnerability Disclosure
[How to report security issues]

## Incident Response
[What to do if breach occurs]

## Security Contact
[Contact information]
```

### For Environment/Configuration Documentation

```markdown
# Environment Configuration

[Overview of configuration approach]

## ⚡ Quick Setup
[Minimal .env example for getting started]

## 📋 Table of Contents
[Sections...]

## Configuration Overview
[How configuration works]

## Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| ...      | ...         | ...     |

## Optional Variables
| Variable | Description | Default |
|----------|-------------|---------|
| ...      | ...         | ...     |

## Environment-Specific Configuration
### Development
[Dev-specific settings]

### Staging
[Staging-specific settings]

### Production
[Production-specific settings]

## Platform-Specific Setup
### Docker
[Docker configuration]

### Kubernetes
[K8s configuration]

### Cloud Providers
[AWS/GCP/Azure specifics]

## Secrets Management
[How to handle sensitive values]

## Configuration Examples
[Complete .env.example files]

## Validation
[How to test configuration]

## Troubleshooting
[Common configuration errors]

## Migration Guide
[If updating from old config format]
```

### For API Documentation

```markdown
# API Reference

[API overview and base URL]

## ⚡ Quick Start
[Authentication + first API call]

## 📋 Table of Contents
[Sections...]

## Authentication
[How to authenticate requests]

## Rate Limiting
[Rate limit details]

## Error Handling
[Error response format and codes]

## Endpoints

### Resource Category 1

#### GET /resource
[Description]

**Request:**
```http
GET /resource?param=value
```

**Response:**
```json
{
  "data": "example"
}
```

#### POST /resource
[Description]

**Request:**
```http
POST /resource
Content-Type: application/json

{
  "field": "value"
}
```

**Response:**
```json
{
  "id": "123",
  "created": true
}
```

## SDKs / Client Libraries
[Available libraries]

## Examples
[Real-world use cases]

## Changelog
[API version history]
```

### For Tutorials/Guides

```markdown
# Tutorial Title

[What you'll learn]

## What You'll Learn
- Outcome 1
- Outcome 2
- Outcome 3

## Prerequisites
- Requirement 1
- Requirement 2

## Time Estimate
[Estimated completion time]

## 📋 Table of Contents
[Steps...]

## Step 1: [Action Verb] - [Goal]
[Detailed instructions]

```bash
command here
```

[Explanation of what happened]

## Step 2: [Action Verb] - [Goal]
[Detailed instructions]

## Step 3: [Action Verb] - [Goal]
[Detailed instructions]

## Verification
[How to verify it worked]

## Troubleshooting
[Common issues in this tutorial]

## Next Steps
- [Link to advanced tutorial]
- [Link to related guide]
- [Link to API reference]
```

### For Contributing Guides

```markdown
# Contributing Guide

[Welcome message and project values]

## 📋 Table of Contents
[Sections...]

## Code of Conduct
[Link or inline]

## Ways to Contribute
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Getting Started
### Development Environment Setup
[How to set up local dev environment]

### Project Structure
[Overview of codebase organization]

## Contribution Workflow
### 1. Fork & Clone
[Instructions]

### 2. Create Branch
[Branch naming conventions]

### 3. Make Changes
[Coding standards, testing requirements]

### 4. Commit
[Commit message format]

### 5. Submit PR
[PR template and review process]

## Coding Standards
[Style guide, linting, formatting]

## Testing Requirements
[How to run tests, coverage requirements]

## Documentation
[When and how to update docs]

## Review Process
[What to expect during review]

## Questions?
[How to get help]
```

### For Changelogs

**Requirements:**
- Must reference [Keep a Changelog](https://keepachangelog.com/) format
- Must reference [Semantic Versioning](https://semver.org/)
- Use only the six standard categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Date format must be ISO 8601: YYYY-MM-DD
- Version numbers must follow semver: MAJOR.MINOR.PATCH

**Category Usage Guide:**
- **Added**: New features or capabilities
- **Changed**: Changes to existing functionality (not bug fixes)
- **Deprecated**: Features marked for removal in future versions
- **Removed**: Features removed in this version
- **Fixed**: Bug fixes
- **Security**: Security-related improvements or fixes

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Deprecated
- Deprecated feature

### Removed
- Removed feature

### Fixed
- Bug fix description

### Security
- Security improvement

## [1.2.0] - 2024-01-15

### Added
- Feature A
- Feature B

### Fixed
- Bug fix

## [1.1.0] - 2024-01-01

[Previous versions...]
```

### For License Files

```markdown
# License

[License name]

Copyright (c) [Year] [Copyright Holder]

[Full license text]
```

---

## Anti-Patterns to Avoid

### ❌ Structure Anti-Patterns

1. **Multiple H1 headings** - Only the title should be H1
2. **Missing Table of Contents** - Required for docs >3 sections
3. **Skipping heading levels** - Don't go from H2 to H4
4. **Burying Quick Start** - Should be immediately after intro
5. **No logical flow** - Sections should build on each other
6. **Orphaned sections** - Every section should fit the narrative

### ❌ Content Anti-Patterns

1. **Wall of text** - Break into subsections, use lists, add examples
2. **No code examples** - Technical docs need concrete examples
3. **Vague instructions** - Be specific, use exact commands
4. **Missing context** - Explain why, not just what
5. **Outdated information** - Mark deprecated features clearly
6. **Inconsistent terminology** - Use terms consistently throughout

### ❌ Formatting Anti-Patterns

1. **Unspecified code blocks** - Always use language tags (```python not ```)
2. **Broken links** - Test all links before publishing
3. **Inconsistent list markers** - Use * or - consistently, not both
4. **Missing alt text** - Images should have descriptive alt text
5. **Hard-wrapped text** - Let editors handle line wrapping
6. **Mixing tabs and spaces** - Use spaces for indentation

### ❌ Appending Anti-Patterns

1. **"Updates" section at bottom** - Integrate into relevant sections
2. **Duplicate sections** - Merge with existing content
3. **No TOC update** - Always update Table of Contents
4. **Breaking narrative flow** - Maintain logical progression
5. **Contradicting existing content** - Reconcile before appending

---

## Validation Checklist

Before finalizing any markdown document, verify:

### Structure
- [ ] Only ONE H1 heading (document title)
- [ ] Quick Start section present (for actionable docs)
- [ ] Table of Contents with working anchor links
- [ ] Logical section progression
- [ ] Consistent heading hierarchy (no skipped levels)

### Content
- [ ] Clear value proposition in introduction
- [ ] Prerequisites listed before setup instructions
- [ ] Code examples include language specifications
- [ ] All commands are copy-paste ready
- [ ] Examples demonstrate real-world usage
- [ ] Troubleshooting covers common issues

### Formatting
- [ ] All code blocks specify language
- [ ] Tables are properly formatted
- [ ] Links are descriptive and working
- [ ] Lists use consistent markers
- [ ] Emphasis used appropriately
- [ ] Images have alt text

### Metadata
- [ ] License information present (if applicable)
- [ ] Author/maintainer information
- [ ] Last updated date (if using)
- [ ] Version number (if applicable)

### Accessibility
- [ ] Heading hierarchy is logical
- [ ] Links have descriptive text (no "click here")
- [ ] Images have alt text
- [ ] Tables have headers
- [ ] Color is not the only means of conveying information

### Cross-References
- [ ] Internal links use correct anchor format
- [ ] External links are current and valid
- [ ] Related documentation is linked
- [ ] API references point to correct endpoints

---

## Usage Instructions for AI Workflows

### For Document Creation

```
When creating a new .md file:
1. Detect document type (filename + content analysis)
2. Apply appropriate template from "Common Patterns by Document Type"
3. Follow "Standard Document Structure"
4. Validate against "Validation Checklist"
```

### For Document Reorganization

```
When reorganizing existing markdown:
1. Identify current document type
2. Map existing sections to "Section Organization Rules"
3. Apply appropriate template structure
4. Preserve all content (move, don't delete)
5. Update Table of Contents
6. Validate against "Validation Checklist"
```

### For Content Appending

```
When appending content to existing markdown:
1. Read existing document structure
2. Follow "Appending Content Guidelines" decision tree
3. Determine appropriate append location
4. Apply appropriate appending method
5. Update Table of Contents if adding new section
6. Validate section hierarchy
7. Check for redundancy/contradictions
```

### For Cleanup/Refactoring

```
When cleaning up markdown:
1. Check against "Anti-Patterns to Avoid"
2. Fix structure issues first
3. Then fix formatting issues
4. Then optimize content
5. Validate against "Validation Checklist"
6. Preserve all meaningful content
```

---

## Version History

- **v1.0.0** (2026-02-06): Initial comprehensive markdown formatting guide
- **v1.1.0** (2026-02-08): Fixes it removing code examples
---

## Maintenance

This guide should be updated when:
- New document patterns emerge
- Markdown standards evolve
- Team conventions change
- New anti-patterns are discovered

**Last Updated**: 2026-02-08
**Maintainer**: Documentation Team