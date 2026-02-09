import { z } from "zod";
import { datasetSchema } from "./dataset.schema";

export const jobSchema = z.object({
	id: z.uuid(),
	status: z.enum([
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
	]),
	dataset_id: z.uuid(),
	dataset: datasetSchema,
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

export type Job = z.infer<typeof jobSchema>;

export const getJobsForDatasetResponseSchema = z.array(jobSchema);
