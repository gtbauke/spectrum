import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
	type CreateProfileFromDatasetPayload,
	createProfileFromDataset,
} from "~/api/profiles.api";
import { useEditorStore } from "~/stores/editor.store";

export function useCreateProfileFromDatasetMutation() {
	const queryClient = useQueryClient();
	const openTab = useEditorStore((s) => s.openTab);

	return useMutation({
		mutationFn: (payload: CreateProfileFromDatasetPayload) =>
			createProfileFromDataset(payload),

		onSuccess: (newProfile) => {
			queryClient.invalidateQueries({ queryKey: ["profiles"] });
			queryClient.invalidateQueries({ queryKey: ["datasets"] });

			openTab({
				type: "profile",
				id: newProfile.id,
				data: {
					name: newProfile.versions[0]?.name || "New Profile",
					profileId: newProfile.id,
					isDirty: false,
					activeBlockId: null,
					blocks: [],
					description: newProfile.versions[0]?.description || "",
					future: [],
					past: [],
					tabId: newProfile.id,
					versionId: newProfile.versions[0]?.id || "",
				},
			});
		},
		onError: (error) => {
			console.error("Failed to upload dataset:", error);
		},
	});
}
