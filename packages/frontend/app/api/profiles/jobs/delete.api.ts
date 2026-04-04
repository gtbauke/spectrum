import { apiRequest } from "~/api/fetch.api";

export type DeleteJobParams = {
	profileId: string;
	jobId: string;
};

export async function deleteJob({ profileId, jobId }: DeleteJobParams) {
	return apiRequest(`/profiles/${profileId}/jobs/${jobId}`, {
		method: "DELETE",
	});
}
