import { useEffect, useRef } from "react";
import { BASE_URL } from "~/api/fetch.api";
import { inferenceResultSchema } from "~/schemas/domain/inference-result.schema";
import { useEditorStore } from "~/stores/editor.store";
import type { InferenceErrorType } from "~/utils/types/editor.types";

function classifyError(
	errorMsg?: string,
	explicitType?: string,
): InferenceErrorType {
	if (
		explicitType &&
		["syntax", "execution", "network", "unknown"].includes(explicitType)
	) {
		return explicitType as InferenceErrorType;
	}
	if (!errorMsg) return "unknown";
	const lower = errorMsg.toLowerCase();
	if (
		lower.includes("syntax") ||
		lower.includes("parse") ||
		lower.includes("expected") ||
		lower.includes("invalid query") ||
		lower.includes("tokenizer")
	) {
		return "syntax";
	}
	if (
		lower.includes("connection lost") ||
		lower.includes("network") ||
		lower.includes("failed to fetch") ||
		lower.includes("timeout") ||
		lower.includes("reconnecting")
	) {
		return "network";
	}
	if (
		lower.includes("execution") ||
		lower.includes("worker") ||
		lower.includes("prediction") ||
		lower.includes("solver") ||
		lower.includes("index") ||
		lower.includes("failed")
	) {
		return "execution";
	}
	return "unknown";
}

export function useInferenceStream(
	profileId: string,
	blockId: string,
	runId?: string,
) {
	const updateBlock = useEditorStore((state) => state.updateBlock);
	const eventSourceRef = useRef<EventSource | null>(null);
	const retryCountRef = useRef(0);
	const retryTimerRef = useRef<NodeJS.Timeout | null>(null);

	useEffect(() => {
		if (!runId) return;

		retryCountRef.current = 0;
		let isUnmounted = false;

		const connect = () => {
			const url = `${BASE_URL}/profiles/${profileId}/blocks/${blockId}/runs/${runId}/stream`;
			const eventSource = new EventSource(url, { withCredentials: true });
			eventSourceRef.current = eventSource;

			eventSource.onmessage = (event) => {
				try {
					const data = JSON.parse(event.data);

					retryCountRef.current = 0;

					if (data.error) {
						const errorType = classifyError(data.error, data.error_type);
						updateBlock(
							blockId,
							{
								status: "failed",
								error: data.error,
								errorType: errorType,
								errorDetails: data.error_details,
							},
							{ recordHistory: false },
						);
						eventSource.close();
						return;
					}

					const results = data.results
						? data.results.map((r: any) => inferenceResultSchema.parse(r))
						: undefined;

					const errorType = data.error
						? classifyError(data.error, data.error_type)
						: undefined;

					updateBlock(
						blockId,
						{
							status: data.status,
							executionTimeMs: data.execution_time_ms,
							error: data.error,
							errorType: errorType,
							errorDetails: data.error_details,
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
				eventSource.close();

				if (isUnmounted) return;

				const maxRetries = 3;
				if (retryCountRef.current < maxRetries) {
					retryCountRef.current += 1;
					const backoffMs = Math.pow(2, retryCountRef.current - 1) * 1000;

					updateBlock(
						blockId,
						{
							status: "reconnecting",
							error: `Connection lost. Attempting reconnection (${retryCountRef.current}/${maxRetries})...`,
							errorType: "network",
						},
						{ recordHistory: false },
					);

					retryTimerRef.current = setTimeout(() => {
						if (!isUnmounted) {
							connect();
						}
					}, backoffMs);
				} else {
					updateBlock(
						blockId,
						{
							status: "failed",
							error:
								"Connection lost while streaming results. Server or network unavailable.",
							errorType: "network",
							errorDetails:
								"The SSE connection was interrupted multiple times. Please check your network connection and server health.",
						},
						{ recordHistory: false },
					);
				}
			};
		};

		connect();

		return () => {
			isUnmounted = true;
			if (retryTimerRef.current) clearTimeout(retryTimerRef.current);
			if (eventSourceRef.current) eventSourceRef.current.close();
		};
	}, [profileId, blockId, runId, updateBlock]);

	return null;
}
