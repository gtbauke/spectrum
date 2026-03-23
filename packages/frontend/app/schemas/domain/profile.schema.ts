import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";
import type { blockSchema } from "./block.schema";
import type { datasetSchema } from "./dataset.schema";
import { profileModeSchema } from "./enums.schema";
import type { jobSchema } from "./job.schema";
import type { modelSchema } from "./model.schema";

export const profileSchema = baseMutableObject
	.extend({
		name: z.string(),
		description: z.string(),
		owner_id: z.uuid(),
		mode: profileModeSchema,
		datasets: z.array(z.any()),
		jobs: z.array(z.any()),
		models: z.array(z.any()),
		blocks: z.array(z.any()),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
		description: data.description,
		ownerId: data.owner_id,
		mode: data.mode,
		datasets: data.datasets as z.infer<typeof datasetSchema>[],
		jobs: data.jobs as z.infer<typeof jobSchema>[],
		models: data.models as z.infer<typeof modelSchema>[],
		blocks: data.blocks as z.infer<typeof blockSchema>[],
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type Profile = z.infer<typeof profileSchema>;
