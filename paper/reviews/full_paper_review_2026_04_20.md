# Academic Review: Interface Web para Regressão Simbólica

> **Document type**: Trabalho de Conclusão de Curso (Undergraduate Thesis / Monograph)
> **Reviewed file(s)**: `symbolic_regression_web_interface.tex`, `chapters/introduction.tex`, `chapters/literature_review.tex`, `chapters/methodology.tex`, `chapters/platform.tex`, `chapters/query_language.tex`, `chapters/conclusion.tex`, `references.bib`
> **Review date**: 2026-04-20

---

## Executive Summary

This is a well-scoped undergraduate thesis that proposes Spectrum, a web platform for symbolic regression, featuring a novel domain-specific query language (IQL). The project itself is impressive in breadth — spanning a full-stack application with React, FastAPI, RabbitMQ workers, and a custom DSL — and the paper does a solid job of walking the reader through the architecture and design decisions. The use of DDD, Unit of Work, and the Ports and Adapters pattern is well-motivated and effectively communicated through code examples.

**The most critical issue is the absence of a Results chapter.** The `results.tex` file is empty (commented out in `main.tex`), meaning the thesis has no empirical evaluation, no benchmarks, no user study, and no discussion connecting the implementation back to the objectives stated in the introduction. For a TCC, this is a significant gap that an evaluation committee will almost certainly flag. Without results, the paper reads as an extended technical report rather than a research monograph.

Beyond the missing chapter, the paper suffers from **structural imbalances**: the Platform chapter (~900 lines of LaTeX) dwarfs all other chapters combined, and the IQL chapter (~60 lines) is too thin given that IQL is presented as the project's "great differential." The writing is generally clear but contains notable repetition, some grammatical issues, and occasional inconsistencies in terminology. Figures are abundant and well-placed, though many captions could be more self-contained.

Overall, the core content is strong. Addressing the missing results and rebalancing chapter lengths would significantly raise the quality of this thesis.

---

## Structure

### Strengths
- **Logical progression**: The document follows a conventional and effective structure — context → literature → methodology → platform → DSL → conclusion — making it easy to follow the narrative arc from problem to solution.
- **Well-defined objectives**: Section 1.2 clearly enumerates the platform's functional goals as a bullet list, giving the reader concrete expectations for what will be demonstrated.
- **DDD motivation is well-threaded**: The choice of Domain-Driven Design is introduced in the methodology and consistently referenced throughout the platform chapter, providing architectural coherence.
- **User Stories bridge theory and practice**: Using User Stories (Section 4.2) to translate functional requirements into actionable scenarios is a well-chosen technique that grounds the platform description.

### Suggestions

1. **The Results chapter is entirely missing.** `results.tex` contains only a chapter heading, and the `\include{chapters/results}` is commented out in the main file. The introduction (Section 1.4) explicitly promises chapters on results (Chapter 6) and conclusion (Chapter 7), so the reader expects to find empirical data. At minimum, this chapter should include:
   - A demonstration scenario showing the full pipeline (upload → train → query via IQL → analyze results)
   - Performance metrics: training times for sample datasets, IQL query execution times
   - A qualitative comparison table: Spectrum vs. TuringBot vs. HeuristicLab (feature parity)
   - A brief usability assessment, even if informal

2. **The chapter numbering in Section 1.4 is now incorrect.** The "Organização deste trabalho" section references Chapters 2–7, but with the Results chapter commented out, only 6 chapters exist. Update this section to reflect the actual structure.

3. **Massive imbalance between Platform (~900 lines) and IQL (~60 lines).** The IQL is presented in the abstract and introduction as the "grande diferencial" of the platform, yet it receives only ~2 pages of treatment. By contrast, the platform chapter exhaustively documents every entity's domain code. Consider:
   - Moving the formal grammar into a proper BNF/EBNF definition
   - Adding a section on the tokenizer design with examples of token streams
   - Expanding the Pratt Parsing explanation with a worked example
   - Adding a section on error handling and reporting in IQL
   - Including a comparison table between IQL and SQL constructs

4. **The Methodology chapter (Ch. 3) conflates methodology with architecture.** The chapter starts with development methodology (Scrum, DDD) but then transitions into deep architectural descriptions of the storage layer, repository patterns, and Unit of Work. Consider splitting this into:
   - Chapter 3: *Materiais e Métodos* — development tools, methodology, project structure (shorter)
   - Chapter 4: *Arquitetura* — architectural patterns, abstractions, database design

5. **The Literature Review lacks a comparison matrix.** Section 2.6 mentions TuringBot, HeuristicLab, and rEGGression but doesn't provide a structured comparison. A table comparing features (web vs. desktop, remote execution, DSL support, pipeline support, open source) would strengthen the justification section.

