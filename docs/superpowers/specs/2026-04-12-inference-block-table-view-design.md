# Inference Block Result Table View Design

## Goal
The goal of this feature is to enhance the `InferenceBlock` by allowing users to switch between a list view and a compact table view for inference results. This will provide better data density and visibility for many variants, especially when focused on numerical metrics like fitness, size, and frequency.

## User Review Required
> [!IMPORTANT]
> - By default, the list view remains active. This choice preserves visual consistency for existing users.
> - The table view will truncate raw expressions but offer a LaTeX "peek" on hover using tooltips.

## Proposed Changes

### Frontend Component: `InferenceBlock`

#### [MODIFY] `packages/frontend/app/components/ui/notebook/sections/workspace/blocks/inference-block.component.tsx`
- Add `viewMode` state (`list` | `table`).
- Implement the `ViewSwitcher` component to toggle between `list` and `table`.
- Update `ResultsPane` to conditionally render `ResultItem` list or `ResultsTable`.
- Implement `ResultsTable` using `@tanstack/react-table`.
- Integrate `@radix-ui/react-tooltip` for the math expression peek.

### Data Flow
1. User clicks the table icon in the `ResultsPane` header.
2. `viewMode` state updates to `table`.
3. `ResultsPane` renders the `ResultsTable` component instead of mapping over `ResultItem`.
4. `ResultsTable` maps the current `results` array into rows.
5. Hovering over a row's expression cell triggers a Radix Tooltip showing the LaTeX math.

## Open Questions
- None at this time (the user approved Option 2 for the LaTeX peek).

## Verification Plan

### Automated Tests
- N/A for this visual feature (manual verification preferred).

### Manual Verification
1. Run an inference query in the frontend.
2. Toggle to "Table View" using the new icon.
3. Verify all columns (Fitness, Size, DL, Frequency) are visible.
4. Verify bidirectional scrolling (scroll right to see extra columns).
5. Hover over a raw expression and ensure the LaTeX peek appears correctly.
6. Toggle back to "List View" and ensure the layout is intact.
