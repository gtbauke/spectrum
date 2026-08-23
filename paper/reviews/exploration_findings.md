# Exploration Findings

Based on an analysis of the project's codebase, data, and LaTeX source files, here are the findings regarding the review comments:

## 1. Methodology & SCRUM (Q3a)
- **Findings:** A search through the project files and `paper/chapters/methodology.tex` reveals a mention of SCRUM principles ("divisão do trabalho em ciclos curtos e a revisão constante"), mas there are no tangible artifacts in the repository (e.g., exported backlog, issue tracker data, sprint reviews, or meeting notes) demonstrating how it was actually operationalized. The methodology section remains purely theoretical.

## 2. Domain-Driven Design (DDD) (Q3b, Q3c, Q3e)
- **Findings:** The source code strongly supports the reviewer's critique. In the `packages/` directory, domain entities are defined in `core/core/features/` using Pydantic, while database models are defined in `db_core/db/features/` using SQLAlchemy. A comparison (e.g., for `Dataset` and `DatasetORM`) shows a nearly 1-to-1 mapping. The domain models are anemic and include infrastructure concerns like `created_at`, `updated_at`, and `deleted_at`, confirming that the domain representation is dictated by the CRUD database structure rather than ubiquitous language or bounded contexts.

## 3. Entity Classification (Q3d)
- **Findings:** The classification into mutable, immutable, and versioned entities is implemented as generic base classes (`BaseMutableDomainModel`, `BaseImmutableDomainModel`, `BaseImmutableVersionedDomainModel` in `packages/core/core/features/base.py`). This was clearly a platform/technical decision for code reuse (e.g., auto-managing IDs, timestamps, and optimistic concurrency control via version fields) rather than a requirement derived from the actual symbolic regression domain. 

## 4. User Stories (Q4a)
- **Findings:** The user stories are listed in `paper/chapters/platform.tex` (`\section{Histórias de Usuário}`). However, there is no accompanying text, documentation, or evidence in the project explaining how these stories were gathered (e.g., through interviews, surveys) or who the target persona is. They appear to be retroactively written to describe the implemented features rather than validated requirements.

## 5. Inference Query Language (IQL) (Q5a)
- **Findings:** 
  - **Syntax Mismatches (`ORDER BY`):** The codebase explicitly proves the reviewer right. In `packages/inference_query_language/iql/parser/parselets/commands/select_command_parselet.py` (Line 124), the `ORDER BY` clause literally throws a `NotImplementedError("ORDER BY clause is not implemented yet")`. It is present in the theoretical grammar but not functional in the code.
  - **`PATTERN` Clause:** The parsing for the `PATTERN` clause is implemented (e.g., `_parse_pattern` checking for `IS LIKE`), but the reviewer is correct that it is missing from the evaluation.

## 6. Results, Discussion & Claims (Q6a)
- **Findings:** 
  - **Contribution Evaluation:** `paper/chapters/results.tex` confirms the experiment only tests the rediscovery of the Law of Universal Gravitation with varying noise levels. This tests the capabilities of the underlying `eggp` algorithm rather than the Spectrum platform itself.
  - **Missing IQL Evaluation:** The only IQL queries used in the results section are basic `SELECT PARETO ...` and `SELECT TOP 10 ...` commands. The `PATTERN` clause is completely absent from the experiments.
  - **Unsubstantiated Claims:** 
    - **Scalability:** The scalability claim stems from the architectural use of RabbitMQ and multiple workers (`platform.tex`). However, there is no load testing, benchmarking, or experimental data in the results chapter to back up the claim that multiple workers practically lead to scalability.
    - **Intuitive Interface:** There is no mention of UX testing, A/B testing, or user feedback (e.g., SUS scale) anywhere in the repository or paper to validate the "intuitive" claim.
