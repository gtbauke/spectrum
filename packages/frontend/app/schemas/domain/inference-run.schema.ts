import { z } from "zod";
import { baseVersionedObject } from "../common/base.schema";
import { inferenceRunStatusSchema } from "./enums.schema";

export const inferenceRunRawSchema = baseVersionedObject.extend({
	block_id: z.string().uuid(),
	profile_id: z.string().uuid(),
	query: z.string(),
	status: inferenceRunStatusSchema,
	execution_time_ms: z.number().int().nullable(),
	error: z.string().nullable(),
});

export type InferenceRunRaw = z.infer<typeof inferenceRunRawSchema>;

export const inferenceRunSchema = inferenceRunRawSchema.transform((data) => ({
	id: data.id,
	version: data.version,
	timestamp: data.timestamp,
	isLatest: data.is_latest,
	blockId: data.block_id,
	profileId: data.profile_id,
	query: data.query,
	status: data.status,
	executionTimeMs: data.execution_time_ms,
	error: data.error,
}));

export type InferenceRun = z.infer<typeof inferenceRunSchema>;
