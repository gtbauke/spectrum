import type { QueryFunctionContext } from "@tanstack/react-query";
import type { CreateProfileFromDatasetInput } from "~/schemas/create-profile-from-dataset.schema";
import type { Profile } from "~/schemas/models/profile.schema";
import type { ProfileDatasetRole } from "~/schemas/models/profile-dataset-role.schema";
import type { ProfileVisibility } from "~/schemas/models/profile-visibility.schema";
import { profileSummarySchema } from "~/schemas/responses/profiles/profile-summary.schema";
import type { ProfileStatus } from "../schemas/models/profile-status.schema";
import { apiRequest, safeApiRequest } from "./fetch.api";
import { paginatedResponseSchema } from "./types.api";

export type ProfileFilters = {
	version?: number;
	name?: string;
	description?: string;
	status?: ProfileStatus;
	visibility?: ProfileVisibility;
	role?: ProfileDatasetRole;
	onlyMe?: boolean;
};

export const DEFAULT_PROFILE_FILTERS: ProfileFilters = {
	status: "active",
	visibility: "public",
	onlyMe: false,
};

export async function fetchProfilesSummary({
	pageParam = 1,
	queryKey,
}: QueryFunctionContext<readonly [string, ProfileFilters], number>) {
	const [_, filters] = queryKey;
	const { name, description, onlyMe, role, status, version, visibility } =
		filters;

	const finalOnlyMe = onlyMe ?? DEFAULT_PROFILE_FILTERS.onlyMe;
	const finalStatus = status ?? DEFAULT_PROFILE_FILTERS.status;
	const finalVisibility = visibility ?? DEFAULT_PROFILE_FILTERS.visibility;

	const params = new URLSearchParams({
		page: pageParam.toString(),
		size: "20",
		...(name && { name }),
		...(description && { description }),
		...(finalOnlyMe && { only_me: finalOnlyMe.toString() }),
		...(role && { role }),
		...(finalStatus && { status: finalStatus }),
		...(version && { version: version.toString() }),
		...(finalVisibility && { visibility: finalVisibility }),
	});

	return safeApiRequest(
		`/profiles/summary?${params}`,
		paginatedResponseSchema(profileSummarySchema),
	);
}

export type CreateProfileFromDatasetPayload = CreateProfileFromDatasetInput & {
	file: File;
};

export async function createProfileFromDataset(
	payload: CreateProfileFromDatasetPayload,
) {
	console.log(payload);
	const formData = new FormData();

	formData.append("file", payload.file);
	formData.append("dataset_name", payload.datasetName);

	if (payload.datasetDescription) {
		formData.append("dataset_description", payload.datasetDescription);
	}

	formData.append("dataset_role", payload.datasetRole);

	return apiRequest<Profile>("/profiles/from-dataset", {
		method: "POST",
		body: formData,
	});
}
