# Job Creation Form Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a fully functional inline job creation form inside `ProfileJobsSection`, wired to the backend API, with Basic + Advanced field sections, validation, and loading/error states.

**Architecture:** The form lives in `add-job.component.tsx` and is rendered conditionally when the user clicks the "Add" button. It uses `react-hook-form` with `zodResolver` for validation, a new `useCreateJobMutation` hook for the API call, and `Controller` for the `MultiSelectInput` field. Defaults are authoritative in the backend `CreateJobDto` and mirrored in the frontend Zod schema.

**Tech Stack:** Python/Pydantic (backend DTO), TypeScript/Zod, React, react-hook-form, TanStack Query, lucide-react.

**Spec:** `docs/superpowers/specs/2026-04-04-job-creation-form-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `packages/backend/app/features/profiles/jobs/dtos/create.py` | Modify | Add `default=` values to all optional fields |
| `packages/frontend/app/schemas/dtos/job.dto.ts` | Modify | Sync `.default()` values with backend; update constraints |
| `packages/frontend/app/hooks/use-create-job-mutation.hook.ts` | Create | TanStack Query mutation hook for job creation |
| `packages/frontend/app/components/ui/notebook/sections/jobs/jobs-section.component.tsx` | Modify | Add `profileId` and `datasets` props; thread to `AddJob` |
| `packages/frontend/app/components/ui/notebook/editor.component.tsx` | Modify | Pass `profile.id` and `profile.datasets` to `ProfileJobsSection` |
| `packages/frontend/app/components/ui/notebook/sections/jobs/add-job.component.tsx` | Replace | Full form implementation |

---

## Task 1: Add Defaults to Backend `CreateJobDto`

**Files:**
- Modify: `packages/backend/app/features/profiles/jobs/dtos/create.py`

The backend DTO currently declares all fields as required (`...`). Add field-level `default=` values so the backend accepts partial payloads and the defaults are documented at the source.

- [ ] **Step 1: Update `create.py` with authoritative defaults**

Replace the file contents with:

```python
from uuid import UUID
from pydantic import BaseModel, Field

from core.features.profiles.jobs.available_function import AvailableFunction
from core.features.profiles.jobs.loss_function import LossFunction


class CreateJobDto(BaseModel):
    name: str = Field(..., description="The name of the job")
    runs_against: UUID = Field(..., description="The ID of the dataset it runs against")
    generations: int = Field(default=100, description="The number of generations for the genetic algorithm")
    population: int = Field(default=100, description="The population size for the genetic algorithm")
    max_size: int = Field(default=15, description="The maximum size of the expression")
    number_of_tournaments: int = Field(default=3, description="The number of tournaments for the genetic algorithm")
    crossover_probability: float = Field(default=0.9, description="The crossover probability for the genetic algorithm")
    mutation_probability: float = Field(default=0.3, description="The mutation probability for the genetic algorithm")
    non_terminals: list[AvailableFunction] = Field(
        default=["add", "sub", "mul", "div"],
        description="The non-terminals to be used in the genetic programming",
    )
    loss: LossFunction = Field(default=LossFunction.MSE, description="The loss function to be used for evaluating the models")
    optimization_iterations: int = Field(default=50, description="The number of optimization iterations for the models")
    optimization_repeats: int = Field(default=2, description="The number of optimization repeats for the models")
    max_param_count: int = Field(default=-1, description="The maximum number of parameters (-1 means unlimited)")
    split: int = Field(default=1, description="The split to be used for training and testing the models")
    simplify: bool = Field(default=False, description="Whether to simplify the expressions of the models")
