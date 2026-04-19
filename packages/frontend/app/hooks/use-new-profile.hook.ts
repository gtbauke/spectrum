import { useCallback } from "react";
import { useEditorStore } from "~/stores/editor.store";
import { useCreateProfileMutation } from "./use-create-profile-mutation.hook";

export function useNewProfile() {
	const openProfileTab = useEditorStore((s) => s.openProfileTab);
	const { mutate: createProfile, isPending } = useCreateProfileMutation();

	const handler = useCallback(() => {
		createProfile(
			{
				name: "Untitled Profile",
				description: "",
			},
			{
				onSuccess: (response) => {
					openProfileTab(response.id);
				},
			},
		);
	}, [createProfile, openProfileTab]);

	return { openNewProfile: handler, isPending };
}
