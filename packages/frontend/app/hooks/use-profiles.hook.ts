import {
	type InfiniteData,
	keepPreviousData,
	useInfiniteQuery,
	useQuery,
} from "@tanstack/react-query";
import {
	fetchProfiles,
	fetchProfilesPage,
	type ProfileFilters,
} from "~/api/profiles.api";
import type { PaginatedResponse } from "~/api/types.api";
import type { Profile } from "~/schemas/models/profile.schema";

export function useProfiles(filters: ProfileFilters, page: number) {
	return useQuery({
		queryKey: ["profiles", filters, page] as const,
		queryFn: () => fetchProfilesPage({ filters, page }),
		placeholderData: keepPreviousData,
	});
}

export function useInfiniteProfiles(filters: ProfileFilters) {
	return useInfiniteQuery<
		PaginatedResponse<Profile>,
		Error,
		InfiniteData<PaginatedResponse<Profile>>,
		readonly [string, ProfileFilters],
		number
	>({
		queryKey: ["profiles", filters] as const,
		queryFn: fetchProfiles,
		initialPageParam: 1,
		getNextPageParam: (lastPage) => {
			if (lastPage.page < lastPage.pages) {
				return lastPage.page + 1;
			}

			return undefined;
		},
		placeholderData: (previousData) => previousData,
	});
}
