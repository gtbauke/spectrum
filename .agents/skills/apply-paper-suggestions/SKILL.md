---
name: apply-paper-suggestions
description: >-
  Use this skill to read paper review suggestions from a markdown file, interactively ask the user whether to apply, modify, or skip each one, apply the accepted changes to the project, and commit each change to git.
---

# Apply Paper Suggestions Workflow

This skill guides you through applying paper suggestions one by one, giving the user control over each change, and automatically committing them.

## Steps

1. **Identify the Input File**
   - By default, read from `paper/reviews/application_suggestions.md`.
   - If the user specified a different file when triggering the skill, use that file instead.

2. **Parse the Suggestions**
   - Read the chosen markdown file and break it down into a list of distinct, actionable suggestions.
   - Keep a running count of how many suggestions are Applied, Modified, and Skipped.

3. **Process Each Suggestion**
   - Loop through each suggestion one by one. For each suggestion:
     1. Present the suggestion to the user and explain briefly what files you plan to change.
     2. Use the `ask_question` tool to ask the user:
        - "Apply as is"
        - "Modify"
        - "Skip"
     3. If the user chooses "Skip", record it and move to the next suggestion.
     4. If the user chooses "Modify", prompt the user to explain how they want to modify the suggestion.
     5. Apply the code/text changes to the appropriate files in the project (e.g. `paper/symbolic_regression_web_interface.tex`).
     6. Run `git add <modified_files>` for the files you changed.
     7. Run `git commit -m "Apply suggestion: <brief description of the change>"`.
     8. Record the suggestion as Applied or Modified.

4. **Completion Summary**
   - Once all suggestions have been processed, present a summary to the user indicating how many suggestions were applied, modified, or skipped.
   - Run `git log -n <number of applied/modified commits>` to show the newly created commits and include this output in your final message to the user.
