import { z } from "zod";
import { ownerTypeSchema } from "./owner-type.schema";

export const ownerSchema = z.object({
	id: z.uuid(),
	version: z.number().int(),
	timestamp: z.iso.datetime(),
	is_latest: z.boolean(),
	owner_type: ownerTypeSchema,
	user_id: z.uuid().nullable().optional(),
	deleted_at: z.iso.datetime().nullable().optional(),
});

export type Owner = z.infer<typeof ownerSchema>;
