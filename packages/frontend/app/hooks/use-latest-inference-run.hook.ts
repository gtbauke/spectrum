import { useQuery } from "@tanstack/react-query";
import { getLatestInferenceRun } from "~/api/profiles/blocks/get-latest-inference-run.api";

export function useLatestInferenceRun(
	profileId: string,
	blockId: string,
	options?: { enabled?: boolean },
) {
	return useQuery({
		queryKey: ["profiles", profileId, "blocks", blockId, "runs", "latest"],
		queryFn: () => getLatestInferenceRun(profileId, blockId),
		retry: false,
		enabled: options?.enabled,
	});
}