6. **The conclusion section on limitations is strong but could be better structured.** Currently it's three dense paragraphs. Breaking it into subsections (e.g., "Resilience", "IQL Expansion", "Algorithm Support") would improve readability.

---

## Writing

### Strengths
- **Consistent academic register**: The text maintains a formal, academic tone throughout, appropriate for a Brazilian ABNT-formatted thesis.
- **Good use of citations**: Claims about symbolic regression, genetic algorithms, and e-graphs are well-supported by relevant references.
- **Clear abstracts**: Both the Portuguese resumo and English abstract are well-structured, covering problem, method, contribution, and conclusion.
- **Technical terms are introduced before use**: Terms like "e-graph," "e-node," "e-class," "saturação de igualdade" are all defined upon first appearance.

### Suggestions

1. **Heavy repetition across chapters.** Several paragraphs essentially restate the same information. For example:
   - The phrase "permitindo que os usuários acessem e analisem os resultados..." appears (with minor variations) at least 5 times in the Platform chapter.
   - The justification for remote execution ("máquinas com baixo poder computacional") is repeated in the abstract, introduction, and platform chapter.
   - The description of what Profiles, Jobs, and Models do is repeated nearly verbatim between sections. Each entity's subsection in Ch. 4 restates relationships already established in the overview.

   **Recommendation:** Write each concept once with full detail, then use brief forward/backward references ("conforme descrito na Seção X") in subsequent mentions.

2. **Bullet/dash lists in LaTeX are inconsistent.** In `introduction.tex` (Section 1.2) and `literature_review.tex` (Section 2.6.1), plain dashes (`-`) are used instead of `\begin{itemize}` environments. This likely produces misformatted output in the compiled PDF. Use proper LaTeX list environments throughout.

3. **Subject-verb agreement errors:**
   - Introduction, line 6: "outras técnicas de IA, como a regressão simbólica, **tem** ganhado destaque" → should be "**têm** ganhado" (plural subject).
   - Lit. Review, line 102: "até que nenhuma" → "até que **nenhuma**" appears to be a typo for "nenhuma" (should be fine, but double-check).

4. **TOML listing uses JavaScript comment syntax.** In `methodology.tex`, the TOML code listing (Code 2) uses `//` for comments (e.g., `// Servidor`, `// Pacote Core`). TOML uses `#` for comments. This is misleading within a code listing that defines `\lstdefinelanguage{Toml}` with `#` comments.

5. **The epigraph quote attribution is dubious.** The quote attributed to Albert Einstein ("Computadores são incrivelmente rápidos...") is a well-known misattribution. Consider either finding a verified attribution or replacing it with a genuine quote.

6. **Code listing captions could be more descriptive.** Several captions are generic:
   - "Bibliotecas utilizadas no front-end e suas versões" → specifies *what* but not *why*. Consider: "Dependências do front-end React, incluindo bibliotecas de estado, roteamento e visualização."
   - Two code listings share the same caption text: "Classe de domínio que define um bloco de consulta em linguagem IQL" (Codes for InferenceBlock and MarkdownBlock).

7. **Inconsistent use of English terms.** Some terms appear in English without italics or explanation:
   - "pipelines" (used freely), "upload" (used freely), "soft delete" (explained inline)
   - Consider using `\textit{}` consistently for English loanwords on first use, then dropping the formatting.

8. **Long paragraphs in the Platform chapter.** Several paragraphs in Sections 4.5–4.7 exceed 10 lines of dense text. For readability, break them into shorter paragraphs — especially the Workers subsections (training, validation, IQL queries), where each paragraph covers multiple sequential steps.

---

## Figures & Visualization

### Strengths
- **Abundant visual documentation**: The paper includes 17+ figures spanning diagrams, code listings, and application screenshots, providing strong visual evidence of the implemented platform.
- **TikZ entity diagram (Fig. entity_diagram)**: The hand-crafted TikZ ER diagram is a standout — it's clean, well-labeled, and directly compilable from the source, making it maintainable and resolution-independent.
- **Screenshots cover the full user flow**: From login to model metrics, the screenshots demonstrate every major UI feature, giving the reader a comprehensive understanding of the platform.
- **Figures are consistently referenced before appearance**: Every figure is referenced in the text before its placement, following good academic practice.

### Suggestions

