import { type Model, modelSchema } from "~/schemas/model.schema";
import { apiRequest } from "./base.api";

export async function runModel(modelId: string): Promise<Model> {
	const response = await apiRequest(
		`/models/${modelId}/run`,
		"POST",
		modelSchema,
	);

	return response;
}
