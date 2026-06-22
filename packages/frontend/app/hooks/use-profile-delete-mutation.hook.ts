import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteProfile } from "~/api/profiles/delete-profile.api";
import type { ProfileSummary } from "~/schemas/domain/profile.schema";

export function useProfileDeleteMutation() {
	const queryKey = ["profiles", "summary"];
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (profileId: string) => deleteProfile(profileId),
		onMutate: async (deletedProfileId: string) => {
			await queryClient.cancelQueries({ queryKey });
			const previousProfiles =
				queryClient.getQueryData<ProfileSummary[]>(queryKey);

			queryClient.setQueryData<ProfileSummary[]>(queryKey, (oldProfiles) =>
				oldProfiles
					? oldProfiles.filter((profile) => profile.id !== deletedProfileId)
					: [],
			);

			return { previousProfiles };
		},
		onError: (error) => {
			console.error("Failed to delete profile:", error);
		},
	});
}
