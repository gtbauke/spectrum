import { z } from "zod";
import { baseMutableObject } from "../common/base.schema";

export const modelMetricsParetoFrontSchema = z
	.object({
		DL: z.number(),
		Expression: z.string(),
		Fitness: z.number(),
		Size: z.number().int(),
		Latex: z.string(),
		Numpy: z.string(),
		Parameters: z.string(),
		Id: z.number().int(),
	})
	.transform((data) => {
		const parametersArray = JSON.parse(data.Parameters) as number[];
		if (!Array.isArray(parametersArray)) {
			throw new Error("Parameters field is not a valid JSON array");
		}

		return {
			dl: data.DL,
			expression: data.Expression,
			fitness: data.Fitness,
			size: data.Size,
			latex: data.Latex,
			numpy: data.Numpy,
			parameters: parametersArray,
			id: data.Id,
		};
	});

export const modelMetricsSchema = z
	.object({
		pareto_front: z.array(modelMetricsParetoFrontSchema),
	})
	.transform((data) => ({
		paretoFront: data.pareto_front,
	}));

export type ModelMetricsParetoFront = z.infer<
	typeof modelMetricsParetoFrontSchema
>;

export type ModelMetrics = z.infer<typeof modelMetricsSchema>;

export const modelSchema = baseMutableObject
	.extend({
		name: z.string(),
		profile_id: z.uuid(),
		generated_by: z.uuid(),
		path: z.string(),
		validation_path: z.string().nullable().optional(),
		metrics: modelMetricsSchema.nullable().optional(),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
		profileId: data.profile_id,
		generatedBy: data.generated_by,
		path: data.path,
		validationPath: data.validation_path,
		metrics: data.metrics,
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type Model = z.infer<typeof modelSchema>;
