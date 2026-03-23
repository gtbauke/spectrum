import { paginatedResponseSchema } from "~/schemas/common/pagination.schema";
import { datasetSchema } from "~/schemas/domain/dataset.schema";
import type { DatasetFilterInput } from "~/schemas/dtos/dataset.dto";
import { safeApiRequest } from "../fetch.api";

export async function listDatasets(
	filters: DatasetFilterInput = {},
	pagination: { limit?: number; offset?: number } = {},
) {
	const params = new URLSearchParams();

	if (filters.name) params.append("name", filters.name);
	if (filters.ownerId) params.append("owner_id", filters.ownerId);
	if (filters.visibility) params.append("visibility", filters.visibility);

	if (pagination.limit) params.append("limit", String(pagination.limit));
	if (pagination.offset) params.append("offset", String(pagination.offset));

	const endpoint = `/datasets?${params.toString()}`;
	return safeApiRequest(endpoint, paginatedResponseSchema(datasetSchema));
}
