import { type Job, jobSchema } from "~/schemas/job.schema";
import { apiRequest } from "./base.api";

export async function getJob(datasetId: string, jobId: string): Promise<Job> {
	const response = await apiRequest(
		`/datasets/${datasetId}/jobs/${jobId}`,
		"GET",
		jobSchema,
	);

	return response;
}
