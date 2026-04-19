import { useQuery } from "@tanstack/react-query";
import { getRecentProfiles } from "~/api/profiles/get-recent-profiles.api";

export function useRecentProfiles() {
	return useQuery({
		queryFn: () => getRecentProfiles(),
		queryKey: ["recent-profiles"] as const,
		staleTime: 1000 * 60 * 60,
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		refetchInterval: false,
	});
}
