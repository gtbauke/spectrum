# Workspace Blocks Design Spec

**Date**: 2026-04-04
**Topic**: IQL and Markdown Code Editors for Profile Workspace

## Overview

The Workspace section of the Profile Editor provides an interactive notebook-style environment where users can document their discoveries and execute inference scripts. We are implementing two core building blocks: the **InferenceBlock (IQL)** and the **MarkdownBlock**.

## User Experience

### [InferenceBlock (IQL)]
- **Editor**: Monaco-based code editor with a specialized theme.
- **Language**: SQL (as a base for IQL).
- **Autocomplete**: Global completion provider that triggers after a `FROM` token to offer model names associated with the current profile.
- **Interactivity**: Fluid editing and execution feedback (results/metrics display).

### [MarkdownBlock]
- **Dual Display Model**: 
    - **Active/Focused**: Automatically shows the Monaco Markdown editor.
    - **Inert/Blurred**: Shows the rendered "Prose" view (via `react-markdown`).
- **Side-by-Side Preview**: A manual toggle in the block toolbar for complex formatting tasks.
- **Advanced Rendering**: Support for GitHub Flavored Markdown (GFM), Syntax Highlighting, and LaTeX math formulas (`react-katex`).

## Architecture & Components

### [Global Monaco Manager](file:///home/gusta/dev/spectrum/packages/frontend/app/utils/monaco-autocomplete.ts) [NEW]
- A singleton utility to manage global Monaco language configuration.
- `registerModelAutocomplete(models: Model[])`: Registers a `completionProvider` for the `sql` language. It dynamically updates its completion list based on the active profile's models.

### [InferenceBlock](file:///home/gusta/dev/spectrum/packages/frontend/app/components/ui/notebook/sections/workspace/blocks/inference-block.component.tsx) [NEW]
- **Container**: Wrapped in a `Cell` component for standard notebook interactions (drag, delete).
- **State**: Synchronizes code changes to the `EditorStore`.

### [MarkdownBlock](file:///home/gusta/dev/spectrum/packages/frontend/app/components/ui/notebook/sections/workspace/blocks/markdown-block.component.tsx) [NEW]
- **Container**: Wrapped in a `Cell`.
- **Mode Switching**: Decides between "Editor" and "Renderer" based on `activeBlockId` comparison.
- **Math Support**: Configures `react-markdown` with `remark-math` and `rehype-katex` plugins.

## Relationship Mapping

- **Data Origin**: Blocks fetch their initial content from the `EditorStore`.
- **Data Mutation**: Updates are sent back to the store via `updateBlock`.
- **User Preference**: Block activation (focus) is managed globally via the `EditorStore`'s `activeBlockId`.

## Verification Plan

### Automated
- Typecheck verification for props and store interaction.
- Verify block addition and removal still works as expected in the `WorkspaceSection`.

### Manual
- **Autocomplete**: Type `SELECT * FROM ` in an Inference block and verify model names appear at the cursor.
- **Markdown Switch**: Click in and out of a Markdown block and verify the editor/prose auto-toggle.
- **Math**: Type `$E = mc^2$` and verify it renders correctly in the preview mode.
- **Layout**: Verify that the side-by-side preview mode works on different screen sizes.
