import { z } from "zod";

export const lossFunctionSchema = z.enum([
	"MSE",
	"Gaussian",
	"Bernoulli",
	"Poisson",
]);

export const availableFunctionsSchema = z.enum([
	"add",
	"sub",
	"mul",
	"div",
	"power",
	"powerabs",
	"square",
	"cube",
	"sqrt",
	"sqrtabs",
	"cbrt",
	"sin",
	"cos",
	"tan",
	"asin",
	"acos",
	"atan",
	"sinh",
	"cosh",
	"tanh",
	"asinh",
	"acosh",
	"atanh",
	"abs",
	"log",
	"logabs",
	"exp",
	"recip",
	"aq",
]);

export const jobStatusSchema = z.enum([
	"PENDING",
	"QUEUED",
	"RUNNING",
	"SUCCEEDED",
	"FAILED",
	"CANCELED",
	"TIMEOUT",
	"RETRYING",
	"SKIPPED",
	"UNKNOWN",
]);

export const jobSchema = z.object({
	id: z.uuid(),
	status: jobStatusSchema,
	dataset_id: z.uuid(),
	created_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
	started_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date())
		.nullable()
		.optional(),
	finished_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date())
		.nullable()
		.optional(),
	generations: z.number().int().nonnegative(),
	population: z.number().int().nonnegative(),
	max_size: z.number().int().nonnegative(),
	number_of_tournaments: z.number().int().nonnegative(),
	crossover_probability: z.number().min(0).max(1),
	mutation_probability: z.number().min(0).max(1),
	non_terminals: z.array(availableFunctionsSchema),
	loss: lossFunctionSchema,
	optimization_iterations: z.number().int().nonnegative(),
	optimization_repeats: z.number().int().nonnegative(),
	max_param_count: z.number().int(),
	split: z.number().int(),
	simplify: z.boolean(),
});

export const editJobSchema = jobSchema.omit({
	id: true,
	status: true,
	dataset_id: true,
	created_at: true,
	started_at: true,
	finished_at: true,
});

export type JobStatus = z.infer<typeof jobStatusSchema>;

export type Job = z.infer<typeof jobSchema>;
export type EditJob = z.infer<typeof editJobSchema>;

export const getJobsForDatasetResponseSchema = z.array(jobSchema);
