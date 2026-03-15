import { z } from "zod";
import { datasetVersionSchema } from "./dataset-version.schema";
import { profileDatasetRoleSchema } from "./profile-dataset-role.schema";

export const profileDatasetAssociationSchema = z.object({
	id: z.uuid(),
	timestamp: z.iso.datetime(),
	profile_version_id: z.uuid(),
	dataset_version_id: z.uuid(),
	role: profileDatasetRoleSchema,
	dataset_version: datasetVersionSchema.nullable().optional(),
});

export type ProfileDatasetAssociation = z.infer<
	typeof profileDatasetAssociationSchema
>;
