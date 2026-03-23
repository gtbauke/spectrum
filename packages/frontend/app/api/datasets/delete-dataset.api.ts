import { apiRequest } from "../fetch.api";

export async function deleteDataset(datasetId: string) {
	await apiRequest(`/datasets/${datasetId}`, {
		method: "DELETE",
	});
}
