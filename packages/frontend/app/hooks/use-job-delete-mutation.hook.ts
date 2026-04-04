import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
	type DeleteJobParams,
	deleteJob,
} from "~/api/profiles/jobs/delete.api";

export function useJobDeleteMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (params: DeleteJobParams) => deleteJob(params),
		onSuccess: (_, params) => {
			queryClient.invalidateQueries({
				queryKey: ["profile", params.profileId],
			});
		},
	});
}
