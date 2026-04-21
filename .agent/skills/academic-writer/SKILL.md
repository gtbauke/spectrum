---
name: academic-writer
description: >
  Write and edit academic documents — papers, theses, monographies, and dissertations.
  Produces publication-ready LaTeX, TeX, and Markdown content including full sections,
  paragraphs, tables, TikZ diagrams, generated images, captions, labels, and BibTeX
  references. Use this skill whenever the user asks to write, draft, expand, rewrite,
  or edit content in an academic paper, thesis, or monograph. Also trigger when the
  user wants to create tables, figures, diagrams, or any visual element for a scientific
  document. If the user says "write the results chapter," "add a comparison table,"
  "create a diagram showing X," "fix the issues from the review," or "expand this
  section" — this is a writing task and this skill applies. This skill complements the
  academic-reviewer skill: the reviewer identifies what to improve, and this skill
  executes the improvements.
---

# Academic Writer

Write, edit, and expand academic documents. Produce publication-ready content in LaTeX
or Markdown with proper structure, cross-references, citations, and visual elements.

## Overview

Academic writing is a craft with specific structural patterns that differ by document
type and by section within a document. An introduction persuades the reader that a
problem matters. A literature review maps the existing landscape. A methodology section
must be precise enough for reproduction. A results section must let data speak before
interpretation. This skill helps you produce content that fits these conventions while
matching the author's existing voice and the document's formatting standards.

This skill complements the **academic-reviewer** skill. The reviewer reads a document
and produces a structured critique. This writer takes instructions — which may come
from a review, from the user directly, or from your own analysis — and produces the
actual content. The two skills form a review–write loop: review → identify gaps →
write to fill them → review again.

## Workflow

### Step 1: Map the project

Before writing anything, understand the project's structure. Academic documents are
rarely a single file.

**For LaTeX projects:**
1. Find the main `.tex` file (the one with `\documentclass` and `\begin{document}`)
2. Follow all `\input{}` and `\include{}` commands to map every chapter/section file
3. Note the document class and packages — these determine available commands
4. Read the `.bib` file(s) to understand existing references
5. Check for custom commands (`\newcommand`) that the author uses
6. Identify the formatting standard (ABNT, etc.) from the document class

**For Markdown projects:**
1. Find the config file (`_toc.yml`, `book.toml`, `_bookdown.yml`, `mkdocs.yml`)
2. Map the chapter ordering and file structure
3. Note any custom shortcodes, macros, or extensions in use

Build a mental model of:
- What exists (completed chapters/sections)
- What's missing (empty files, commented-out includes, TODOs)
- What style the author uses (voice, terminology, level of formality)

### Step 2: Understand the task

The user's request falls into one of several categories. Identify which:

| Task type | Description | Example request |
|---|---|---|
| **New section** | Write a section or chapter from scratch | "Write the results chapter" |
| **Expand** | Add depth to thin content | "Expand the IQL section with more examples" |
| **Rewrite** | Improve existing content without changing meaning | "Rewrite section 3.2 to be clearer" |
| **Visual element** | Create a table, figure, or diagram | "Add a comparison table of SR tools" |
| **Review fix** | Address specific issues from a review | "Fix the issues flagged in the review" |
| **Structural** | Reorganize, split, or merge sections | "Split the methodology into two chapters" |

For **review-fix** tasks, read the review file first (typically in a `reviews/`
directory as produced by the academic-reviewer skill). Extract the specific, actionable
suggestions and prioritize them by the review's Priority Actions ranking.

### Step 3: Analyze the voice

Academic writing must be consistent. Before writing new content, read 2–3 existing
sections to internalize the author's patterns:

- **Sentence length**: Does the author favor long, clause-heavy sentences or shorter,
  punchier ones?
- **Person and voice**: First person plural ("nós propomos"), impersonal ("propõe-se"),
  or passive ("foi proposto")?
- **Terminology**: What terms does the author use for key concepts? Use the same ones,
  not synonyms.
