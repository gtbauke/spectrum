import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";

export const modelSchema = baseMutableObject
	.extend({
		name: z.string(),
		profile_id: z.uuid(),
		generated_by: z.uuid(),
		path: z.string(),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
		profileId: data.profile_id,
		generatedBy: data.generated_by,
		path: data.path,
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type Model = z.infer<typeof modelSchema>;
