import { useQuery } from "@tanstack/react-query";
import { listJobs } from "~/api/profiles/jobs/list-jobs.api";
import type { JobFilter } from "~/schemas/dtos/job.dto";

export type UseJobsOptions = {
    profileId: string;
    filters?: JobFilter;
    page?: number;
};

export function useJobs({ profileId, filters, page = 1 }: UseJobsOptions) {
	return useQuery({
		queryKey: ["jobs", profileId, filters, page] as const,
		queryFn: () => listJobs(profileId), // Note: listJobs might need to accept filters/pagination eventually
		placeholderData: (previousData, previousQuery) => {
			const previousProfileId = previousQuery?.queryKey[1];

			if (previousProfileId === profileId) {
				return previousData;
			}

			return undefined;
		},
	});
}
