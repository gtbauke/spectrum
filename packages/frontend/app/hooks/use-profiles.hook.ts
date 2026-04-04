import { useQuery } from "@tanstack/react-query";
import { getProfile } from "~/api/profiles/get-profile.api";
import { listProfileSummaries } from "~/api/profiles/summary.api";

export function useProfiles() {
	return useQuery({
		queryKey: ["profiles"],
		queryFn: () => listProfileSummaries(),
	});
}

export function useProfile(id: string | null) {
	return useQuery({
		queryKey: ["profile", id],
		queryFn: () => getProfile(id!),
		enabled: !!id,
	});
}
