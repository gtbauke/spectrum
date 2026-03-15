import { z } from "zod";
import { datasetVersionSchema } from "./dataset-version.schema";

export const datasetSchema = z.object({
	id: z.uuid(),
	created_at: z.iso.datetime(),
	updated_at: z.iso.datetime(),
	owner_id: z.uuid(),
	deleted_at: z.iso.datetime().nullable().optional(),
	versions: z.array(datasetVersionSchema),
});

export type Dataset = z.infer<typeof datasetSchema>;
