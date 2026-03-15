import { z } from "zod";
import { profileBlockSchema } from "./profile-block.schema";
import { profileDatasetAssociationSchema } from "./profile-dataset-association.schema";
import { profileStatusSchema } from "./profile-status.schema";
import { profileVisibilitySchema } from "./profile-visibility.schema";

export const profileVersionSchema = z.object({
	id: z.uuid(),
	version: z.number().int(),
	timestamp: z.iso.datetime(),
	is_latest: z.boolean(),
	name: z.string(),
	description: z.string().nullable().optional(),
	status: profileStatusSchema,
	visibility: profileVisibilitySchema,
	profile_id: z.uuid(),
	datasets: z.array(profileDatasetAssociationSchema),
	blocks: z.array(profileBlockSchema),
});

export type ProfileVersion = z.infer<typeof profileVersionSchema>;
