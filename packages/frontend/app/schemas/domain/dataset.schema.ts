import { z } from "zod";
import { baseImmutableObject, baseMutableObject } from "../common/base.schema";
import { artifactRoleSchema, datasetVisibilitySchema } from "./enums.schema";

export const artifactSchema = baseImmutableObject
	.extend({
		dataset_id: z.uuid(),
		checksum: z.string(),
		size_in_bytes: z.number().int(),
		path: z.string(),
		role: artifactRoleSchema,
		timestamp: z.coerce.date().nullable().optional(),
		group_by_columns: z.array(z.string()).optional(),
	})
	.transform((data) => ({
		id: data.id,
		datasetId: data.dataset_id,
		checksum: data.checksum,
		sizeInBytes: data.size_in_bytes,
		path: data.path,
		role: data.role,
		timestamp: data.timestamp,
		groupByColumns: data.group_by_columns,
	}));

export type Artifact = z.infer<typeof artifactSchema>;

export const datasetSchema = baseMutableObject
	.extend({
		name: z.string(),
		description: z.string(),
		owner_id: z.uuid(),
		visibility: datasetVisibilitySchema,
		artifacts: z.array(artifactSchema),
		deleted_at: z.coerce.date().nullable().optional(),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
		description: data.description,
		ownerId: data.owner_id,
		visibility: data.visibility,
		artifacts: data.artifacts,
		deletedAt: data.deleted_at,
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type Dataset = z.infer<typeof datasetSchema>;

export const artifactPreviewResponseSchema = z.object({
	columns: z.array(z.string()),
	data: z.array(z.record(z.string(), z.any())),
	total: z.number().int(),
});

export type ArtifactPreviewResponse = z.infer<
	typeof artifactPreviewResponseSchema
>;
