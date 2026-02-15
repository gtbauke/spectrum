import { type JobRun, jobRunSchema } from "~/schemas/job-run.schema";
import { apiRequest } from "./base.api";

export async function getJobRunHistory(modelId: string): Promise<JobRun[]> {
	const response = await apiRequest(
		`/models/${modelId}/runs`,
		"GET",
		jobRunSchema.array(),
	);

	return response;
}
