# Job Listing Design Specification

## Overview
This document outlines the design and architectural implementation for displaying the jobs listing within the `ProfileJobsSection` (`packages/frontend/app/components/ui/notebook/sections/jobs/jobs-section.component.tsx`). The primary goal is to present complex job configuration and execution state (runs) in an accessible, visually consistent card layout inspired by the `DatasetItem` component.

## Data Source & Context
The implementation relies on the `Job` schema (zod inferred) coming from the backend properties of a `Profile`:
- **Basic Configuration**: Name, `runsAgainst` (Dataset reference), Loss function, Generations, Population, Simplify toggle.
- **Advanced Configuration**: Max Size, Tournaments, Crossover/Mutation Probabilities, Optimization details, Max Param Count.
- **History**: An array of `Run` objects (with status, start/finish times).

## UI Architecture (Expandable Card Format)

The `JobItem` will be implemented as a bounded component (`job-item.component.tsx`) that behaves as a progressive disclosure card.

### 1. Card Container
- Consistent with `DatasetItem`, the outer wrapper will use `bg-background border border-border rounded-lg p-4`.
- Incorporates a clean internal flex/grid layout to separate concerns into Header, Overview, and Advanced sections.

### 2. Header
- **Title**: Displays `job.name` using `<h3 className="font-bold text-md">`.
- **Status Indicator**: Right-aligned pill or badge indicating the status of the *latest* run (e.g., `Queued`, `Running`, `Completed`, `Failed`). If no runs exist, it shows `No Runs`.

### 3. Basic Settings Grid (Always Visible)
Directly beneath the header, a concise UI element (like a small data list or grid) displays the most critical parameters that were defined under "Basic Settings" during job creation:
- **Dataset**: Resolved dataset name using `job.runsAgainst`.
- **Loss Function**: `job.loss`
- **Generations**: `job.generations`
- **Population**: `job.population`
- **Simplify**: Boolean representation (Yes/No).

### 4. Advanced Settings & History (Accordion)
To maintain vertical scanning efficiency across multiple jobs, advanced settings are hidden behind a toggle button.
- **Toggle Mechanism**: A discrete button (e.g., "Advanced Settings & History" with a `ChevronDown`/`ChevronUp` icon) matching the one in `AddJob`.
- **Expanded State (Advanced Stats)**: A grid (`grid-cols-2` or `grid-cols-3` depending on space) displaying Max Size, Tournaments, Crossover Probability, Mutation Probability, etc.
- **Expanded State (Run History)**: A vertical list or mini-table detailing the job's historical runs. This includes the `status` block, `startedAt`, and `finishedAt` timings mapped over `job.runs`.

## Component Scaffolding

```tsx
// Proposed Component Signature
type JobItemProps = {
	job: Job;
	datasets: Dataset[]; // Passed down to resolve dataset name from reference ID
};

export function JobItem({ job, datasets }: JobItemProps) {
	// 1. Resolve dataset name
	// 2. Determine latest run status
	// 3. Manage accordion state (isExpanded)
	// 4. Render Layout
}
```

## Integration Points
1. `ProfileJobsSection` will map over the `jobs` array and render `<JobItem job={job} datasets={datasets} />`.
2. Uses the same project-native CSS variables (`bg-background-surface`, `border-border`) utilized elsewhere in the application to ensure color parity out of the box.
