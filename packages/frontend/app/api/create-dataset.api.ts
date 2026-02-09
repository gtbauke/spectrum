import {
	type CreateDatasetData,
	datasetSchema,
} from "~/schemas/dataset.schema";
import { apiRequest } from "./base.api";

export async function createDataset(data: CreateDatasetData, file: File) {
	try {
		const formData = new FormData();
		formData.append("name", data.name);
		formData.append("file", file);

		const response = await apiRequest(
			"/datasets/upload",
			"POST",
			datasetSchema,
			formData,
		);

		return response;
	} catch (error) {
		console.error("Error creating dataset:", error);
		throw error;
	}
}
