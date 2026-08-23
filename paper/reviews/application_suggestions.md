# Application Suggestions

Based on the review comments (`areas_of_improvement.md`) and the analysis of the project's codebase (`exploration_findings.md`), here are the actionable suggestions for applying these corrections to the final paper.

## 1. Methodology & SCRUM (Q3a)
*   **Current Issue:** The paper claims to use SCRUM but lacks practical evidence or artifacts. The methodology is purely theoretical.
*   **Suggestion:** Adjust the claims in `paper/chapters/methodology.tex`. Instead of claiming strict adherence to SCRUM, reframe the methodology as an "iterative development process inspired by agile principles." Briefly describe the actual practical workflow used (e.g., iterative development, self-management) and acknowledge the limitations of applying formal SCRUM (like sprints, backlog management, and formal roles) in the context of this specific academic project.

## 2. Domain-Driven Design (DDD) (Q3b, Q3c, Q3e)
*   **Current Issue:** The codebase does not reflect strict DDD principles; it has anemic domain models that closely map to the database structure (CRUD-driven rather than domain-driven).
*   **Suggestion:** Downgrade the architectural claims in the paper. 
    *   Remove or soften the claims of using strict DDD (bounded contexts, ubiquitous language). 
    *   Reframe the architecture as being inspired by "Clean Architecture" and layered design, where the goal was a structural separation of concerns.
    *   Explicitly address the reviewer's concern by acknowledging that the "domain" models were designed pragmatically to map to the database for implementation efficiency, rather than being purely driven by a conceptual domain model. 

## 3. Entity Classification (Q3d)
*   **Current Issue:** The reviewer asked what domain need led to classifying entities into mutable, immutable, and versioned. The code shows this was a technical code-reuse decision.
*   **Suggestion:** Clarify this directly in the text. State that the classification into mutable, immutable, and versioned entities was a **technical, platform-level architectural decision** designed to facilitate code reuse, manage database timestamps, and implement optimistic concurrency control. Explicitly state that it was not derived from a specific requirement of the symbolic regression domain.

## 4. User Stories (Q4a)
*   **Current Issue:** User stories are presented without evidence of how they were gathered or validated with actual users.
*   **Suggestion:** Rename the "Histórias de Usuário" (User Stories) section in `paper/chapters/platform.tex` to "Requisitos Funcionais" (Functional Requirements) or "Capacidades do Sistema" (System Capabilities). Present them as the target capabilities that guided the platform's development, rather than validated user stories gathered from user research.

## 5. Inference Query Language (IQL) (Q5a)
*   **Current Issue:** Syntax mismatches (e.g., `ORDER BY` is in grammar but throws `NotImplementedError` in code) and lack of evaluation for the `PATTERN` clause.
*   **Suggestion:**
    *   **Grammar Fix:** Update the IQL grammar in the paper (e.g., Figure 28) to match the actual implementation. Remove `ORDER BY` from the formal grammar definition in the text or explicitly note it as "planned for future work."
    *   **PATTERN Clause:** Add a brief qualitative discussion or example in the results/evaluation section demonstrating how the `PATTERN` clause can be used theoretically, while explicitly acknowledging that its quantitative evaluation is left for future work.
    *   **Utility vs API:** Add a paragraph clarifying that IQL provides a declarative, domain-specific, and expressive way for researchers to query complex symbolic regression models, which would be cumbersome and less intuitive using standard REST API endpoints.

## 6. Results, Discussion & Claims (Q6a)
*   **Current Issue:** Unsubstantiated claims about scalability and intuitive UI, and the evaluation mainly tests the `eggp` algorithm rather than the platform.
*   **Suggestion:**
    *   **Contribution Evaluation:** Clearly state the scope of the current experiments. Frame the experiment as a "proof-of-concept" that validates the end-to-end integration of the `eggp` algorithm within the Spectrum platform, rather than a comprehensive evaluation of the platform's performance.
    *   **Scalability:** Remove the absolute claim that the platform *is* scalable. Rephrase to state that the architecture was *designed to support scalability* (via RabbitMQ and workers), but note that formal load testing and benchmarking remain as future work.
    *   **Intuitive Interface:** Remove subjective terms like "intuitive" or "personalized" from the text (e.g., page 52), as no formal UX/user testing was conducted. Describe the interface objectively based on its features (e.g., "a web-based graphical interface").

## 7. Minor Textual/Grammatical Corrections
*   **Current Issue:** Correction needed in the abstract around "fields, however".
*   **Suggestion:** Apply the specific grammatical fix in the Abstract (e.g., changing it to "fields; however," or rewording the gerund phrase) to improve readability.
