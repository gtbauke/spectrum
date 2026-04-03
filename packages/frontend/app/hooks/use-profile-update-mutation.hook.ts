import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateProfile } from "~/api/profiles/update-profile.api";
import type { UpdateProfileDto } from "~/schemas/dtos/profile.dto";

type UpdateProfileParams = {
	profileId: string;
	data: UpdateProfileDto;
};

export function useProfileUpdateMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async ({ profileId, data }: UpdateProfileParams) => {
			console.log("Updating profile with data:", { profileId, data });
			return await updateProfile(profileId, data);
		},
		onSuccess: (updatedProfile) => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
		},
		onError: (error) => {
			console.error("Failed to update profile:", error);
		},
	});
}
