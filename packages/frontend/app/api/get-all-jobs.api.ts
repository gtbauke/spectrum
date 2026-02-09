import {
	getJobsForDatasetResponseSchema,
	type Job,
} from "~/schemas/job.schema";
import { apiRequest } from "./base.api";

export async function getAllJobsForDataset(datasetId: string): Promise<Job[]> {
	try {
		const response = await apiRequest(
			`/datasets/${datasetId}/jobs`,
			"GET",
			getJobsForDatasetResponseSchema,
		);

		return response;
	} catch (error) {
		console.error("Error fetching jobs for dataset:", error);
		throw error;
	}
}
