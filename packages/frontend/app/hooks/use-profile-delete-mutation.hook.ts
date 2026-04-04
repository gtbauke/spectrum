import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteProfile } from "~/api/profiles/delete-profile.api";
import type { ProfileSummary } from "~/schemas/domain/profile.schema";

export function useProfileDeleteMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (profileId: string) => deleteProfile(profileId),
		onSuccess: async (_, profileId) => {
			queryClient.removeQueries({ queryKey: ["profile", profileId] });
			queryClient.setQueryData(
				["profiles"],
				(oldData: ProfileSummary[] | undefined) => {
					if (!oldData) {
						return oldData;
					}

					return oldData.filter((profile) => profile.id !== profileId);
				},
			);

			await queryClient.invalidateQueries({ queryKey: ["profiles"] });
		},
		onError: (error) => {
			console.error("Failed to delete profile:", error);
		},
	});
}
