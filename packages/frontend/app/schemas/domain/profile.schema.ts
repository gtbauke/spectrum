import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";
import { blockSchema } from "./block.schema";
import { datasetSchema } from "./dataset.schema";
import { profileModeSchema } from "./enums.schema";
import { jobSchema } from "./job.schema";
import { modelSchema } from "./model.schema";

export const rawProfileSchema = baseMutableObject.extend({
	name: z.string(),
	description: z.string(),
	owner_id: z.uuid(),
	mode: profileModeSchema,
	datasets: z.array(datasetSchema),
	jobs: z.array(jobSchema),
	models: z.array(modelSchema),
	blocks: z.array(blockSchema),
});

export const profileSchema = rawProfileSchema.transform((data) => ({
	id: data.id,
	name: data.name,
	description: data.description,
	ownerId: data.owner_id,
	mode: data.mode,
	datasets: data.datasets.map((d) => (d.ownerId ? d : datasetSchema.parse(d))),
	jobs: data.jobs.map((j) => (j.profileId ? j : jobSchema.parse(j))),
	models: data.models.map((m) => (m.profileId ? m : modelSchema.parse(m))),
	blocks: data.blocks.map((b) => (b.kind ? b : blockSchema.parse(b))),
	createdAt: data.created_at,
	updatedAt: data.updated_at,
}));

export type Profile = z.infer<typeof profileSchema>;

export const profileSummarySchema = rawProfileSchema.pick({
	id: true,
	name: true,
	mode: true,
});

export type ProfileSummary = z.infer<typeof profileSummarySchema>;
