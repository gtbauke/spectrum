import { type InfiniteData, useInfiniteQuery } from "@tanstack/react-query";
import { fetchProfilesSummary, type ProfileFilters } from "~/api/profiles.api";
import type { PaginatedResponse } from "~/api/types.api";
import type { ProfileSummary } from "~/schemas/responses/profiles/profile-summary.schema";

export function useInfiniteProfiles(filters: ProfileFilters) {
	return useInfiniteQuery<
		PaginatedResponse<ProfileSummary>,
		Error,
		InfiniteData<PaginatedResponse<ProfileSummary>>,
		readonly [string, ProfileFilters],
		number
	>({
		queryKey: ["profiles", filters] as const,
		queryFn: fetchProfilesSummary,
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
