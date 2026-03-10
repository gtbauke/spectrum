import { z } from "zod";

export const artifactTypeSchema = z.enum([
	"data",
	"schema",
	"stats",
	"preview",
	"features",
	"manifest",
]);

export type ArtifactType = z.infer<typeof artifactTypeSchema>;

export const datasetArtifactSchema = z.object({
	id: z.uuid(),
	dataset_id: z.uuid(),
	file_path: z.string().min(1, "File path is required"),
	size_in_bytes: z.number().int().nonnegative(),
	checksum: z.string(),
	timestamp: z.iso.datetime(),
});

export const datasetArtifactVersionSchema = z.object({
	id: z.uuid(),
	dataset_version_id: z.uuid(),
	dataset_artifact_id: z.uuid(),
	artifact_type: artifactTypeSchema,
	timestamp: z.iso.datetime(),
});

export const datasetVersionSchema = z.object({
	id: z.uuid(),
	dataset_id: z.uuid(),
	version: z.number().int().positive(),
	is_latest: z.boolean(),
	timestamp: z.iso.datetime(),
	artifacts: z.array(datasetArtifactVersionSchema),
});

export const datasetSchema = z.object({
	id: z.uuid(),
	name: z.string().min(1, "Dataset name is required"),
	description: z.string().nullable().optional(),
	owner_id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	deleted_at: z.iso.datetime().nullable().optional(),
	versions: z.array(datasetVersionSchema),
});

export type Dataset = z.infer<typeof datasetSchema>;
