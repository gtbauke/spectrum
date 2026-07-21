import { safeApiRequest } from "~/api/fetch.api";
import { inferenceRunSchema } from "~/schemas/domain/inference-run.schema";

export async function getLatestInferenceRun(profileId: string, blockId: string) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/blocks/${blockId}/runs/latest`,
		inferenceRunSchema,
		{
			method: "GET",
		},
	);

	return response;
}
