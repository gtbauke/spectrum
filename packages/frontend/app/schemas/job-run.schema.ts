import { z } from "zod";

export const jobRunSchema = z.object({
	id: z.uuid(),
	model_id: z.uuid(),
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
});

export type JobRun = z.infer<typeof jobRunSchema>;
