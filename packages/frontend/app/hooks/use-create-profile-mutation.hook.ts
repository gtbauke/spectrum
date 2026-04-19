import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProfile } from "~/api/profiles/create-profile.api";
import type { CreateProfileDto } from "~/schemas/dtos/profile.dto";

export function useCreateProfileMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async (data: CreateProfileDto) => createProfile(data),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
		},
		onError: (error) => {
			console.error("Failed to create profile:", error);
		},
	});
}
