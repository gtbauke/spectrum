import { z } from "zod";
import { baseImmutableObject } from "../common/base.schema";

export const inferenceResultRawSchema = baseImmutableObject.extend({
	run_id: z.string().uuid(),
	expression: z.string(),
	dl: z.number().nullable(),
	fitness: z.number().nullable(),
	latex: z.string().nullable(),
	numpy: z.string().nullable(),
	parameters: z.record(z.string(), z.number()).nullable(),
	size: z.number().int().nullable(),
	frequency: z.number().int().nullable(),
});

export type InferenceResultRaw = z.infer<typeof inferenceResultRawSchema>;

export const inferenceResultSchema = inferenceResultRawSchema.transform((data: InferenceResultRaw) => ({
	id: data.id,
	timestamp: data.timestamp,
	runId: data.run_id,
	expression: data.expression,
	dl: data.dl,
	fitness: data.fitness,
	latex: data.latex,
	numpy: data.numpy,
	parameters: data.parameters,
	size: data.size,
	frequency: data.frequency,
}));

export type InferenceResult = z.infer<typeof inferenceResultSchema>;
