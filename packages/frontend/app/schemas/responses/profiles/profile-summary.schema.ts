import { z } from "zod";
import { ownerDetailsSchema } from "../owners/owner-details.schema";
import { profileVersionSummarySchema } from "./profile-version-summary.schema";

export const profileSummarySchema = z
	.object({
		id: z.uuid(),
		created_at: z.iso.datetime(),
		updated_at: z.iso.datetime(),
		owner: ownerDetailsSchema,
		versions: z.array(profileVersionSummarySchema),
	})
	.transform((data) => ({
		id: data.id,
		createdAt: new Date(data.created_at),
		updatedAt: new Date(data.updated_at),
		owner: data.owner,
		versions: data.versions,
	}));

export type ProfileSummaryApiPayload = z.input<typeof profileSummarySchema>;
export type ProfileSummary = z.infer<typeof profileSummarySchema>;
