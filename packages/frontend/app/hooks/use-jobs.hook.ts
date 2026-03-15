import { useQuery } from "@tanstack/react-query";
import { type FetchJobsPageOptions, fetchJobsPage } from "~/api/jobs.api";

export function useJobs({ filters, page, where }: FetchJobsPageOptions) {
	return useQuery({
		queryKey: ["jobs", where.profile.id, filters, page] as const,
		queryFn: () => fetchJobsPage({ filters, where, page }),
		placeholderData: (previousData, previousQuery) => {
			const previousProfileId = previousQuery?.queryKey[1];

			if (previousProfileId === where.profile.id) {
				return previousData;
			}

			return undefined;
		},
	});
}