- **Paragraph structure**: Does the author use topic sentences? How long are paragraphs?
- **Transition style**: How does the author connect sections? ("Dessa forma," "Além
  disso," "Nesse contexto,")
- **Language**: Write in the document's language. If the thesis is in Portuguese, write
  in Portuguese. If sections are bilingual (abstract in both languages), match each.

The goal is that a reader cannot tell where the original author stopped and you began.

### Step 4: Write the content

Follow the appropriate pattern for the content type. The `references/` directory
contains detailed guidance — consult the relevant file:

- **Sections and paragraphs** → `references/writing_patterns.md`
- **LaTeX environments, commands, ABNT formatting** → `references/latex_patterns.md`
- **Tables, figures, TikZ diagrams** → `references/visual_elements.md`

#### General writing principles

**Every paragraph earns its place.** Each paragraph should advance exactly one idea.
Start with the claim or topic, develop it with evidence or reasoning, and connect it
to what comes next. If a paragraph doesn't add something new, cut it.

**Avoid empty repetition.** The most common flaw in academic writing is restating the
same point across sections. Write each idea once, in its natural home, then reference
it elsewhere: "conforme descrito na Seção X" / "as discussed in Section X."

**Be specific over general.** "The system uses modern technologies" says nothing.
"The system uses FastAPI 0.111 with async SQLAlchemy 2.0 for non-blocking database
access" informs the reader.

**Support claims with evidence.** Every non-trivial factual claim needs a citation.
If you introduce a claim and aren't sure of a source, flag it with a TODO comment
rather than leaving it uncited:
```latex
% TODO: find citation for this claim
```

#### Labels and cross-references

Every numbered element (figure, table, code listing, equation, section) gets a label.
Follow a consistent naming convention based on what the project already uses. Common
patterns:

```latex
\label{fig:entity_diagram}     % figures
\label{tab:comparison}          % tables
\label{code:user_domain}        % code listings
\label{eq:loss_function}        % equations
\label{sec:results}             % sections
\label{ch:methodology}          % chapters
```

Always reference elements before they appear: "A Tabela \ref{tab:comparison}
apresenta..." — then the table follows. Never place a figure or table without
referencing it in the body text.

#### Captions

Captions are standalone summaries. A reader should understand what a figure or table
shows from the caption alone, without needing the surrounding text.

**Weak**: "Tabela 1: Comparação de ferramentas"
**Strong**: "Tabela 1: Comparação de funcionalidades entre as ferramentas de regressão
simbólica TuringBot, HeuristicLab e Spectrum, abrangendo execução remota, suporte a
DSL e código aberto."

For ABNT-formatted documents, captions go **above** figures and tables
(`\caption` before `\includegraphics` or table content).

### Step 5: Integrate into the project

After writing the content:

1. **Place the content** in the correct file. For new chapters, create a new `.tex`
   file and add the corresponding `\include{}` or `\input{}` in the main file.

2. **Add citations** to the `.bib` file. When introducing new references, create
   properly formatted BibTeX entries. Use the existing entries as style templates:
   ```bibtex
   @article{author2024title,
     author  = {Last, First and Last, First},
     title   = {Full Title of the Paper},
     journal = {Journal Name},
     year    = {2024},
     volume  = {10},
     number  = {2},
     pages   = {123--145},
     doi     = {10.1234/example}
   }
   ```

3. **Update cross-references** if you added sections that other parts reference.
   Check that `\ref{}` targets exist and that section numbering hasn't been disrupted.

4. **Verify float order**. If you added figures or tables, make sure the reference
   in the text appears before the float. Use `[htbp]` placement specifiers to keep
   floats near their references.

### Step 6: Compile and verify

After writing, compile the LaTeX project to catch errors early. Run the appropriate
compilation command from the project root:

```bash
# For projects using biber (biblatex):
latexmk -pdf -interaction=nonstopmode main.tex

# Or manually:
pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
```

Check the compilation output for:
- **Errors** (lines starting with `!`): Fix these before delivering — they prevent
  PDF generation. Common causes: unmatched braces, undefined commands, missing
  packages.
- **Warnings** (`LaTeX Warning`): Address "undefined reference" and "citation
  undefined" warnings. "Overfull hbox" warnings are less critical but worth checking
  if they exceed 10pt.
- **Missing references**: Run compilation twice (or use `latexmk`) to resolve
  cross-references and citations.

If `latexmk` or `pdflatex` are not available in the environment, flag this to the
user and list a manual quality checklist instead.

### Step 7: Quality checklist

Before delivering, verify:

- [ ] Content is in the document's language
- [ ] Voice matches the author's existing style
- [ ] Every figure/table has a caption and a label
- [ ] Every figure/table is referenced in the body text
- [ ] Every factual claim has a citation (or a TODO flag)
- [ ] No orphaned labels (labels that nothing references)
- [ ] Float placement specifiers are present (`[htbp]`)
- [ ] New `.bib` entries are syntactically correct
- [ ] LaTeX compiles without errors
- [ ] No content from other sections is duplicated

## Creating visual elements

### Tables

Tables are often the most effective way to present structured comparisons. When a user
asks for a table, or when your analysis suggests one would clarify a point:

1. Identify the dimensions (what goes in rows vs. columns)
2. Choose the right column types (`l`, `c`, `r`, `p{width}`)
3. Use `\toprule`, `\midrule`, `\bottomrule` from the `booktabs` package when
   available — avoid `\hline` and vertical rules for cleaner aesthetics
4. Make sure the table fits the page width. Use `\resizebox` or `tabularx` if needed

See `references/visual_elements.md` for complete table templates.

### Diagrams

TikZ is the preferred approach for all diagrams — it keeps everything in LaTeX,
produces resolution-independent output, and is maintainable alongside the text.

| Diagram type | Approach | Notes |
|---|---|---|
| Flowcharts, pipelines | TikZ | Use `positioning` and `arrows.meta` libraries |
| ER / entity diagrams | TikZ | Use `rectangle split` for table-style nodes |
| Architecture diagrams | TikZ | Use layered layouts with `on background layer` |
| Syntax trees | `forest` package | Built on TikZ, optimized for trees |
| Data-driven charts | `pgfplots` | Integrates directly with TikZ |

Match the style of existing diagrams in the project (colors, node shapes, arrow
styles). See `references/visual_elements.md` for TikZ templates.

**Fallback**: If TikZ cannot reasonably express the diagram (e.g., a conceptual
illustration requiring complex visual elements, or a diagram with 50+ nodes where
manual positioning is impractical), use the `generate_image` tool as a fallback.
Save generated images to the project's images directory with descriptive filenames:
`iql_execution_pipeline.png`, not `diagram1.png`.

### Figures from screenshots or photos

If figures need to be included from external sources, place them in the project's
images directory and create proper figure environments:

```latex
\begin{figure}[htbp]
    \caption{Descriptive caption that stands alone}
    \centering
    \includegraphics[width=0.8\textwidth]{images/descriptive_name.png}
    \label{fig:descriptive_name}
\end{figure}
```

## Working with reviews

When the user asks you to address issues from a review (produced by the
academic-reviewer skill or by hand):

1. Read the review file completely
2. Extract all actionable suggestions into a checklist
3. Prioritize using the review's "Priority Actions" if available
4. Work through suggestions in priority order
5. For each fix, explain briefly what you changed and why
6. Track completed fixes — this helps the user see progress

The writer does not re-review the document. If the user wants verification that
the fixes addressed the reviewer's concerns, they should run the reviewer skill again.

## Reference files

The `references/` directory contains detailed patterns and templates. Read the
relevant file when you need specifics:

- **`references/writing_patterns.md`** — Templates for each section type (introduction,
  lit review, methodology, results, conclusion), paragraph structures, transition
  phrases, and common pitfalls. Read this when writing new sections or expanding thin
  content.

- **`references/latex_patterns.md`** — LaTeX environments, formatting commands, ABNT
  conventions, float management, listings configuration, and common package usage.
  Read this when creating LaTeX-specific elements or debugging formatting.

- **`references/visual_elements.md`** — Table templates (booktabs, tabularx, longtable),
  TikZ diagram patterns, figure environments, subfigures, and best practices for
  academic visuals. Read this when creating tables, diagrams, or figures.
