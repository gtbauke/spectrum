import { z } from "zod";
import { profileDatasetRoleSchema } from "./models/profile-dataset-role.schema";

export const createProfileFromDatasetSchema = z.object({
	datasetName: z.string(),
	datasetDescription: z.string().optional().nullable(),
	datasetRole: profileDatasetRoleSchema,
});

export type CreateProfileFromDatasetInput = z.infer<
	typeof createProfileFromDatasetSchema
>;
