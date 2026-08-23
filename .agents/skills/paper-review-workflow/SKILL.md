---
name: paper-review-workflow
description: >-
  Use this skill to automate the process of analyzing paper comments, exploring project sources based on the comments, and generating suggestions for the final paper.
---

# Paper Review Workflow

This skill orchestrates a multi-step workflow involving subagents to process paper comments and suggest improvements. 

## Steps

1. **Step 1: Identify Areas of Improvement**
   - You (the main agent) should read the comment files located in the `paper/comments/` directory.
   - Read the main project paper (e.g. `paper/symbolic_regression_web_interface.tex` and any related files).
   - Identify the areas of improvement the comments talk about.
   - Create a markdown file at `paper/reviews/areas_of_improvement.md` with your summarized findings.

2. **Step 2: Explore Comments Through Project Sources**
   - Invoke a new subagent (Type: `research`, Role: `Codebase and Web Researcher`).
   - Give it the following prompt:
     "Read `paper/reviews/areas_of_improvement.md`. Then, explore the comments through the project sources (e.g., codebase, data, scripts) or other sources on the internet to gather more context and findings. Create a file at `paper/reviews/exploration_findings.md` with your findings. Send a message back when done."
   - Wait for the subagent to complete its task.

3. **Step 3: Suggest Applications for Final Paper**
   - Invoke another new subagent (Type: `self`, Role: `Paper Editor`).
   - Give it the following prompt:
     "Read `paper/reviews/areas_of_improvement.md` and `paper/reviews/exploration_findings.md`. Based on these documents, suggest how the comments should be applied in the final paper. Create a file at `paper/reviews/application_suggestions.md` with your suggestions. Send a message back when done."
   - Wait for the subagent to complete its task.

4. **Step 4: Completion**
   - Once the last subagent finishes, summarize the workflow completion to the user and provide links to the three generated markdown files.
