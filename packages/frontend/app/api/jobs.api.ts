import type { Job } from "~/schemas/models/job.schema";
import { apiRequest } from "./fetch.api";
import type { PaginatedResponse } from "./types.api";

export type JobFilters = {
	name?: string;
};

export type JobsWhere = {
	profile: {
		id: string;
	};
};

export type FetchJobsPageOptions = {
	filters?: JobFilters;
	where: JobsWhere;
	page: number;
};

export async function fetchJobsPage({
	filters = {},
	where,
	page,
}: FetchJobsPageOptions) {
	const { name } = filters;

	const params = new URLSearchParams({
		page: page.toString(),
		size: "20",
		...(name && { name }),
	});

	return apiRequest<PaginatedResponse<Job>>(
		`/profiles/${where.profile.id}/jobs?${params}`,
	);
}