1. **Captions are too terse and not self-contained.** Academic figure captions should allow the reader to understand the figure without reading the surrounding text. Several captions need expansion:

   | Figure | Current Caption | Suggested Improvement |
   |---|---|---|
   | Fig. 1 (AST) | "Exemplo de uma AST para a expressão $log(x/2) + 3x$" | Add: "Círculos representam operações (nós não terminais) e quadrados representam variáveis e constantes (nós terminais)." |
   | Fig. editor_screen | "Tela inicial do Editor da plataforma Spectrum" | Add: "A interface apresenta uma barra de atividades à esquerda, uma barra lateral para navegação de Profiles/Datasets, e uma área central com abas para espaços de trabalho." |
   | Fig. models_section | "Seção de modelos de uma Profile..." | The caption is nearly 3 lines and essentially repeats the subsection text. Trim to essentials. |

2. **Some figure captions duplicate the surrounding text verbatim.** Figures for add_job, models_section, and iql_results have captions that are nearly identical to the paragraph preceding them. Captions should complement, not copy, the body text.

3. **Missing `[ht]` or `[htbp]` float specifiers on several figures.** Figures in `literature_review.tex` (crossover, mutation, e-graph, exhaustive) lack explicit placement hints, which can cause LaTeX to float them far from their references. Add `[htbp]` to all `\begin{figure}` environments for better placement control.

4. **The entity diagram caption is placed below the TikZ figure.** In ABNT formatting, captions are placed above figures (`\caption` before `\includegraphics`). Several figures in the platform chapter correctly use this convention (e.g., the AST figures in Ch. 2), but the TikZ diagram and some screenshots place the caption after. Make this consistent throughout.

   > [!NOTE]
   > ABNT NBR 14724 specifies that figure captions go *above* the figure (using `\caption` before the content). Check your compiled output to verify compliance across all figures.

5. **No figure for the IQL execution pipeline.** Chapter 5 describes a multi-stage process (tokenization → Pratt parsing → AST → rEGGression calls → results), but provides no diagram. A flowchart or pipeline diagram here would significantly clarify the execution model for the reader.

6. **Image naming typo**: The signup screenshot is named `spctrum_signup.png` (missing 'e'). While this doesn't affect the compiled output, it suggests the file may have been hastily added. Consider renaming for consistency (`spectrum_signup.png`).

---

## Technical Presentation

### Strengths
- **Excellent architecture documentation**: The paper thoroughly documents the Ports and Adapters pattern, showing both the protocol definition (`FileStorage`) and a concrete implementation (`LocalStorage`). This clearly demonstrates understanding of the architectural pattern.
- **Code examples are well-chosen**: Rather than dumping entire codebases, the paper selects representative examples that illustrate patterns (base entities, repository protocols, Unit of Work) — this is effective pedagogy.
- **Worker architecture is well-explained**: The training → validation → IQL execution pipeline through RabbitMQ is clearly described, with attention to why tasks run asynchronously and how results flow back.
- **Security considerations are mentioned**: JWT in HttpOnly cookies, path traversal protection, soft deletes — these show awareness of production concerns.

### Suggestions

1. **The IQL formal grammar needs rigor.** The grammar in Chapter 5 is presented in pseudocode rather than a proper BNF/EBNF format. For a DSL that's positioned as the paper's main contribution, the formal grammar should be precisely defined. Consider adding:
   - A complete EBNF or PEG grammar specification
   - The set of valid field names (expression, error, size, dl, fitness, etc.)
   - How patterns (`PATTERN IS LIKE`) are parsed — what constitutes a valid pattern?
   - How the `FROM` clause resolves model names to e-graph instances

2. **No mention of testing.** The paper doesn't discuss testing methodology despite having `pytest` and `ruff` in dev dependencies. For a software engineering thesis, at least a brief mention of unit testing strategy, test coverage, or CI/CD would strengthen the technical credibility.

3. **The `results.tex` file is empty.** As noted in the Structure section, this is the most significant gap. For the technical evaluation, the results chapter should include at minimum:
   - Benchmark datasets used (Feynman? SRBench? Custom?)
   - Training time comparisons
   - IQL query execution benchmarks
   - Comparison of e-graph size before and after saturation
   - Demonstration that IQL queries return correct results

4. **The Data Mapper pattern is mentioned but not shown.** The methodology chapter mentions Data Mappers as a core pattern ("ORM models MUST NOT contain transformation logic. Use dedicated Mapper classes"), but no Mapper code example appears in the paper. Since this is a central architectural decision, showing one Mapper would strengthen the presentation.

5. **Missing discussion of scalability.** The paper mentions that "múltiplos workers podem ser adicionados conforme a demanda" but doesn't discuss:
   - How many concurrent workers the system supports
   - Memory consumption of loading e-graphs for large models
   - Whether the SSE streaming approach scales with many simultaneous users

---

## Priority Actions

