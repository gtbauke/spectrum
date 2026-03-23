import { safeApiRequest } from "~/api/fetch.api";
import { paginatedResponseSchema } from "~/schemas/common/pagination.schema";
import { modelSchema } from "~/schemas/domain/model.schema";

export async function listModels(profileId: string) {
	return safeApiRequest(
		`/profiles/${profileId}/models`,
		paginatedResponseSchema(modelSchema),
	);
}
