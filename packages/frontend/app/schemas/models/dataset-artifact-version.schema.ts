import { z } from "zod";
import { artifactTypeSchema } from "./artifact-type.schema";
import { datasetArtifactSchema } from "./dataset-artifact.schema";

export const datasetArtifactVersionSchema = z.object({
	id: z.uuid(),
	timestamp: z.iso.datetime(),
	dataset_version_id: z.uuid(),
	dataset_artifact_id: z.uuid(),
	dataset_artifact: datasetArtifactSchema.nullable().optional(),
	artifact_type: artifactTypeSchema,
});

export type DatasetArtifactVersion = z.infer<
	typeof datasetArtifactVersionSchema
>;
