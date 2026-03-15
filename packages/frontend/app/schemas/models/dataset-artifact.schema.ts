import { z } from "zod";

export const datasetArtifactSchema = z.object({
	id: z.uuid(),
	timestamp: z.iso.datetime(),
	dataset_id: z.uuid(),
	file_path: z.string(),
	size_in_bytes: z.number().int(),
	checksum: z.string(),
});

export type DatasetArtifact = z.infer<typeof datasetArtifactSchema>;
