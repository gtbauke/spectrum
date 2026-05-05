---
name: academic-chapter-planner
description: Plan, outline, and prepare chapters for academic monographs and theses. Use this skill whenever the user asks to "plan a chapter", "outline the methodology section", "draft the results chapter", or help structure academic content before writing. This skill creates a detailed outline that captures tone and writing style instructions, reviews it with the user, and then hands off to the academic-writer skill to write the chapter.
---

# Academic Chapter Planner

This skill establishes a structured pipeline for planning and writing chapters for academic projects (theses, monographs, papers). It ensures that before any LaTeX is written, a solid outline is agreed upon, and stylistic continuity is maintained.

## Workflow

1. **Context Gathering**
   - Read relevant existing chapters (e.g., Introduction, related work), abstracts, or project documentation to understand the domain, language, tone, and specific terminology used in the project.
   - Ask the user for the specific goals, main arguments, and key figures/tables/results they want to include in the target chapter.

2. **Outline Creation**
   - Generate a detailed, hierarchical outline for the chapter in a Markdown file or Artifact.
   - **Crucial Step:** Include a dedicated section in the outline titled `Style and Tone Instructions`. This section must explicitly state the academic tone, specific terminology, formatting preferences (e.g., ABNT standards, LaTeX macros), and language (e.g., Formal Brazilian Portuguese) based on the context gathered in step 1. This ensures the `academic-writer` maintains consistency.

3. **User Review**
   - Present the outline to the user for review.
   - Actively solicit feedback and iterate on the outline until the user explicitly approves it.

4. **Handoff to Academic Writer**
   - Once the user approves the outline, explicitly transition to using the `academic-writer` skill to generate the full LaTeX/TeX chapter. Provide the approved outline and the `Style and Tone Instructions` as the primary inputs for the drafting phase.

## Output Format for the Outline

Use the following structure for the outline document to ensure smooth handoff:

```markdown
# Outline: [Chapter Name]

## 1. Style and Tone Instructions (for academic-writer)
- **Language:** [e.g., Formal Brazilian Portuguese]
- **Voice:** [e.g., Objective academic tone, third-person]
- **Terminology:** [List specific domain terms, project names, or acronyms]
- **Formatting:** [e.g., ABNT citations, specific LaTeX environments]

## 2. Chapter Structure
### 2.1 [Section Title]
- Main point 1
- Main point 2
  - Sub-detail
- *Proposed Visuals:* [Describe any figures, TikZ diagrams, or tables needed]

### 2.2 [Section Title]
...
```
