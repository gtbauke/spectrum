import { z } from "zod";

export const userDetailsSchema = z
	.object({
		id: z.uuid(),
		first_name: z.string(),
		last_name: z.string(),
		email: z.email(),
		created_at: z.iso.datetime(),
		updated_at: z.iso.datetime(),
		deleted_at: z.iso.datetime().optional().nullable(),
	})
	.transform((data) => ({
		id: data.id,
		firstName: data.first_name,
		lastName: data.last_name,
		email: data.email,
		createdAt: new Date(data.created_at),
		updatedAt: new Date(data.updated_at),
		deletedAt: data.deleted_at ? new Date(data.deleted_at) : null,
	}));

export type UserDetailsApiPayload = z.input<typeof userDetailsSchema>;
export type UserDetails = z.infer<typeof userDetailsSchema>;
