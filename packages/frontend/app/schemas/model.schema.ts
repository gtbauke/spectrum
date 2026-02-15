import { z } from "zod";

export const modelSchema = z.object({
	id: z.uuid(),
	name: z.string(),
	dataset_id: z.uuid(),
	job_id: z.uuid(),
	model_file: z.string().optional().nullable(),
	created_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
	updated_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
});

export type Model = z.infer<typeof modelSchema>;
