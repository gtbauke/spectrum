import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
	type CreateRunParams,
	createRun,
} from "~/api/profiles/jobs/runs/create-run.api";

export function useRunJobMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (params: CreateRunParams) => createRun(params),
		onSuccess: (_, params) => {
			queryClient.invalidateQueries({
				queryKey: ["profile", params.profileId],
			});
		},
	});
}
