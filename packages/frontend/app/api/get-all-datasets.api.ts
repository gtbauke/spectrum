import {
	type Dataset,
	getAllDatasetsResponseSchema,
} from "~/schemas/dataset.schema";
import { apiRequest } from "./base.api";

export async function getAllDatasets(): Promise<Dataset[]> {
	try {
		const response = await apiRequest(
			"/datasets",
			"GET",
			getAllDatasetsResponseSchema,
		);

		return response;
	} catch (error) {
		console.error("Error fetching datasets:", error);
		throw error;
	}
}
