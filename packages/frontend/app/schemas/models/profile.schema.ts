import { z } from "zod";
import { profileVersionSchema } from "./profile-version.schema";

export const profileSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	owner_id: z.uuid(),
	versions: z.array(profileVersionSchema),
});

export type Profile = z.infer<typeof profileSchema>;
