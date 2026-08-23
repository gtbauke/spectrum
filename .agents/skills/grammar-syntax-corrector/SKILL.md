---
name: grammar-syntax-corrector
description: Analyzes text in Brazilian Portuguese for grammatical and syntactical errors, flags them to the user, and waits for approval before applying fixes. Can analyze specific files or git commit diffs.
---

# Grammar and Syntax Corrector

This skill is designed to act as an expert proofreader for Brazilian Portuguese academic and professional writing. It analyzes designated text, flags grammatical, syntactical, and spelling errors, suggests corrections, and applies them upon the user's approval.

## Analysis Rules

1. **Grammar & Syntax:** Look for common PT-BR errors such as:
   - Agreement (Concordância verbal e nominal).
   - Placement of pronouns (Colocação pronominal).
   - Prepositions and governance (Regência verbal e nominal).
   - Use of the backtick for "crase" (Uso da crase).
   - Punctuation errors, especially comma splices or missing commas before conjunctions.
2. **Spelling:** Check for typos and adherence to the Novo Acordo Ortográfico.
3. **Tone Preservation:** Do not rewrite the sentence for style (leave that to the `ai-style-analyzer`), only fix objective errors.

## Workflow

1. **Determine the Scope of Analysis**:
   - Wait for the user to provide the target areas to analyze.
   - The user may provide a git commit reference (e.g., `HEAD~1`) or specific file paths/line ranges.
   - **If a commit reference is provided**: Use the `run_command` tool to execute `git diff <commit_ref> -U0` to extract the exact lines that were added or modified. Only analyze those specific lines.
   - **If specific files/lines are provided**: Read only those files or lines using the `view_file` tool.

2. **Flag Errors & Suggest Fixes**:
   - For every error found in the analyzed text, create a report presenting:
     - The file and line number.
     - The original incorrect text (quoted).
     - The grammatical/syntactical explanation of the error.
     - The proposed fixed text.
   - Wait for the user to review the report and approve, reject, or modify the suggestions.

3. **Apply Fixes**:
   - Once the user has given their approval, use the `replace_file_content` or `multi_replace_file_content` tools to safely apply the accepted fixes to the actual files.
