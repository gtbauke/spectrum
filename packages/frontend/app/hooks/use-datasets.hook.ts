import {
	type InfiniteData,
	keepPreviousData,
	useInfiniteQuery,
	useQuery,
} from "@tanstack/react-query";
import {
	type DatasetFilters,
	fetchDatasets,
	fetchDatasetsPage,
} from "~/api/datasets.api";
import type { PaginatedResponse } from "~/api/types.api";
import type { Dataset } from "~/schemas/generated/dataset.schema";

export function useDatasets(filters: DatasetFilters, page: number) {
	return useQuery({
		queryKey: ["datasets", filters, page] as const,
		queryFn: () => fetchDatasetsPage({ filters, page }),
		placeholderData: keepPreviousData,
	});
}

export function useInfiniteDatasets(filters: DatasetFilters) {
	return useInfiniteQuery<
		PaginatedResponse<Dataset>,
		Error,
		InfiniteData<PaginatedResponse<Dataset>>,
		readonly [string, DatasetFilters],
		number
	>({
		queryKey: ["datasets", filters] as const,
		queryFn: fetchDatasets,
		initialPageParam: 1,
		getNextPageParam: (lastPage) => {
			if (lastPage.page < lastPage.pages) {
				return lastPage.page + 1;
			}

			return undefined;
		},
		placeholderData: (previousData) => previousData,
	});
}
