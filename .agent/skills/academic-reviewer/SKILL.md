---
name: academic-reviewer
description: >
  Review and analyze academic projects — papers, theses, monographies, and dissertations.
  Provides structured improvement suggestions on general structure, writing quality, and
  figures/visualization. Use this skill whenever the user asks to review, analyze, critique,
  give feedback on, or improve an academic paper, thesis, monograph, or dissertation. Also
  trigger when the user shares LaTeX (.tex), Markdown (.md), or PDF files and asks for
  writing feedback, structural analysis, or wants to know what can be improved. Even if
  the user just says "take a look at my paper" or "what do you think of my thesis" — that's
  a review request and this skill applies.
---

# Academic Project Reviewer

Review academic projects (papers, theses, monographies) and produce a structured Markdown
report with actionable improvement suggestions.

## Overview

Academic writing has specific conventions that vary by document type. A journal paper needs
tight, focused argumentation. A thesis requires methodological rigor and comprehensive
literature coverage. A monograph demands narrative coherence across chapters. This skill
helps you identify the document type, apply the right evaluation lens, and produce feedback
the author can act on immediately.

## Workflow

### Step 1: Gather the source material

The user may provide files in several formats. Read them using the appropriate method:

**LaTeX / TeX files (`.tex`, `.bib`, `.sty`)**
Read directly with `view_file`. LaTeX projects often span multiple files — look for
`\input{}` and `\include{}` commands in the main `.tex` file and follow them to read
the full document. Also read `.bib` files for reference analysis.

**Markdown files (`.md`)**
Read directly with `view_file`. If the project uses a static site generator or book
framework (like mdBook, Jupyter Book, or Bookdown), check for a config file
(`_bookdown.yml`, `_toc.yml`, `book.toml`) to understand chapter ordering.

**PDF files (`.pdf`)**
Use the bundled extraction script to get the text content:
```bash
python <skill-path>/scripts/extract_pdf.py <path_to_pdf> --with-images
```
The `--with-images` flag includes a summary of embedded images (count, dimensions,
page locations) which is essential for the figures review section. The output includes
page numbers so you can reference specific locations in your review.

If the PDF is very large (>100 pages, common for theses), extract in stages and focus
your review on the most impactful sections first — typically the abstract, introduction,
methodology, and conclusion.

### Step 2: Identify the document type

Before reviewing, determine what kind of academic work this is. The document type
changes what you emphasize:

| Type | Key characteristics | Review emphasis |
|---|---|---|
| **Journal paper** | 8–30 pages, tight scope, single research question | Argument flow, novelty claims, conciseness |
| **Conference paper** | 4–12 pages, strict page limits | Space efficiency, key contribution clarity |
| **Thesis / Dissertation** | 50–300+ pages, chapters, committee-oriented | Methodology rigor, literature depth, internal consistency |
| **Monograph** | Book-length, narrative arc | Chapter cohesion, audience engagement, argumentative throughline |

Look for signals: page count, presence of `\chapter{}` vs `\section{}`, acknowledgments
mentioning advisors or committees, submission formatting guidelines, abstract length.

If you can't tell, ask the user — but make your best guess first.

### Step 3: Perform the review

Analyze the document across four dimensions. For each dimension, identify both strengths
and areas for improvement. Concrete, specific feedback is far more useful than generic
advice — reference specific sections, paragraphs, or page numbers whenever possible.

#### Dimension 1: General Structure

Evaluate the overall organization and logical flow of the document.

Consider:
- Does the document follow the expected structure for its type?
  - Papers: Abstract → Introduction → Related Work → Method → Results → Discussion → Conclusion
  - Theses: Front matter → Introduction → Literature Review → Methodology → Results → Discussion → Conclusion → References → Appendices
  - Monographs: varies, but should have a clear argumentative arc
- Is there a logical progression from problem statement to contribution?
- Are sections appropriately sized relative to their importance?
- Does the introduction clearly state the research question, motivation, and contribution?
- Does the conclusion actually conclude (summarize findings, state limitations, suggest future work)?
- Are there missing sections that the document type conventionally expects?
- Is there unnecessary repetition between sections?

#### Dimension 2: Writing Quality

Evaluate clarity, precision, and adherence to academic writing conventions.

Consider:
- **Clarity**: Are sentences easy to parse on first read? Are there ambiguous pronouns,
  dangling modifiers, or garden-path sentences?
- **Precision**: Are claims appropriately hedged? Does the author distinguish between
  correlation and causation? Are terms defined before use?
- **Tone**: Is the register consistently academic? Watch for casual language, marketing
  speak ("groundbreaking", "revolutionary"), or unsupported superlatives.
- **Transitions**: Do paragraphs and sections connect logically? Are there abrupt topic
  shifts?
- **Paragraph structure**: Does each paragraph have a clear topic sentence and develop
  a single idea?
- **Citations**: Are claims supported by references? Are there passages that make factual
  claims without citation? Is self-citation proportionate?
- **Abstract quality**: Does the abstract concisely state the problem, method, key results,
  and main conclusion? (Many abstracts fail to include results.)

