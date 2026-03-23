import { z } from "zod";
import { blockDataSchema } from "../domain/block.schema";

export const createBlockDtoSchema = z
	.object({
		orderIndex: z.number().int(),
		data: blockDataSchema,
	})
	.transform((data) => ({
		order_index: data.orderIndex,
		data: data.data,
	}));

export type CreateBlockDto = z.infer<typeof createBlockDtoSchema>;

export const updateBlockDtoSchema = z
	.object({
		orderIndex: z.number().int().optional(),
		data: blockDataSchema.optional(),
	})
	.transform((data) => ({
		order_index: data.orderIndex,
		data: data.data,
	}));

export type UpdateBlockDto = z.infer<typeof updateBlockDtoSchema>;

export const bulkUpdateBlockDtoSchema = z
	.object({
		id: z.uuid(),
		orderIndex: z.number().int().optional(),
		data: blockDataSchema.optional(),
	})
	.transform((data) => ({
		id: data.id,
		order_index: data.orderIndex,
		data: data.data,
	}));

export type BulkUpdateBlockDto = z.infer<typeof bulkUpdateBlockDtoSchema>;
