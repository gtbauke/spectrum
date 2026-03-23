import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";

export const userSchema = baseMutableObject
	.extend({
		first_name: z.string(),
		last_name: z.string(),
		email: z.email(),
		deleted_at: z.coerce.date().nullable(),
	})
	.transform((data) => ({
		id: data.id,
		firstName: data.first_name,
		lastName: data.last_name,
		email: data.email,
		deletedAt: data.deleted_at,
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type User = z.infer<typeof userSchema>;
