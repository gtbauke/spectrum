import { z } from "zod";
import { datasetArtifactVersionSchema } from "./dataset-artifact-version.schema";

export const datasetVersionSchema = z.object({
	id: z.uuid(),
	name: z.string(),
	description: z.string().nullable().optional(),
	version: z.number().int(),
	timestamp: z.iso.datetime(),
	is_latest: z.boolean(),
	dataset_id: z.uuid(),
	artifacts: z.array(datasetArtifactVersionSchema),
});

export type DatasetVersion = z.infer<typeof datasetVersionSchema>;
