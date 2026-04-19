import { datasetSchema } from "~/schemas/domain/dataset.schema";
import { safeApiRequest } from "../fetch.api";

export async function getDataset(id: string) {
	const response = await safeApiRequest(`/datasets/${id}`, datasetSchema);
	return response;
}
