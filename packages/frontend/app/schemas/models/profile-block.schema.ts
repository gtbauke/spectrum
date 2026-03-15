import { z } from "zod";
import { profileBlockTypeSchema } from "./profile-block-type.schema";

export const profileBlockSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	version_id: z.uuid(),
	order_index: z.number().int(),
	type: profileBlockTypeSchema,
	data: z.record(z.string(), z.any()),
});

export type ProfileBlock = z.infer<typeof profileBlockSchema>;
