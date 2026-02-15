import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { getJob } from "~/api/get-job.api";
import { MainContainer } from "~/components/layout/main.component";
import { FormInput } from "~/components/ui/forms/form-input.component";
import { type EditJob, editJobSchema } from "~/schemas/job.schema";
import type { Route } from "./+types/edit-job";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
	const response = await getJob(params.datasetId, params.jobId);
	return { job: response };
}

export default function EditJobScreen({ loaderData }: Route.ComponentProps) {
	const navigate = useNavigate();
	const { register, handleSubmit, reset } = useForm({
		defaultValues: {
			generations: loaderData.job.generations,
			population: loaderData.job.population,
			max_size: loaderData.job.max_size,
			number_of_tournaments: loaderData.job.number_of_tournaments,
			crossover_probability: loaderData.job.crossover_probability,
			mutation_probability: loaderData.job.mutation_probability,
			optimization_iterations: loaderData.job.optimization_iterations,
			optimization_repeats: loaderData.job.optimization_repeats,
			max_param_count: loaderData.job.max_param_count,
			split: loaderData.job.split,
			simplify: loaderData.job.simplify,
			loss: loaderData.job.loss,
			non_terminals: loaderData.job.non_terminals,
		},
		resolver: zodResolver(editJobSchema),
	});

	const onSubmit = (data: EditJob) => {};

	const onCancel = () => {
		reset();
		navigate(`/datasets/${loaderData.job.dataset_id}/jobs`);
	};

	return (
		<MainContainer>
			<div className="space-y-6">
				<header className="space-y-1">
					<h1 className="text-2xl font-bold">Editing Job</h1>
					<p className="text-xs text-gray-600">{loaderData.job.id}</p>
				</header>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<h2 className="text-lg font-semibold">Job Properties</h2>

					<form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
						<FormInput
							label="Generations"
							type="number"
							{...register("generations")}
						/>

						<FormInput
							label="Population"
							type="number"
							{...register("population")}
						/>

						<FormInput
							label="Max Size"
							type="number"
							{...register("max_size")}
						/>

						<FormInput
							label="Number of Tournaments"
							type="number"
							{...register("number_of_tournaments")}
						/>

						<FormInput
							label="Crossover Probability"
							type="number"
							step="0.01"
							{...register("crossover_probability")}
						/>

						<FormInput
							label="Mutation Probability"
							type="number"
							step="0.01"
							{...register("mutation_probability")}
						/>

						<FormInput
							label="Optimization Iterations"
							type="number"
							{...register("optimization_iterations")}
						/>

						<FormInput
							label="Optimization Repeats"
							type="number"
							{...register("optimization_repeats")}
						/>

						<FormInput
							label="Max Param Count"
							type="number"
							{...register("max_param_count")}
						/>

						<FormInput label="Split" type="text" {...register("split")} />

						{/* TODO: create checkbox component */}
						<FormInput
							label="Simplify"
							type="checkbox"
							{...register("simplify")}
						/>

						{/* TODO: create select component */}
						<FormInput label="Loss" type="text" {...register("loss")} />

						{/* TODO: create multiselect component */}
						<FormInput
							label="Non Terminals (comma separated)"
							type="text"
							{...register("non_terminals")}
						/>

						<div className="flex flex-col gap-2">
							<input
								type="submit"
								value="Submit"
								className="cursor-pointer p-2 bg-green-600 hover:bg-green-700 active:bg-green-800 rounded-sm font-bold"
							/>

							<input
								type="reset"
								value="Cancel"
								className="cursor-pointer p-2 bg-red-600 hover:bg-red-700 active:bg-red-800 rounded-sm font-bold"
								onClick={onCancel}
							/>
						</div>
					</form>
				</div>
			</div>
		</MainContainer>
	);
}
