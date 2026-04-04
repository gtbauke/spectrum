import { safeApiRequest } from "~/api/fetch.api";
import { runSchema } from "~/schemas/domain/job.schema";

export type CreateRunParams = {
	profileId: string;
	jobId: string;
};

export async function createRun({ profileId, jobId }: CreateRunParams) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/jobs/${jobId}/runs`,
		runSchema,
		{ method: "POST" },
	);

	return response;
}