```

- [ ] **Step 2: Verify `LossFunction.MSE` exists in the enum**

Open `packages/core/core/features/profiles/jobs/loss_function.py` and confirm the enum member name. If the enum uses string values (e.g., `"MSE"`), use `default="MSE"` instead of `default=LossFunction.MSE`.

- [ ] **Step 3: Commit**

```bash
git add packages/backend/app/features/profiles/jobs/dtos/create.py
git commit -m "feat(backend): add default values to CreateJobDto"
```

---

## Task 2: Sync Frontend Zod Schema Defaults and Constraints

**Files:**
- Modify: `packages/frontend/app/schemas/dtos/job.dto.ts`

Update the `.default()` values in `createJobDtoSchema` to match the backend, and add `.min()` / `.max()` constraints. Also verify the `max_param_count` constraint allows `-1`.

- [ ] **Step 1: Update `createJobDtoSchema` defaults and constraints**

In `packages/frontend/app/schemas/dtos/job.dto.ts`, update the schema object inside `createJobDtoSchema` (lines roughly 8–24). Replace the entire `.object({...})` block with:

```ts
export const createJobDtoSchema = z
  .object({
    name: z.string().min(1),
    runsAgainst: z.uuid(),
    generations: z.number().int().min(1).default(100),
    population: z.number().int().min(1).default(100),
    maxSize: z.number().int().min(1).default(15),
    numberOfTournaments: z.number().int().min(1).default(3),
    crossoverProbability: z.number().min(0).max(1).default(0.9),
    mutationProbability: z.number().min(0).max(1).default(0.3),
    nonTerminals: z
      .array(availableFunctionSchema)
      .default(["add", "sub", "mul", "div"]),
    loss: lossFunctionSchema.default("MSE"),
    optimizationIterations: z.number().int().min(0).default(50),
    optimizationRepeats: z.number().int().min(1).default(2),
    maxParamCount: z.number().int().min(-1).default(-1),
    split: z.number().int().min(1).default(1),
    simplify: z.boolean().default(false),
  })
  .transform((data) => ({
    name: data.name,
    runs_against: data.runsAgainst,
    generations: data.generations,
    population: data.population,
    max_size: data.maxSize,
    number_of_tournaments: data.numberOfTournaments,
    crossover_probability: data.crossoverProbability,
    mutation_probability: data.mutationProbability,
    non_terminals: data.nonTerminals,
    loss: data.loss,
    optimization_iterations: data.optimizationIterations,
    optimization_repeats: data.optimizationRepeats,
    max_param_count: data.maxParamCount,
    split: data.split,
    simplify: data.simplify,
  }));
```

The `.transform()` block is identical to before — only the `.object({})` defaults and constraints change.

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd packages/frontend && npx tsc --noEmit
```

Expected: no errors in `job.dto.ts` or any file importing it.

- [ ] **Step 3: Commit**

```bash
git add packages/frontend/app/schemas/dtos/job.dto.ts
git commit -m "feat(frontend): sync job DTO defaults and add validation constraints"
```

---

## Task 3: Create `useCreateJobMutation` Hook

**Files:**
- Create: `packages/frontend/app/hooks/use-create-job-mutation.hook.ts`

Follow the same pattern as `use-create-dataset-mutation.hook.ts`.

- [ ] **Step 1: Create the hook file**

```ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createJobs } from "~/api/profiles/jobs/create-jobs.api";
import type { CreateJobDto } from "~/schemas/dtos/job.dto";

export function useCreateJobMutation(profileId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (jobs: CreateJobDto[]) => createJobs(profileId, jobs),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobs", profileId] });
    },
    onError: (error) => {
      console.error("Failed to create job:", error);
    },
  });
}
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd packages/frontend && npx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add packages/frontend/app/hooks/use-create-job-mutation.hook.ts
git commit -m "feat(frontend): add useCreateJobMutation hook"
```

---

## Task 4: Thread Props Through `ProfileJobsSection` and `editor.component.tsx`

**Files:**
- Modify: `packages/frontend/app/components/ui/notebook/sections/jobs/jobs-section.component.tsx`
- Modify: `packages/frontend/app/components/ui/notebook/editor.component.tsx`

`ProfileJobsSection` needs `profileId` and `datasets` props so it can pass them to `AddJob`.

- [ ] **Step 1: Update `ProfileJobsSection` props and wiring**

Replace the contents of `jobs-section.component.tsx`:

```tsx
import { useState } from "react";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import type { Job } from "~/schemas/domain/job.schema";
import { AddButton } from "../add-button.component";
import { AddJob } from "./add-job.component";

type ProfileJobsSectionProps = {
  profileId: string;
  jobs: Job[];
  datasets: Dataset[];
};

export function ProfileJobsSection({
  profileId,
  jobs,
  datasets,
}: ProfileJobsSectionProps) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm space-y-2">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Jobs</h2>

        <AddButton
          isEditing={isEditing}
          onEditClick={() => setIsEditing(true)}
          onSaveClick={() => setIsEditing(false)}
          onCancelClick={() => setIsEditing(false)}
        />
      </div>

      {isEditing && (
        <AddJob
          profileId={profileId}
          datasets={datasets}
          onSuccess={() => setIsEditing(false)}
          onCancel={() => setIsEditing(false)}
        />
      )}

      <div className="space-y-2">
        {jobs.length === 0 && (
          <p className="text-sm text-gray-500">No jobs found.</p>
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Update `editor.component.tsx` to pass `profileId` and `datasets`**

In `editor.component.tsx`, find line 131:

```tsx
<ProfileJobsSection jobs={profile.jobs} />
```

Replace with:

```tsx
<ProfileJobsSection
  profileId={profile.id}
  jobs={profile.jobs}
  datasets={profile.datasets}
