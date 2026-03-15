import { z } from "zod";

export const refreshTokenSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	user_id: z.uuid(),
	owner_id: z.uuid(),
	token_hash: z.string(),
	expires_at: z.iso.datetime(),
	revoked: z.boolean().nullable().optional(),
});

export type RefreshToken = z.infer<typeof refreshTokenSchema>;
