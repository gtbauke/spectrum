import { z } from "zod";
import { profileVisibilitySchema } from "~/schemas/models/profile-visibility.schema";

export const profileVersionSummarySchema = z
	.object({
		id: z.uuid(),
		version: z.int().nonnegative(),
		timestamp: z.iso.datetime(),
		is_latest: z.boolean(),
		name: z.string(),
		description: z.string().optional().nullable(),
		visibility: profileVisibilitySchema,
		profile_id: z.uuid(),
		attached_dataset_count: z.int().nonnegative(),
	})
	.transform((data) => ({
		id: data.id,
		version: data.version,
		timestamp: new Date(data.timestamp),
		isLatest: data.is_latest,
		name: data.name,
		description: data.description ?? "",
		visibility: data.visibility,
		profileId: data.profile_id,
		attachedDatasetCount: data.attached_dataset_count,
	}));

export type ProfileVersionSummaryApiPayload = z.input<
	typeof profileVersionSummarySchema
>;

export type ProfileVersionSummary = z.infer<typeof profileVersionSummarySchema>;