/>
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
cd packages/frontend && npx tsc --noEmit
```

Expected: no errors. If `profile.id` reports a type error, check the `Profile` type — the field may be named differently (e.g., `profile.id` vs `profile.profileId`). Inspect `packages/frontend/app/schemas/domain/profile.schema.ts` to confirm.

- [ ] **Step 4: Commit**

```bash
git add packages/frontend/app/components/ui/notebook/sections/jobs/jobs-section.component.tsx
git add packages/frontend/app/components/ui/notebook/editor.component.tsx
git commit -m "feat(frontend): thread profileId and datasets props into ProfileJobsSection"
```

---

## Task 5: Implement the `AddJob` Form

**Files:**
- Replace: `packages/frontend/app/components/ui/notebook/sections/jobs/add-job.component.tsx`

This is the main deliverable. The form uses `react-hook-form` with the Zod schema. The `nonTerminals` `MultiSelectInput` uses `Controller`. Numeric fields use `type="number"` with `valueAsNumber: true` in the `register` call. The entire form must use `z.input<typeof createJobDtoSchema>` as the form type.

- [ ] **Step 1: Implement the complete form**

Replace the entire file with:

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useEffect, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { MultiSelectInput } from "~/components/ui/forms/input/multi-select-input.component";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { ToggleInput } from "~/components/ui/forms/input/toggle-input.component";
import { useCreateJobMutation } from "~/hooks/use-create-job-mutation.hook";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import { availableFunctionSchema, lossFunctionSchema } from "~/schemas/domain/enums.schema";
import { createJobDtoSchema } from "~/schemas/dtos/job.dto";
import { capitalize } from "~/utils/capitalize.util";

// Use the INPUT type so form field names stay camelCase.
// createJobDtoSchema has a .transform() that converts to snake_case at submission time.
type JobFormValues = z.input<typeof createJobDtoSchema>;

type AddJobProps = {
  profileId: string;
  datasets: Dataset[];
  onSuccess: () => void;
  onCancel: () => void;
};

export function AddJob({ profileId, datasets, onSuccess, onCancel }: AddJobProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const { mutate: createJob, isPending } = useCreateJobMutation(profileId);

  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
  } = useForm<JobFormValues>({
    resolver: zodResolver(createJobDtoSchema),
    defaultValues: createJobDtoSchema.parse({
      name: "",
      runsAgainst: datasets[0]?.id ?? "",
    }),
  });

  // Clear the API error as soon as the user edits any field.
  useEffect(() => {
    const subscription = watch(() => setApiError(null));
    return () => subscription.unsubscribe();
  }, [watch]);

  const onSubmit = (data: JobFormValues) => {
    setApiError(null);
    const parsed = createJobDtoSchema.safeParse(data);
    if (!parsed.success) return;
    createJob([parsed.data], {
      onSuccess: () => {
        onSuccess();
      },
      onError: (err) => {
        setApiError(err instanceof Error ? err.message : "Failed to create job. Please try again.");
      },
    });
  };

  const datasetOptions = datasets.map((d) => ({ label: d.name, value: d.id }));
  const lossOptions = lossFunctionSchema.options.map((opt) => ({ label: opt, value: opt }));
  const functionOptions = availableFunctionSchema.options.map((opt) => ({
    label: capitalize(opt),
    value: opt,
  }));

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="p-4 border border-border rounded-lg bg-background-surface space-y-4"
    >
      <h3 className="text-md font-medium">New Job</h3>

      {/* ── Basic fields ── */}
      <div className="grid grid-cols-2 gap-4">
        <TextInput
          label="Name"
          required
          placeholder="e.g. my-experiment-v1"
          error={errors.name}
          {...register("name")}
        />

        <SelectInput
          label="Dataset"
          required
          options={
            datasetOptions.length > 0
              ? datasetOptions
              : [{ label: "No datasets linked to this profile", value: "" }]
          }
          disabled={datasetOptions.length === 0}
          error={errors.runsAgainst}
          {...register("runsAgainst")}
        />
      </div>

      <div className="grid grid-cols-3 gap-4">
        <SelectInput
          label="Loss Function"
          options={lossOptions}
          error={errors.loss}
          {...register("loss")}
        />

        <TextInput
          label="Generations"
          type="number"
          error={errors.generations}
          {...register("generations", { valueAsNumber: true })}
        />

        <TextInput
          label="Population"
          type="number"
          error={errors.population}
          {...register("population", { valueAsNumber: true })}
        />
      </div>

      <Controller
        name="nonTerminals"
        control={control}
        render={({ field }) => (
          <MultiSelectInput
            label="Available Functions"
            options={functionOptions}
            value={field.value ?? []}
            onChange={field.onChange}
            error={errors.nonTerminals as import("react-hook-form").FieldError | undefined}
          />
        )}
      />

      <ToggleInput
        label="Simplify"
        description="Apply algebraic simplification after evolution"
        {...register("simplify")}
      />

      {/* ── Advanced toggle ── */}
      <div className="border-t border-border pt-2">
        <button
          type="button"
          onClick={() => setShowAdvanced((v) => !v)}
          className="flex items-center gap-2 text-xs text-gray-400 hover:text-gray-200 transition-colors"
        >
          {showAdvanced ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          Advanced Settings
        </button>
      </div>

      {/* ── Advanced fields ── */}
      {showAdvanced && (
        <div className="grid grid-cols-2 gap-4">
          <TextInput
            label="Max Size"
            type="number"
            error={errors.maxSize}
            {...register("maxSize", { valueAsNumber: true })}
          />

          <TextInput
            label="Number of Tournaments"
            type="number"
            error={errors.numberOfTournaments}
            {...register("numberOfTournaments", { valueAsNumber: true })}
          />

          <TextInput
            label="Crossover Probability"
            type="number"
            step="0.01"
            error={errors.crossoverProbability}
            {...register("crossoverProbability", { valueAsNumber: true })}
          />

          <TextInput
            label="Mutation Probability"
            type="number"
            step="0.01"
            error={errors.mutationProbability}
            {...register("mutationProbability", { valueAsNumber: true })}
          />

          <TextInput
            label="Optimization Iterations"
            type="number"
            error={errors.optimizationIterations}
            {...register("optimizationIterations", { valueAsNumber: true })}
          />

          <TextInput
            label="Optimization Repeats"
            type="number"
            error={errors.optimizationRepeats}
            {...register("optimizationRepeats", { valueAsNumber: true })}
          />

          <TextInput
            label="Max Param Count"
            type="number"
            error={errors.maxParamCount}
            {...register("maxParamCount", { valueAsNumber: true })}
          />

          <TextInput
            label="Split"
            type="number"
            error={errors.split}
            {...register("split", { valueAsNumber: true })}
          />
        </div>
      )}

      {/* ── API error ── */}
      {apiError && (
        <p className="text-xs text-red-500 animate-in fade-in slide-in-from-top-1">
          {apiError}
        </p>
      )}

      {/* ── Actions ── */}
      <div className="flex justify-end gap-2 pt-2 border-t border-border">
        <button
          type="button"
          onClick={onCancel}
          disabled={isPending}
          className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 border border-border rounded-lg transition-colors disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isPending}
          className="px-4 py-2 text-sm bg-violet-600 hover:bg-violet-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPending ? "Creating…" : "Create Job"}
        </button>
      </div>
    </form>
  );
}
```

