import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
	type CreateProfileFromDatasetPayload,
	createProfileFromDataset,
} from "~/api/profiles.api";
import { useProfileTabs } from "~/contexts/profile-tabs.context";

export function useCreateProfileFromDatasetMutation() {
	const queryClient = useQueryClient();
	const { openTab } = useProfileTabs();

	return useMutation({
		mutationFn: (payload: CreateProfileFromDatasetPayload) =>
			createProfileFromDataset(payload),

		onSuccess: (newProfile) => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
			queryClient.invalidateQueries({ queryKey: ["datasets"] });

			openTab({
				type: "profile",
				id: `profile-${newProfile.id}`,
				name: newProfile.versions[0]?.name || "New Profile",
				profileId: newProfile.id,
				profileVersion: newProfile.versions[0],
				isDirty: false,
			});
		},
		onError: (error) => {
			console.error("Failed to upload dataset:", error);
		},
	});
}
