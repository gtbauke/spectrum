import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";
import { blockKindSchema } from "./enums.schema";

const markdownBlockDataSchema = z.object({
	kind: z.literal("markdown"),
	data: z.string(),
});

const inferenceBlockDataSchema = z.object({
	kind: z.literal("inference"),
	data: z.string(),
});

export const blockDataSchema = z.discriminatedUnion("kind", [
	markdownBlockDataSchema,
	inferenceBlockDataSchema,
]);

export const rawBlockSchema = baseMutableObject.extend({
	profile_id: z.uuid(),
	kind: blockKindSchema,
	order_index: z.number().int(),
	data: blockDataSchema,
});

export const blockSchema = rawBlockSchema.transform((data) => ({
	id: data.id,
	profileId: data.profile_id,
	kind: data.kind,
	orderIndex: data.order_index,
	data: data.data,
	createdAt: data.created_at,
	updatedAt: data.updated_at,
}));

export type Block = z.infer<typeof blockSchema>;
