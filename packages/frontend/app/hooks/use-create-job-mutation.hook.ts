import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createJobs } from "~/api/profiles/jobs/create-jobs.api";
import type { CreateJobDto } from "~/schemas/dtos/job.dto";

export function useCreateJobMutation(profileId: string) {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: (jobs: CreateJobDto[]) => createJobs(profileId, jobs),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["profile", profileId] });
		},
		onError: (error) => {
			console.error("Failed to create job:", error);
		},
	});
}
