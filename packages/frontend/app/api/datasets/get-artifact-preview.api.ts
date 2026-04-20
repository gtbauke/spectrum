import { safeApiRequest } from "~/api/fetch.api";
import {
	artifactPreviewResponseSchema,
	type ArtifactPreviewResponse,
} from "~/schemas/domain/dataset.schema";

export async function getArtifactPreview(
	datasetId: string,
	artifactId: string,
	limit: number = 50,
	offset: number = 0,
): Promise<ArtifactPreviewResponse> {
	const params = new URLSearchParams({
		limit: limit.toString(),
		offset: offset.toString(),
	});

	return await safeApiRequest(
		`/datasets/${datasetId}/artifacts/${artifactId}/preview?${params}`,
		artifactPreviewResponseSchema,
	);
}
