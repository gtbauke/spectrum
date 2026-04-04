# Job Creation Form Design

## Context

The Spectrum platform allows users to run symbolic regression algorithms by creating **Jobs** tied to a **Profile**. A Job configures a genetic programming run: which dataset to fit, the GP hyperparameters, the local optimization settings, and the non-terminal function set.

The form lives in `packages/frontend/app/components/ui/notebook/sections/jobs/add-job.component.tsx` and is rendered inline inside `ProfileJobsSection` when the user clicks the "Add" button.

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
| Available Functions | `nonTerminals` | `MultiSelectInput` | `[]` | Options from `availableFunctionSchema.options` |
| Simplify | `simplify` | `ToggleInput` | `true` | |

### Advanced (collapsed by default, toggled by an expander button)

| Field | Schema key | Component | Default |
|---|---|---|---|
| Max Size | `maxSize` | `TextInput[number]` | `40` |
| Number of Tournaments | `numberOfTournaments` | `TextInput[number]` | `4` |
| Crossover Probability | `crossoverProbability` | `TextInput[number]` | `0.9` |
| Mutation Probability | `mutationProbability` | `TextInput[number]` | `0.1` |
| Optimization Iterations | `optimizationIterations` | `TextInput[number]` | `0` |
| Optimization Repeats | `optimizationRepeats` | `TextInput[number]` | `1` |
| Max Param Count | `maxParamCount` | `TextInput[number]` | `10` |
| Split (%) | `split` | `TextInput[number]` | `75` |

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

## Error Handling

- Validation errors surface inline via each input's `error` prop (populated by `react-hook-form`).
- API errors from `useCreateJobMutation.onError` surface as a top-level error message rendered below the form and above the action buttons.

## Files Touched

| File | Change |
|---|---|
| `add-job.component.tsx` | Full implementation of the form |
| `jobs-section.component.tsx` | Add `profileId` and `datasets` props; pass to `AddJob`; wire `onSuccess`/`onCancel` |
| `hooks/use-create-job-mutation.hook.ts` | New file — TanStack Query mutation hook |

No new UI primitives are required; all inputs (`TextInput`, `SelectInput`, `MultiSelectInput`, `ToggleInput`) already exist.
