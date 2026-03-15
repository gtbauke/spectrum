import { z } from "zod";

export const artifactTypeValues = [
	"data",
	"schema",
	"stats",
	"preview",
	"features",
	"manifest",
] as const;
export const artifactTypeSchema = z.enum(artifactTypeValues);

export type ArtifactType = z.infer<typeof artifactTypeSchema>;
