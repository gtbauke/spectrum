# Job Creation Form Design

## Context

The Spectrum platform allows users to run symbolic regression algorithms by creating **Jobs** tied to a **Profile**. A Job configures a genetic programming run: which dataset to fit, the GP hyperparameters, the local optimization settings, and the non-terminal function set.

The form lives in `packages/frontend/app/components/ui/notebook/sections/jobs/add-job.component.tsx` and is rendered inline inside `ProfileJobsSection` when the user clicks the "Add" button.

> **Implementation Note — Zod Transform Gotcha**: `createJobDtoSchema` includes a `.transform()` that converts camelCase keys to snake_case. When used with `react-hook-form`'s `zodResolver`, this causes the inferred form type to be the *output* (snake_case), not the *input* (camelCase). The form must use `z.input<typeof createJobDtoSchema>` for the `useForm<...>` generic so field names match the component props. The schema is passed to `zodResolver` as-is for validation; the transform runs only at submission time.

## Field Inventory

All fields map directly to `createJobDtoSchema` in `packages/frontend/app/schemas/dtos/job.dto.ts`.

### Basic (always visible)

| Field | Schema key | Component | Default | Notes |
|---|---|---|---|---|
| Name | `name` | `TextInput` | — | Required |
| Dataset | `runsAgainst` | `SelectInput` | — | Required; populated from `datasets` prop |
| Loss Function | `loss` | `SelectInput` | `"MSE"` | Options: `MSE`, `Gaussian`, `Bernoulli`, `Poisson` |
| Generations | `generations` | `TextInput[number]` | `100` | |
| Population | `population` | `TextInput[number]` | `100` | |
| Available Functions | `nonTerminals` | `MultiSelectInput` | `[]` | Options from `availableFunctionSchema.options` (imported from `~/schemas/domain/enums.schema`); must be wired with `Controller` (not `register`) because `MultiSelectInput` uses `value`/`onChange` props |
| Simplify | `simplify` | `ToggleInput` | `true` | |

### Advanced (collapsed by default, toggled by an expander button)

| Field | Schema key | Component | Default | Constraints |
|---|---|---|---|---|
| Max Size | `maxSize` | `TextInput[number]` | `40` | int ≥ 1 |
| Number of Tournaments | `numberOfTournaments` | `TextInput[number]` | `4` | int ≥ 1 |
| Crossover Probability | `crossoverProbability` | `TextInput[number]` | `0.9` | 0 – 1 |
| Mutation Probability | `mutationProbability` | `TextInput[number]` | `0.1` | 0 – 1 |
| Optimization Iterations | `optimizationIterations` | `TextInput[number]` | `0` | int ≥ 0 |
| Optimization Repeats | `optimizationRepeats` | `TextInput[number]` | `1` | int ≥ 1 |
| Max Param Count | `maxParamCount` | `TextInput[number]` | `10` | int ≥ 1 |
| Split (%) | `split` | `TextInput[number]` | `75` | int 1 – 100 |

Numerical constraints are enforced at the Zod schema level using `.min()` / `.max()` refinements added directly in `createJobDtoSchema`. The `Generations` and `Population` basic fields also have the constraint int ≥ 1.

### Dataset Selector Mapping

The `SelectInput` for the `runsAgainst` field is populated from `datasets` prop:

```ts
options={datasets.map(d => ({ label: d.name, value: d.id }))}
```

If `datasets` is empty, the select renders a disabled placeholder option: `"No datasets linked to this profile"`.

## Architecture

### Component Interface

```tsx
type AddJobProps = {
  profileId: string;
  datasets: Dataset[];
  onSuccess: () => void;
  onCancel: () => void;
};
```

`ProfileJobsSection` is updated to accept a `datasets: Dataset[]` prop and pass it (along with `profileId` and the cancel/success callbacks) into `AddJob`.

### Form Management

- **Library**: `react-hook-form` with `zodResolver(createJobDtoSchema)`.
- **Pre-population**: All fields default to the schema defaults defined in `createJobDtoSchema` (see field table above).
- **Submission**: Calls `createJobs(profileId, [parsedData])` from the existing API module. The DTO transform in `createJobDtoSchema` handles camelCase → snake_case conversion before the request.

### Mutation Hook

A new hook `useCreateJobMutation` is added in `packages/frontend/app/hooks/use-create-job-mutation.hook.ts`, following the same pattern as `useCreateDatasetMutation`:

```ts
export function useCreateJobMutation(profileId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (jobs: CreateJobDto[]) => createJobs(profileId, jobs),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobs", profileId] });
    },
  });
}
```

### Data Flow

```
ProfileNotebook
  └─ ProfileJobsSection (datasets: Dataset[], profileId: string, jobs: Job[])
       └─ AddJob (profileId, datasets, onSuccess, onCancel)
            ├─ useForm (react-hook-form + zodResolver)
            └─ useCreateJobMutation(profileId)
                  └─ createJobs(profileId, [dto]) → POST /profiles/:id/jobs
```

### Prop Threading

`ProfileJobsSection` currently receives `jobs: Job[]`. It must be updated to also receive:
- `profileId: string` — needed by `AddJob` for the API call.
- `datasets: Dataset[]` — needed to populate the dataset `SelectInput`.

The parent component (`ProfileNotebook` or equivalent) already has both pieces of data available.

### Advanced Section Toggle

A local boolean state `showAdvanced` controls whether the advanced fields are visible. The expander is a plain `<button>` rendering a chevron icon (from `lucide-react`) and the label "Advanced Settings". No library dependency required.

`showAdvanced` resets to `false` whenever the form is closed (i.e., when `onCancel` or `onSuccess` fires).

## Error Handling

- Validation errors surface inline via each input's `error` prop (populated by `react-hook-form`).
- API errors from `useCreateJobMutation.onError` are stored in local state (`apiError: string | null`) and rendered as a top-level error message below the form and above the action buttons.
- The `apiError` is cleared on every `onChange` event (use `react-hook-form`'s `watch` subscription or clear it in the `onSubmit` handler before the mutation fires).

### Submission Loading State

- While the mutation is pending (`isPending === true`), the "Create Job" button is disabled and shows a loading spinner (or the text "Creating…") to prevent double submissions.

## Files Touched

| File | Change |
|---|---|
| `add-job.component.tsx` | Full implementation of the form |
| `jobs-section.component.tsx` | Add `profileId` and `datasets` props; pass to `AddJob`; wire `onSuccess`/`onCancel` |
| `hooks/use-create-job-mutation.hook.ts` | New file — TanStack Query mutation hook |
| Parent component (e.g. `ProfileNotebook` or route loader) | Pass `profileId` and `datasets` down to `ProfileJobsSection` |

No new UI primitives are required; all inputs (`TextInput`, `SelectInput`, `MultiSelectInput`, `ToggleInput`) already exist.
