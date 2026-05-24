import { useQuery } from "@tanstack/react-query";
import { getProfile } from "~/api/profiles/get-profile.api";
import { listProfiles } from "~/api/profiles/list-profiles.api";
import { listProfileSummaries } from "~/api/profiles/summary.api";

type UseProfilesOptions = {
	mode?: "summary" | "full";
};

export function useProfiles(options: UseProfilesOptions = { mode: "summary" }) {
	return useQuery({
		queryKey: ["profiles", options.mode],
		queryFn: async () => {
			if (options.mode === "summary") {
				return await listProfileSummaries();
			}

			return await listProfiles();
		},
	});
}

export function useProfile(id: string | null) {
	return useQuery({
		queryKey: ["profile", id],
		queryFn: () => getProfile(id!),
		enabled: !!id,
	});
}
