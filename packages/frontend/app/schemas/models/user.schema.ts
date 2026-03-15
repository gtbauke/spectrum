import { z } from "zod";

export const userSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	first_name: z.string(),
	last_name: z.string(),
	email: z.email(),
	password_hash: z.string(),
	deleted_at: z.iso.datetime().nullable().optional(),
});

export type User = z.infer<typeof userSchema>;
