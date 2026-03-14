import type { QueryFunctionContext } from "@tanstack/react-query";
import type { Profile } from "~/schemas/generated/profile.schema";
import type { ProfileDatasetRole } from "~/schemas/generated/profile-dataset-role.schema";
import type { ProfileVisibility } from "~/schemas/generated/profile-visibility.schema";
import type { ProfileStatus } from "../schemas/generated/profile-status.schema";
import { apiRequest } from "./fetch.api";
import type { PaginatedResponse } from "./types.api";

export type ProfileFilters = {
	version?: number;
	name?: string;
	description?: string;
	status?: ProfileStatus;
	visibility?: ProfileVisibility;
	role?: ProfileDatasetRole;
	only_me?: boolean;
};

export const DEFAULT_PROFILE_FILTERS: ProfileFilters = {
	status: "active",
	visibility: "public",
	only_me: false,
};

export async function fetchProfiles({
	pageParam = 1,
	queryKey,
}: QueryFunctionContext<readonly [string, ProfileFilters], number>) {
	const [_key, filters] = queryKey;
	const { name, description, only_me, role, status, version, visibility } =
		filters;

	const final_only_me = only_me ?? DEFAULT_PROFILE_FILTERS.only_me;
	const final_status = status ?? DEFAULT_PROFILE_FILTERS.status;
	const final_visibility = visibility ?? DEFAULT_PROFILE_FILTERS.visibility;

	const params = new URLSearchParams({
		page: pageParam.toString(),
		size: "20",
		...(name && { name }),
		...(description && { description }),
		...(final_only_me && { only_me: final_only_me.toString() }),
		...(role && { role }),
		...(final_status && { status: final_status }),
		...(version && { version: version.toString() }),
		...(final_visibility && { visibility: final_visibility }),
	});

	return apiRequest<PaginatedResponse<Profile>>(`/profiles?${params}`);
}

export async function fetchProfilesPage({
	filters,
	page,
}: {
	filters: ProfileFilters;
	page: number;
}) {
	const { name, description, only_me, role, status, version, visibility } =
		filters;

	const final_only_me = only_me ?? DEFAULT_PROFILE_FILTERS.only_me;
	const final_status = status ?? DEFAULT_PROFILE_FILTERS.status;
	const final_visibility = visibility ?? DEFAULT_PROFILE_FILTERS.visibility;

	const params = new URLSearchParams({
		page: page.toString(),
		size: "20",
		...(name && { name }),
		...(description && { description }),
		...(final_only_me && { only_me: final_only_me.toString() }),
		...(role && { role }),
		...(final_status && { status: final_status }),
		...(version && { version: version.toString() }),
		...(final_visibility && { visibility: final_visibility }),
	});

	return apiRequest<PaginatedResponse<Profile>>(`/profiles?${params}`);
}
