import { useQuery } from "@tanstack/react-query";
import { getProfile } from "~/api/profiles/get-profile.api";
import { listProfiles } from "~/api/profiles/list-profiles.api";
import { listProfileSummaries } from "~/api/profiles/summary.api";

type UseProfilesOptions = {
	mode?: "summary" | "full";
};

// TODO: Implement pagination and filtering in the API and use it here
export function useProfiles(options: UseProfilesOptions = { mode: "summary" }) {
	return useQuery({
		queryKey: ["profiles", options.mode],
		queryFn: async () => {
			if (options.mode === "summary") {
				return await listProfileSummaries();
			}

			const profiles = await listProfiles(undefined, {
				limit: 1000,
			});

			return profiles.items;
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
