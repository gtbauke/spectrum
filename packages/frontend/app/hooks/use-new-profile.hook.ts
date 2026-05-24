import { useCallback } from "react";
import { useCreateProfileMutation } from "./use-create-profile-mutation.hook";
import { useProfileQueryState } from "./use-profile-query-state.hook";

export function useNewProfile() {
	const { openTab } = useProfileQueryState();
	const { mutate: createProfile, isPending } = useCreateProfileMutation();

	const handler = useCallback(() => {
		createProfile(
			{
				name: "Untitled Profile",
				description: "",
			},
			{
				onSuccess: (response) => {
					openTab(response.id);
				},
			},
		);
	}, [createProfile, openTab]);

	return { openNewProfile: handler, isPending };
}
