import { type Model, modelSchema } from "~/schemas/model.schema";
import { apiRequest } from "./base.api";

export async function getModel(modelId: string): Promise<Model> {
	const response = await apiRequest(`/models/${modelId}`, "GET", modelSchema);

	return response;
}
