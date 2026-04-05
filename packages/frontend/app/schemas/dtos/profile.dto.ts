import { z } from "zod";
import { rawBlockSchema } from "../domain/block.schema";
import { artifactRoleSchema, profileModeSchema } from "../domain/enums.schema";

export const createProfileDtoSchema = z.object({
	name: z.string().min(1),
	description: z.string().default(""),
});

export type CreateProfileDto = z.infer<typeof createProfileDtoSchema>;

export const updateProfileDtoSchema = z.object({
	name: z.string().optional(),
	description: z.string().optional(),
	mode: profileModeSchema.optional(),
	blocks: z.array(rawBlockSchema).optional(),
});

export type UpdateProfileDto = z.infer<typeof updateProfileDtoSchema>;

export const createProfileFromDatasetDtoSchema = z.object({
	datasetName: z.string().min(1),
	datasetDescription: z.string().optional(),
	datasetRole: artifactRoleSchema.default("data"),
});

export type CreateProfileFromDatasetDto = z.infer<
	typeof createProfileFromDatasetDtoSchema
>;

export const profileFilterSchema = z.object({
	name: z.string().optional(),
	description: z.string().optional(),
	onlyMe: z.boolean().optional(),
	status: z.string().optional(),
	visibility: z.string().optional(),
});

export type ProfileFilter = z.infer<typeof profileFilterSchema>;

export const linkDatasetToProfileDtoSchema = z.object({
	dataset_ids: z.array(z.uuid()),
});

export type LinkDatasetToProfileDto = z.infer<
	typeof linkDatasetToProfileDtoSchema
>;
