import { safeApiRequest } from "~/api/fetch.api";
import { paginatedResponseSchema } from "~/schemas/common/pagination.schema";
import { jobSchema } from "~/schemas/domain/job.schema";

export async function listJobs(profileId: string) {
	return safeApiRequest(
		`/profiles/${profileId}/jobs`,
		paginatedResponseSchema(jobSchema),
	);
}
