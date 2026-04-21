# Academic Writing Patterns

Templates and guidance for writing each section type in an academic document.

## Table of Contents

1. [Introduction](#introduction)
2. [Literature Review](#literature-review)
3. [Methodology](#methodology)
4. [Results](#results)
5. [Discussion](#discussion)
6. [Conclusion](#conclusion)
7. [Paragraph Structure](#paragraph-structure)
8. [Transition Phrases](#transition-phrases)
9. [Common Pitfalls](#common-pitfalls)

---

## Introduction

The introduction answers three questions: What is the problem? Why does it matter?
What does this work contribute?

### Structure template

1. **Context** (1–2 paragraphs): Establish the broad field. Start wide, narrow quickly.
   Don't retell the entire history of the field — just enough for the reader to
   understand where the problem sits.

2. **Problem statement** (1 paragraph): State the specific problem clearly. What gap
   exists? What limitation do current approaches have? Be concrete — name the tools,
   methods, or approaches that fall short, and explain *how* they fall short.

3. **Motivation** (1 paragraph): Why does solving this problem matter? Who benefits?
   What's the practical impact? Connect the problem to real users, real scenarios.

4. **Contribution** (1 paragraph): State what this work does. Use clear, falsifiable
   statements. "This work proposes X, which achieves Y by means of Z." List
   specific contributions as bullet points if there are multiple.

5. **Organization** (1 paragraph): Briefly describe the document structure. "This
   document is organized as follows: Chapter 2 presents..."

### What makes a good introduction

- The reader should understand the problem's importance without being an expert
- Contributions should be specific and verifiable (not "we improve performance"
  but "we reduce training time by 40% on benchmark X")
- The scope should match the document type — a thesis introduction can be 3–5 pages;
  a conference paper introduction should be under 1 page

---

## Literature Review

The literature review maps what exists, identifies gaps, and positions this work
within the landscape.

### Structure template

1. **Thematic organization**: Group related works by theme, not chronologically.
   Each group gets a subsection. For example:
   - 2.1 Symbolic Regression Approaches
   - 2.2 Equality Graphs in Optimization
   - 2.3 Domain-Specific Languages for Data Analysis
   - 2.4 Existing Tools and Platforms

2. **For each group**: Start with the foundational/seminal work, then progress to
   recent developments. Show how the field evolved.

3. **Critical analysis**: Don't just summarize — compare. After presenting multiple
   works in a group, synthesize: "While approaches A and B address X, neither handles
   Y, which is essential for Z."

4. **Comparison matrix**: End with a structured comparison (table) showing how
   existing works relate to each other and to this work. Columns typically include:
   features, capabilities, limitations.

5. **Gap identification**: Close with a clear statement of what's missing — the gap
   your work fills. This paragraph bridges to the methodology.

### What makes a good literature review

- Every cited work connects to your research question — no "padding" citations
- You show you understand the works, not just read their abstracts
- The gap you identify flows naturally from the analysis
- You don't dismiss related work — you position yours relative to it

---

## Methodology

The methodology describes *what you did* and *how you did it* with enough detail
that someone could reproduce your work.

### Structure template (for engineering/CS theses)

1. **Development methodology** (1–2 pages): What process did you follow? Agile,
   Scrum, Waterfall? Why this choice? Keep this brief — it's context, not the core.

2. **Architecture and design** (main content): Describe the system's architecture.
   Use diagrams. Explain design patterns and why you chose them. This is where ER
   diagrams, architecture diagrams, and component diagrams belong.

3. **Technology stack** (1 page): List and justify each technology choice. Don't
   just list — explain *why* each was chosen over alternatives.

4. **Implementation details** (selective): Show representative code examples that
   illustrate key patterns. Don't dump entire codebases — select examples that
   demonstrate architectural decisions.

### What makes a good methodology

- Reproducible: another developer could rebuild the system from your description
- Justified: every tool/pattern choice has a reason
- Visual: architecture diagrams, ER diagrams, flowcharts
- Selective: show 3 excellent code examples rather than 20 mediocre ones

---

## Results

The results section presents data and observations without interpretation (that's
for the discussion).

### Structure template

1. **Experimental setup** (1–2 pages): Describe the environment, datasets, metrics,
   and evaluation methodology. What hardware? What datasets? How did you measure
   success?

2. **Quantitative results** (main content): Present performance metrics, benchmarks,
   comparisons with baselines. Use tables for exact numbers, charts for trends.

3. **Qualitative results** (if applicable): Screenshots, example outputs, case
   studies. For a platform, show the complete user journey.

4. **Comparative analysis**: Compare your results against existing tools/methods.
   Use a structured comparison table.

### What makes a good results section

- Data is presented before interpretation
- Tables and figures carry the weight — the text guides the reader through them
- Every metric is defined before it's used
- Negative results are included (where the system underperformed)
- Demonstration scenarios walk the reader through actual usage

---

## Discussion

The discussion interprets the results and connects them back to the research
questions. In shorter documents (conference papers, some theses), this may be merged
with results.

### Structure template

1. **Interpretation**: What do the results mean? How do they answer the research
   question?
2. **Comparison**: How do these results compare to related work?
3. **Limitations**: What couldn't you test? What are known weaknesses?
4. **Threats to validity**: What could undermine your conclusions?

---

## Conclusion

The conclusion synthesizes the entire document. No new information here — only
synthesis and forward-looking statements.

### Structure template

1. **Summary** (1–2 paragraphs): Restate the problem and what this work achieved.
   Don't copy the abstract — provide a higher-level synthesis.

2. **Key contributions** (1 paragraph): Relist contributions with the benefit of
   having demonstrated them in the results.

3. **Limitations** (1 paragraph): Honestly state what the system doesn't do or
   where it falls short.

4. **Future work** (1–2 paragraphs): Concrete, specific suggestions. Not "improve
   performance" but "integrate PySR as an alternative backend to support different
   search strategies."

---

## Paragraph Structure

Every well-formed academic paragraph follows this pattern:

1. **Topic sentence**: States the paragraph's main claim or idea
2. **Development**: Evidence, examples, reasoning that support the topic sentence
3. **Connection**: Links to the next paragraph or back to the section's theme

**Example (Portuguese, CS thesis):**

> A plataforma utiliza o padrão *Unit of Work* para garantir a integridade
> transacional de todas as operações de banco de dados. [TOPIC]
> Esse padrão encapsula um conjunto de operações em uma única transação atômica,
> assegurando que ou todas as modificações são persistidas com sucesso, ou nenhuma
> delas é aplicada. [DEVELOPMENT]
> Dessa forma, operações complexas que envolvem a criação simultânea de entidades
> — como um Job e seu Run associado — mantêm a consistência dos dados mesmo em
> cenários de falha parcial. [CONNECTION]

### Paragraph length

- **Ideal**: 4–8 sentences / 80–150 words
- **Too short** (<3 sentences): Likely could be merged with an adjacent paragraph
- **Too long** (>10 sentences): Likely covers more than one idea — split it

---

## Transition Phrases

### Portuguese academic transitions

**Continuation**: Além disso, ademais, outrossim, igualmente, da mesma forma
**Consequence**: Dessa forma, consequentemente, portanto, por conseguinte, assim
**Contrast**: No entanto, por outro lado, em contrapartida, todavia, contudo
**Exemplification**: Por exemplo, como exemplo, a título de ilustração
**Conclusion**: Em suma, em síntese, conclui-se que, por fim, finalmente
**Temporal sequence**: Primeiramente, em seguida, subsequentemente, por fim
**Emphasis**: É importante destacar, vale ressaltar, cabe salientar

### English academic transitions

**Continuation**: Furthermore, moreover, additionally, in addition
**Consequence**: Therefore, consequently, as a result, thus, hence
**Contrast**: However, on the other hand, in contrast, nevertheless, conversely
**Exemplification**: For instance, for example, as an illustration, specifically
**Conclusion**: In summary, to conclude, overall, in conclusion
**Temporal sequence**: First, subsequently, then, finally
**Emphasis**: Notably, importantly, it is worth noting

---

## Common Pitfalls

### Repetition across sections

The #1 problem in academic theses. Authors restate the same justification, the same
system description, the same motivation across multiple sections. Write each idea
once in its natural home:

- **Motivation** → Introduction
- **How existing tools fall short** → Literature Review
- **Architecture decisions** → Methodology
- **Entity descriptions** → Once, in full, then reference them

When you need to mention something already covered, use a cross-reference:
"conforme descrito na Seção 3.2" / "as described in Section 3.2."

### Unsupported claims

Every factual claim needs a citation. Common uncited claim types:
- "X is widely used" → cite a survey or usage statistics
- "Y outperforms Z" → cite the benchmark paper
- "Most approaches use..." → cite a representative sample

### Vague language

Replace vague quantifiers with specific ones:
- "significantly better" → "12% lower MSE"
- "many approaches" → "at least eight published approaches [refs]"
- "recently" → "since 2020" or "in the past five years"
- "modern technologies" → name them

### Passive voice overuse

Passive voice has its place in academic writing ("the experiment was conducted"),
but overuse makes text dense and hard to follow. Mix active and passive:
- Active: "The algorithm explores the search space using e-graphs"
- Passive: "The search space is explored using e-graphs"
- Preferred: Use active for your contributions, passive for established methods
