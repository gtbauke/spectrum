import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import { getProfile } from "~/api/profiles/get-profile.api";
import { listProfiles } from "~/api/profiles/list-profiles.api";
import { listProfileSummaries } from "~/api/profiles/summary.api";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";

export function useProfiles() {
	return useQuery({
		queryKey: ["profiles", "summary"],
		queryFn: async () => listProfileSummaries(),
	});
}

export function useFullProfiles(filters: ProfileFilter) {
	const limit = 20;

	return useInfiniteQuery({
		queryKey: ["profiles", "full"],
		queryFn: async ({ pageParam = 0 }) =>
			listProfiles(filters, {
				offset: pageParam as number,
				limit: 20,
			}),
		getNextPageParam: (lastPage, allPages) => {
			const loadedCount = allPages.length * limit;
			return loadedCount < lastPage.total ? loadedCount : undefined;
		},
		initialPageParam: 0,
	});
}

export function useProfile(id: string | null) {
	return useQuery({
		queryKey: ["profile", id],
		queryFn: () => getProfile(id!),
		enabled: !!id,
	});
}
