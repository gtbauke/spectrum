import { z } from "zod";
import { availableFunctionSchema } from "./available-function.schema";
import { lossFunctionSchema } from "./loss-function.schema";

export const jobVersionSchema = z.object({
	id: z.uuid(),
	version: z.number().int(),
	timestamp: z.iso.datetime(),
	is_latest: z.boolean(),
	job_id: z.uuid(),
	name: z.string().nullable().optional(),
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

export type JobVersion = z.infer<typeof jobVersionSchema>;