**Key implementation notes:**
- `defaultValues` uses `createJobDtoSchema.parse({ name: "", runsAgainst: ... })` to trigger all `.default()` calls and pre-fill every field.
- `register("generations", { valueAsNumber: true })` is essential for numeric fields — without it, react-hook-form returns a string, which fails Zod's `z.number()` check.
- `Controller` wraps `MultiSelectInput` because it uses `value`/`onChange` props rather than `ref`-based `register`.
- `createJobDtoSchema.safeParse(data)` in `onSubmit` applies the `.transform()` that converts camelCase keys to snake_case before the API call.
- The `apiError` state is reset to `null` at the start of each submission (`setApiError(null)`), so stale errors clear immediately on retry.

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd packages/frontend && npx tsc --noEmit
```

Expected: no errors. Common pitfalls:
- If `d.name` errors on `Dataset`, inspect `packages/frontend/app/schemas/domain/dataset.schema.ts` for the correct field name.
- If `d.id` errors, use the correct UUID field name from the schema.
- If `errors.nonTerminals` type errors on the cast, use `as import("react-hook-form").FieldError | undefined` or `as FieldError`.

- [ ] **Step 3: Start the dev server and manually test the form**

```bash
cd packages/frontend && npm run dev
```

Open the app, navigate to a profile, click the "Add" button in the Jobs section. Verify:
1. Form appears with all Basic fields pre-filled with correct defaults.
2. "Advanced Settings" toggle shows/hides the advanced grid.
3. Submitting with an empty name shows inline validation error.
4. Submitting a valid form calls the API and closes the form on success.
5. Cancel closes the form without submitting.

- [ ] **Step 4: Commit**

```bash
git add packages/frontend/app/components/ui/notebook/sections/jobs/add-job.component.tsx
git commit -m "feat(frontend): implement AddJob form with react-hook-form and zod validation"
```

---

## Completion Checklist

- [ ] Backend `CreateJobDto` has all defaults set
- [ ] Frontend Zod schema defaults match backend
- [ ] `useCreateJobMutation` hook created
- [ ] `ProfileJobsSection` accepts and threads `profileId` and `datasets`
- [ ] `editor.component.tsx` passes `profile.id` and `profile.datasets`
- [ ] `AddJob` form renders all fields, validates, submits, shows loading/error states
- [ ] TypeScript compiles with no errors across all changed files
