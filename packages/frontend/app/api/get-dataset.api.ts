import { type Dataset, datasetSchema } from "~/schemas/dataset.schema";
import { apiRequest } from "./base.api";

export async function getDataset(datasetId: string): Promise<Dataset> {
	const response = await apiRequest(
		`/datasets/${datasetId}`,
		"GET",
		datasetSchema,
	);

	return response;
}
