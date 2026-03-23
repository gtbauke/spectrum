import { paginatedResponseSchema } from "../../schemas/common/pagination.schema";
import { profileSchema } from "../../schemas/domain/profile.schema";
import type { ProfileFilter } from "../../schemas/dtos/profile.dto";
import { safeApiRequest } from "../fetch.api";

export async function listProfiles(
	filters: ProfileFilter = {},
	pagination: { limit?: number; offset?: number } = {},
) {
	const params = new URLSearchParams();

	if (filters.name) params.append("name", filters.name);
	if (filters.description) params.append("description", filters.description);
	if (filters.onlyMe) params.append("mine", "true");
	if (filters.status) params.append("mode", filters.status);

	if (pagination.limit) params.append("limit", String(pagination.limit));
	if (pagination.offset) params.append("offset", String(pagination.offset));

	const endpoint = `/profiles?${params.toString()}`;
	return safeApiRequest(endpoint, paginatedResponseSchema(profileSchema));
}
