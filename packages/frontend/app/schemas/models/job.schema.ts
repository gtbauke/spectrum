import { z } from "zod";
import { jobVersionSchema } from "./job-version.schema";

export const jobSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	owner_id: z.uuid(),
	profile_version_id: z.uuid(),
	versions: z.array(jobVersionSchema),
});

export type Job = z.infer<typeof jobSchema>;
