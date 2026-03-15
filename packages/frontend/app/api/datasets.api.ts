import type { QueryFunctionContext } from "@tanstack/react-query";
import type { ArtifactType } from "~/schemas/models/artifact-type.schema";
import type { Dataset } from "~/schemas/models/dataset.schema";
import { apiRequest } from "./fetch.api";
import type { PaginatedResponse } from "./types.api";

export type DatasetFilters = {
	minSize?: number;
	maxSize?: number;
	name?: string;
	description?: string;
	artifactType?: ArtifactType;
	checksum?: string;
};

export async function fetchDatasets({
	pageParam = 1,
	queryKey,
}: QueryFunctionContext<readonly [string, DatasetFilters], number>) {
	const [_key, filters] = queryKey;
	const { name, minSize, maxSize, artifactType, checksum, description } =
		filters;

	const params = new URLSearchParams({
		page: pageParam.toString(),
		size: "20",
		...(name && { name }),
		...(artifactType && { artifact_type: artifactType }),
		...(checksum && { checksum }),
		...(description && { description }),
		...(minSize && { min_size: minSize.toString() }),
		...(maxSize && { max_size: maxSize.toString() }),
	});

	return apiRequest<PaginatedResponse<Dataset>>(`/datasets/search?${params}`);
}

export async function fetchDatasetsPage({
	filters,
	page,
}: {
	filters: DatasetFilters;
	page: number;
}) {
	const { name, minSize, maxSize, artifactType, checksum, description } =
		filters;

	const params = new URLSearchParams({
		page: page.toString(),
		size: "20",
		...(name && { name }),
		...(artifactType && { artifact_type: artifactType }),
		...(checksum && { checksum }),
		...(description && { description }),
		...(minSize && { min_size: minSize.toString() }),
		...(maxSize && { max_size: maxSize.toString() }),
	});

	return apiRequest<PaginatedResponse<Dataset>>(`/datasets/search?${params}`);
}
