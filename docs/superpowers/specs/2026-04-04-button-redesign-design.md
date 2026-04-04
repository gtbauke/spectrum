# Button Redesign & Group Specification

## Overview
Redesign the existing `Button` component in the Spectrum frontend to support multiple visual variants and introduce a new `Button.Group` container for seamless grouping of actions.

## Context
The current button relies heavily on hardcoded base Tailwind utilities and only supports a solid primary style. The system needs more flexibility (outline and ghost styles) and a dedicated wrapper for toolbars. 

## Component Design

### 1. Button Variants & States
The `Button` component will support a `variant` prop. The classes will be mapped internally using standard objects and `clsx` + `tailwind-merge`.

**Variants:**
- `primary`: Solid background (`bg-primary-600`), text `white`.
- `outline`: Transparent background, colored border (`border-primary-200` or `border-gray-200`), text colored. Hover changes to light colored background (`bg-primary-50` / `bg-gray-50`).
- `ghost`: Transparent background, no border. Hover applies light background.

**States (Shared):**
- **Default/Idle**: Flex center layout, `py-2 px-4` (or `py-3` based on existing), rounded-lg.
- **Hover**: Specific to variant, handled by pseudo-classes.
- **Active**: `active:scale-[0.98]`.
- **Disabled**: `disabled:opacity-50`, `disabled:pointer-events-none`.
- **Loading**: Same visual treatment as disabled, but swaps or injects a spinner icon and changes text opacity.

### 2. Button.Group Architectural Approach
**Approach Chosen:** Pure CSS Child Selectors (via Tailwind `[&>button...]`).

The `ButtonGroup` component will be a functional React component wrapping its children. 

**Modes:**
- `seamless`: Buttons connect. Interacting borders collapse (`-ml-px`). Rounding is removed on inside edges. First child keeps left rounding, last child keeps right rounding.
- `spaced`: Buttons retain individual shapes, with standard `gap-2` between them.

## File Manifest
1. `packages/frontend/app/components/ui/buttons/button.component.tsx` (MODIFY)
2. `packages/frontend/app/components/ui/buttons/button-group.component.tsx` (NEW)
3. `packages/frontend/app/components/ui/buttons/index.ts` (NEW - optional, export barrel if it makes sense)

## Testing Strategy
- Unit mapping validation (visual review in local environment).
- Test all variants inside both `Button.Group` modes to ensure border collapsing works properly.
