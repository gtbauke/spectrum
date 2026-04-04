# Design Spec - Workspace Blocks Redesign (Cyber Laboratory)

**Date**: 2026-04-04
**Topic**: High-performance, premium redesign for the Profile Workspace Blocks.

## 1. Goal & Aesthetic

Transform the basic notebook blocks into a "Cyber Laboratory" interface that feels like a professional symbolic regression workbench. This involves cohesive use of the Spectrum color system and adding a performance-focused results display for inference scripts.

## 2. Color & Style System

The redesign will strictly adhere to the predefined theme variables in `app.css`:

| Element | Role | CSS Variable / Color |
|---------|------|-----------------------|
| **Inference Accent** | Scripting/Math | `--color-secondary` (#10B981 - Emerald) |
| **Markdown Accent** | Documentation/Prose | `--color-primary` (#7C3AED - Purple) |
| **Surface** | Translucent Panels | `--color-background-surface` (#161922) |
| **Border** | Subtle Framing | `--color-border` (#2D3343) |

- **Glassmorphism**: Editor cards use `backdrop-filter: blur(12px)` with a 5% translucent background surface.
- **Micro-glows**: Small glowing indicators in headers to signify active states.

## 3. Component Specifications

### 3.1 InferenceBlock (IQL)
- **Header**:
    - Left-aligned "INFERENCE" label with an emerald glow.
    - Right-aligned "Run" button using the primary purple gradient on hover.
- **Results Pane (NEW)**:
    - **Logic**: A slide-down panel that follows the Monaco editor.
    - **Metrics Grid**: Displays R², MSE, and Complexity using a three-column card layout.
    - **LaTeX Formula**: Centered display of the discovered mathematical model (using `react-katex`).
    - **Status Indicator**: Small, high-contrast badges for "Success", "Running", or "Error".

### 3.2 MarkdownBlock
- **Refined Prose**:
    - Custom styling for `react-markdown` via Tailwind's `@typography` plugin.
    - Emerald accent for links; Purple accent for highlights and list markers.
- **Mode Switching**:
    - **Focused**: Full-width Monaco Markdown editor with syntax highlighting.
    - **Blurred**: Rendered prose view with optimal line spacing (leading-relaxed).
- **Split Preview**: Clean side-by-side view with a vertical divider.

## 4. UI/UX Refinement (Cell Component)
- **Handle**: Subtle "GripVertical" that appears only on block hover.
- **Toolbar**: A "floating" utility bar for block-level operations (delete, move, settings).

## 5. Verification Plan

### Automated
- CSS color variable check (ensure no hardcoded HEX where theme variables exist).

### Manual
- **Results Display**: Confirm the LaTeX formula renders cleanly within the pane.
- **Animations**: Verify the Results Pane slide-down feels smooth and doesn't cause layout shift "jumps".
- **Responsive**: Ensure the Metrics Grid stacks correctly on mobile.
