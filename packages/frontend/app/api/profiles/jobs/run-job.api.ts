import { safeApiRequest } from "~/api/fetch.api";
import { runSchema } from "~/schemas/domain/job.schema";

export async function runJob(profileId: string, jobId: string) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/jobs/${jobId}/runs`,
		runSchema,
		{
			method: "POST",
		},
	);

	return response;
}
