import { safeApiRequest } from "~/api/fetch.api";
import { inferenceRunSchema } from "~/schemas/domain/inference-run.schema";

export async function createInferenceRun(profileId: string, blockId: string) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/blocks/${blockId}/runs`,
		inferenceRunSchema,
		{
			method: "POST",
		},
	);

	return response;
}
