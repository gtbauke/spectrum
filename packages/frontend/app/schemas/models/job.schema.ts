import { z } from "zod";
import { availableFunctionSchema } from "./available-function.schema";
import { lossFunctionSchema } from "./loss-function.schema";

export const jobSchema = z.object({
	id: z.uuid(),
	version: z.number().int(),
	timestamp: z.iso.datetime(),
	is_latest: z.boolean(),
	name: z.string().nullable().optional(),
	profile_version_id: z.uuid(),
	dataset_artifact_id: z.uuid(),
	generations: z.number().int(),
	population: z.number().int(),
	max_size: z.number().int(),
	number_of_tournaments: z.number().int(),
	crossover_probability: z.number(),
	mutation_probability: z.number(),
	non_terminals: z.array(availableFunctionSchema),
	loss: lossFunctionSchema,
	optimization_iterations: z.number().int(),
	optimization_repeats: z.number().int(),
	max_param_count: z.number().int(),
	split: z.number().int(),
	simplify: z.boolean(),
});

export type Job = z.infer<typeof jobSchema>;
