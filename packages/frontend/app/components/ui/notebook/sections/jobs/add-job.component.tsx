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
import { createJobDtoSchema, createJobFormSchema } from "~/schemas/dtos/job.dto";
import { capitalize } from "~/utils/capitalize.util";

type JobFormValues = z.infer<typeof createJobFormSchema>;

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
    resolver: zodResolver(createJobFormSchema) as any,
    defaultValues: createJobFormSchema.parse({
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

      {apiError && (
        <div className="text-red-500 text-sm font-medium mt-2">{apiError}</div>
      )}

      {/* ── Actions ── */}
      <div className="flex justify-end gap-2 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium hover:bg-background-surface active:bg-background-hover rounded"
          disabled={isPending}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium bg-brand text-black hover:bg-brand-hover rounded flex gap-2 items-center"
          disabled={isPending}
        >
          {isPending ? "Creating..." : "Create Job"}
        </button>
      </div>
    </form>
  );
}
