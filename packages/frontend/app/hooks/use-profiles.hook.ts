import { useInfiniteQuery } from "@tanstack/react-query";
import { listProfiles } from "~/api/profiles/list-profiles.api";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";

export function useInfiniteProfiles(filters: ProfileFilter = {}) {
	const limit = 20;

	return useInfiniteQuery({
		queryKey: ["profiles", filters],
		queryFn: ({ pageParam = 0 }) =>
			listProfiles(filters, {
				offset: pageParam as number,
				limit,
			}),
		getNextPageParam: (lastPage, allPages) => {
			const loadedCount = allPages.length * limit;
			return loadedCount < lastPage.total ? loadedCount : undefined;
		},
		initialPageParam: 0,
	});
}