A ranked list of the most impactful changes to make first:

1. **Write the Results chapter.** This is non-negotiable for a TCC defense. Include at least one complete demonstration scenario, performance data for training and IQL queries, and a feature comparison table with existing tools. Even a small-scale evaluation dramatically strengthens the thesis.

2. **Expand the IQL chapter (Ch. 5) significantly.** Double its current length at minimum. Include a formal EBNF grammar, a worked tokenization/parsing example, error handling behavior, and a richer set of query examples. This is your key technical contribution — it deserves proportional depth.

3. **Reduce repetition in the Platform chapter (Ch. 4).** The chapter can be shortened by 20–30% by eliminating repeated descriptions of entity relationships and condensing several subsection introductions. Focus on what each entity adds to the system, not re-explaining what was already stated.

4. **Fix the chapter numbering in Section 1.4.** Update "Organização deste trabalho" to match the actual chapter structure (currently references Ch. 6 and 7 which don't exist in the compiled document).

5. **Add float specifiers and verify ABNT caption placement.** Ensure all `\begin{figure}` environments use `[htbp]` and all captions are positioned above the figure per ABNT standards.

---

## Detailed Notes

| Location | Issue | Suggestion |
|---|---|---|
| `introduction.tex`, §1.2, line 10–17 | Objectives use plain `-` dashes instead of `\begin{itemize}` | Convert to proper `\itemize` or `\enumerate` environment |
| `introduction.tex`, §1.1, line 6 | "tem ganhado destaque" | Change to "**têm** ganhado destaque" (subject is plural: "técnicas") |
| `introduction.tex`, §1.4, line 27 | References Ch. 6 (Results) and Ch. 7 (Conclusion) | Update numbering to match actual structure |
| `literature_review.tex`, §2.6.1, line 129–131 | Plain dash list for other SR methods | Convert to `\itemize` LaTeX environment |
| `literature_review.tex`, §2.5.1, line 102 | "nenhuma" should be "nenhuma" | Verify — appears correct but reads oddly; consider "até que nenhuma nova regra de equivalência seja encontrada" |
| `methodology.tex`, Code 2, lines 85/120/128/133/139 | TOML listing uses `//` comments | Use TOML-standard `#` comments instead |
| `methodology.tex`, §3.2, line 14 | "linguagem imperativa *JavaScript*" | JavaScript is a multi-paradigm language; React specifically uses a declarative paradigm. Consider rephrasing to "linguagem *JavaScript* com o paradigma declarativo do React" |
| `platform.tex`, §4.1, line 6 | "gerencias" | Typo — should be "**gerenciar**" |
| `platform.tex`, §4.5.1, line 311 | "as rotas HTTP disponibilizadas por eles manipulação" | Awkward phrasing — should be "disponibilizadas por eles **para** manipulação" |
| `platform.tex`, §4.5.5, line 626 | "predições... é armazena" | Agreement error — should be "**são armazenadas**" |
| `platform.tex`, §4.5.5, line 624 | "A entidade Model, além de armazenar as informações referentes ao modelo, armazena em si a sua fronteira de pareto" | Confusing self-reference. Clarify: "A entidade Model armazena, em formato JSON na propriedade `metrics`, os dados da fronteira de Pareto do modelo" |
| `platform.tex`, Code 21, label | `code:markdown_block_domain` has caption identical to Code 20 | Change caption of Code 21 to "Classe de domínio que define um bloco de **documentação** em Markdown" |
| `query_language.tex`, §5.2, line 29 | "FROM PARETO" explanation | The grammar shows `SELECT [TOP <n> \| PARETO]` but the explanations use `FROM PARETO` and `FROM TOP <n>`. This is contradictory — clarify which clause the quantifier belongs to |
| `query_language.tex`, §5.2.1, Ex. 3, line 52 | `WHERE PATTERN IS LIKE` | Grammar shows `PATTERN IS LIKE` as a separate clause, not under `WHERE`. Example contradicts grammar definition |
| `main.tex`, line 182 | Epigraph attributed to Einstein | This is a well-known misattributed quote — verify source or replace |
| `references.bib`, entry `heuristiclabDocumentationAboutHeuristicLabx2013` | Missing `author` field, no `year` | Add author (e.g., "HeuristicLab Team") and year for proper citation formatting |
| `references.bib`, entry `sommerville2011software` | Formatted as `@article` but has no journal/volume/pages | Should be `@book` with publisher "Pearson Education" |
| All chapters | Inconsistent capitalization of "Pareto" | Sometimes "pareto" (lowercase), sometimes "Pareto" (capitalized). Use "Pareto" consistently (it's a proper noun) |
