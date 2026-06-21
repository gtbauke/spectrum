import { BASE_URL } from "~/api/fetch.api";

export type GetRunStreamParams = {
	profileId: string;
	jobId: string;
	runId: string;
};

export function getRunStream({ profileId, jobId, runId }: GetRunStreamParams) {
	const url = `${BASE_URL}/profiles/${profileId}/jobs/${jobId}/runs/${runId}/stream`;
	const eventSource = new EventSource(url, { withCredentials: true });

	return eventSource;
}
