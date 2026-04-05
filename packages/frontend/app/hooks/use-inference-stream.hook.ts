import { useEffect, useRef } from "react";
import { inferenceResultSchema } from "~/schemas/domain/inference-result.schema";
import { useEditorStore } from "~/stores/editor.store";

const BASE_URL =
	import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export function useInferenceStream(
	profileId: string,
	blockId: string,
	runId?: string,
) {
	const updateBlock = useEditorStore((state) => state.updateBlock);
	const eventSourceRef = useRef<EventSource | null>(null);

	useEffect(() => {
		if (!runId) return;

		const url = `${BASE_URL}/profiles/${profileId}/blocks/${blockId}/runs/${runId}/stream`;
		const eventSource = new EventSource(url, { withCredentials: true });
		eventSourceRef.current = eventSource;

		eventSource.onmessage = (event) => {
			try {
				const data = JSON.parse(event.data);

				if (data.error) {
					updateBlock(
						blockId,
						{
							status: "failed",
							error: data.error,
						},
						{ recordHistory: false },
					);
					eventSource.close();
					return;
				}

				const results = data.results
					? data.results.map((r: any) => inferenceResultSchema.parse(r))
					: undefined;

				updateBlock(
					blockId,
					{
						status: data.status,
						executionTimeMs: data.execution_time_ms,
						error: data.error,
						results: results,
					},
					{ recordHistory: false },
				);

				if (data.status === "completed" || data.status === "failed") {
					eventSource.close();
				}
			} catch (err) {
				console.error("Failed to parse SSE message", err);
			}
		};

		eventSource.onerror = (err) => {
			console.error("SSE Error", err);
			updateBlock(
				blockId,
				{
					status: "failed",
					error: "Connection lost while streaming results",
				},
				{ recordHistory: false },
			);
			eventSource.close();
		};

		return () => {
			eventSource.close();
		};
	}, [profileId, blockId, runId, updateBlock]);

	return null;
}
