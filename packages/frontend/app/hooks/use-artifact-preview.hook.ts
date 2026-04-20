import { useQuery } from "@tanstack/react-query";
import { getArtifactPreview } from "~/api/datasets/get-artifact-preview.api";

export function useArtifactPreview(
	datasetId: string,
	artifactId: string | null,
	limit: number = 50,
	offset: number = 0,
) {
	return useQuery({
		queryKey: ["artifact-preview", datasetId, artifactId, limit, offset],
		queryFn: async () => {
			if (!artifactId) return null;
			return await getArtifactPreview(datasetId, artifactId, limit, offset);
		},
		enabled: !!artifactId,
	});
}
