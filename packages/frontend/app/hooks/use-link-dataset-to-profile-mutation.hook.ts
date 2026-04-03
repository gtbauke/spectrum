import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProfile } from "~/api/profiles/create-profile.api";
import { linkDatasetToProfile } from "~/api/profiles/link-dataset-to-profile.api";
import type { LinkDatasetToProfileDto } from "~/schemas/dtos/profile.dto";

type ProfileCreationParams =
	| { id: string }
	| { name: string; description?: string };

type UseLinkDatasetToProfileMutationParams = {
	profile: ProfileCreationParams;
	data: LinkDatasetToProfileDto;
};

export function useLinkDatasetToProfileMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async ({
			data,
			profile,
		}: UseLinkDatasetToProfileMutationParams) => {
			if ("id" in profile) {
				return linkDatasetToProfile(profile.id, data);
			}

			const newProfile = await createProfile({
				name: profile.name,
				description: profile.description || "",
			});

			return linkDatasetToProfile(newProfile.id, data);
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
			queryClient.invalidateQueries({ queryKey: ["datasets"] });
		},
		onError: (error) => {
			console.error("Failed to link dataset to profile:", error);
		},
	});
}
