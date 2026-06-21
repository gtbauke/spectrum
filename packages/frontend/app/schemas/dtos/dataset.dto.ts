import { z } from "zod";
import {
	artifactRoleSchema,
	datasetVisibilitySchema,
} from "../domain/enums.schema";

export const datasetFilterSchema = z
	.object({
		name: z.string().optional(),
		description: z.string().optional(),
		ownerId: z.uuid().optional(),
		visibility: datasetVisibilitySchema.optional(),
		minSize: z.coerce.number().int().optional(),
		maxSize: z.coerce.number().int().optional(),
		artifactType: artifactRoleSchema.optional(),
		checksum: z.string().optional(),
	})
	.partial()
	.transform((data) => ({
		name: data.name,
		description: data.description,
		owner_id: data.ownerId,
		visibility: data.visibility,
		min_size: data.minSize,
		max_size: data.maxSize,
		artifact_type: data.artifactType,
		checksum: data.checksum,
	}));

export type DatasetFilter = z.infer<typeof datasetFilterSchema>;
export type DatasetFilterInput = Partial<z.input<typeof datasetFilterSchema>>;

export const extendedArtifactRoleSchema = z.enum([
	...artifactRoleSchema.options,
	"auto-split",
]);

export type ExtendedArtifactRole = z.infer<typeof extendedArtifactRoleSchema>;

export const createDatasetWithMultipleArtifactsSchema = z.object({
	datasetName: z.string().min(1),
	datasetDescription: z.string().optional(),
	roles: z.array(
		z.object({
			fileName: z.string(),
			role: extendedArtifactRoleSchema.default("data"),
			dataSplitRatio: z.number().optional(),
		}),
	),
});

export type CreateDatasetWithMultipleArtifactsDto = z.infer<
	typeof createDatasetWithMultipleArtifactsSchema
>;
