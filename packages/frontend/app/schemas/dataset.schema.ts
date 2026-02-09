import { z } from "zod";

export const datasetMetadataSchema = z.object({
	id: z.uuid(),
	dataset_id: z.uuid(),
	num_rows: z.number(),
	num_features: z.number(),
	processing_attempts: z.number(),
	last_processing_error: z.string().nullable(),
	created_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
	updated_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
});

export type DatasetMetadata = z.infer<typeof datasetMetadataSchema>;

export const datasetSchema = z.object({
	id: z.uuid(),
	name: z.string(),
	status: z.enum(["PENDING", "PROCESSING", "FAILED", "COMPLETED"]),
	file_path: z.string(),
	checksum: z.string().optional().nullable(),
	metadata: datasetMetadataSchema.nullable().optional(),
	created_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
	updated_at: z
		.string()
		.transform((str) => new Date(str))
		.pipe(z.date()),
});

export type Dataset = z.infer<typeof datasetSchema>;

export const createDatasetSchema = datasetSchema.pick({
	name: true,
});

export type CreateDatasetData = z.infer<typeof createDatasetSchema>;

export const getAllDatasetsResponseSchema = z.array(datasetSchema);
