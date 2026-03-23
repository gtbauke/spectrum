import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProfileFromDataset } from "~/api/profiles/from-dataset.api";
import { useEditorStore } from "~/stores/editor.store";
import type { CreateProfileFromDatasetDto } from "~/schemas/dtos/profile.dto";

export function useCreateProfileFromDatasetMutation() {
	const queryClient = useQueryClient();
	const openTab = useEditorStore((s) => s.openTab);

	return useMutation({
		mutationFn: ({ file, data }: { file: File; data: CreateProfileFromDatasetDto }) =>
			createProfileFromDataset(file, data),

		onSuccess: (newProfile) => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
			queryClient.invalidateQueries({ queryKey: ["datasets"] });

			openTab({
				type: "profile",
				id: newProfile.id,
				data: {
					tabId: newProfile.id,
					profileId: newProfile.id,
					versionId: newProfile.id,
					isDirty: false,
					activeBlockId: null,
					blocks: [],
					profile: newProfile,
					future: [],
					past: [],
				},
			});
		},
		onError: (error) => {
			console.error("Failed to upload dataset:", error);
		},
	});
}
