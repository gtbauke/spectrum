import { safeApiRequest } from "~/api/fetch.api";
import { datasetSchema, type Dataset } from "~/schemas/domain/dataset.schema";

export type UpdateDatasetDto = {
	name?: string;
	description?: string;
};

export async function updateDataset(
	datasetId: string,
	data: UpdateDatasetDto,
): Promise<Dataset> {
	return await safeApiRequest(
		`/datasets/${datasetId}`,
		datasetSchema,
		{
			method: "PUT",
			body: JSON.stringify(data),
		}
	);
}
