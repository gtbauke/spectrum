import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { getRunStream } from "~/api/profiles/jobs/runs/get-run.api";
import { type Run, runSchema } from "~/schemas/domain/job.schema";

type UseStreamRunOptions = {
	profileId: string;
	jobId: string;
	runId?: string;

	getInitialData?: () => Run;
};

export function useStreamRun({ profileId, jobId, runId }: UseStreamRunOptions) {
	const [streamedRun, setStreamedRun] = useState<Run | null>(null);
	const queryClient = useQueryClient();

	useEffect(() => {
		const value = runId ? null : null;
		setStreamedRun(value);
	}, [runId]);

	useEffect(() => {
		if (!runId) return;

		const eventSource = getRunStream({
			profileId,
			jobId,
			runId,
		});

		eventSource.onmessage = (event) => {
			try {
				const data = JSON.parse(event.data);
				if (data.error) {
					console.error("Error in run stream:", data.error);
					eventSource.close();
					return;
				}

				const updatedRun = runSchema.parse(data);
				setStreamedRun(updatedRun);

				if (
					updatedRun.status === "finished" ||
					updatedRun.status === "failed"
				) {
					eventSource.close();

					queryClient.invalidateQueries({
						queryKey: ["profile"],
					});
				}
			} catch (err) {
				console.error("Failed to parse SSE message", err);
				eventSource.close();
			}
		};

		eventSource.onerror = (err) => {
			console.error("SSE Error", err);
			eventSource.close();
		};

		return () => {
			eventSource.close();
		};
	}, [profileId, jobId, runId, queryClient]);

	return {
		run: streamedRun,
	};
}
