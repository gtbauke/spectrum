import { apiRequest } from "./base.api";

export async function deleteDataset(datasetId: string) {
	try {
		await apiRequest(`/datasets/${datasetId}`, "DELETE");
	} catch (error) {
		console.error("Failed to delete dataset:", error);
		throw error;
	}
}