For non-English papers, be sensitive to the conventions of the target language's academic
tradition — don't impose anglophone norms on, say, a Brazilian Portuguese thesis that
follows ABNT formatting conventions.

#### Dimension 3: Figures & Visualization

Evaluate the quality and effectiveness of all visual elements — figures, tables, charts,
diagrams, and equations.

Consider:
- **Captions**: Is every figure and table captioned? Are captions self-contained — could
  a reader understand the figure from the caption alone, without reading the surrounding
  text? Captions should describe what is shown, not just label it.
  - Weak: "Figure 3: Results"
  - Strong: "Figure 3: Classification accuracy across all five datasets, showing that
    method X outperforms baselines by 4-7% on average."
- **Labels**: Are axes labeled with units? Are legend entries descriptive? Are font sizes
  readable?
- **References in text**: Is every figure/table referenced in the body text before or
  near its placement? Orphaned figures (never referenced) are a red flag.
- **Placement**: Are figures placed near their first reference in the text? LaTeX float
  placement can cause figures to drift — flag cases where a figure is referenced on
  page 5 but appears on page 8.
- **Numbering**: Are figures and tables numbered sequentially? Are there gaps or
  duplicates?
- **Necessity**: Does every figure earn its space? Could any be consolidated, moved to
  an appendix, or removed entirely?
- **Consistency**: Do all figures use the same visual style (color scheme, font, line
  weights)?
- **Tables**: Are tables well-formatted? Do they use horizontal rules appropriately
  (typically top, header-separator, bottom — not vertical rules or full grids)?
  Are numeric columns right-aligned?

When reviewing from PDF extraction, cross-reference the image metadata (dimensions,
page numbers) with the text content to assess placement relative to first mention.

#### Dimension 4: Technical Content (when applicable)

If the document describes research methodology or technical work, briefly assess:
- Is the methodology described in enough detail to be reproducible?
- Are experimental conditions controlled and clearly stated?
- Do the results actually support the claims made in the discussion?
- Are limitations honestly acknowledged?

This is not about judging the science itself (you're not a domain expert) — it's about
whether the *presentation* of the methodology is clear and complete.

### Step 4: Write the review report

Create the review as a Markdown file. Save it in a `reviews/` directory relative to
the source file's location:

```
<source_file_directory>/
├── reviews/
│   └── review_<source_filename>_<YYYY-MM-DD>.md
└── <source_file>
```

For example, if the user's thesis is at `/home/user/thesis/main.tex`, the review goes to
`/home/user/thesis/reviews/review_main_2025-01-15.md`.

Use the following template as your review structure. Adapt section depth and emphasis
based on the document type and what you found — don't force content into sections where
there's nothing meaningful to say.

---

```markdown
# Academic Review: [Document Title]

> **Document type**: [Paper / Thesis / Monograph]
> **Reviewed file(s)**: [filenames]
> **Review date**: [YYYY-MM-DD]

## Executive Summary

[2-3 paragraph overview: what the document does well, the most important issues to
address, and an overall impression of completeness/readiness. This should be the first
thing the author reads and should give them a clear sense of priority.]

## Structure

### Strengths
- [specific observations]

### Suggestions
- [specific, actionable suggestions with section/page references]

## Writing

### Strengths
- [specific observations]

### Suggestions
- [specific, actionable suggestions with examples from the text]

## Figures & Visualization

### Strengths
- [specific observations]

### Suggestions
- [specific suggestions referencing figure numbers or page locations]

## Technical Presentation

### Strengths
- [specific observations]

### Suggestions
- [specific suggestions]

## Priority Actions

A ranked list of the 3-5 most impactful changes the author should make first:

1. [Highest impact suggestion]
2. [Second highest]
3. ...

## Detailed Notes

[Optional: line-by-line or section-by-section notes for minor issues — typos, formatting
inconsistencies, awkward phrases. Use a table or checklist format for scanability.]

| Location | Issue | Suggestion |
|---|---|---|
| Section 2.1, p.4 | "This method is very good" | Replace with specific claim: "This method reduces error by 12%" |
| Figure 5 caption | Missing units on y-axis | Add "Accuracy (%)" label |
```

---

## Guidelines for effective reviews

**Be specific, not vague.** "The writing needs improvement" is useless. "Section 3.2 uses
passive voice in 8 of 12 sentences, making it hard to identify who performed each
experiment" is actionable.

**Balance criticism with recognition.** Academic writing is hard work. Start each section
by noting what's done well before identifying issues. This isn't about being nice — it's
about being credible. A review that only lists problems reads as hostile and gets ignored.

**Prioritize ruthlessly.** A thesis might have 50 issues. The author can realistically fix
10 before their deadline. Put the highest-impact suggestions in the Priority Actions
section so they know where to focus.

**Adapt your depth to the document's maturity.** A rough first draft needs big-picture
structural feedback, not comma corrections. A near-final version benefits from detailed
line edits. Ask the user what stage they're at if it's not obvious.

**Respect disciplinary conventions.** Computer science papers look different from history
monographs. STEM theses have different norms than humanities dissertations. Don't flag
something as "wrong" if it's actually a disciplinary convention you're not familiar
with — phrase it as a question instead.
