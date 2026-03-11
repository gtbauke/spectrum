import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { type DatasetFilters, fetchDatasetsPage } from "~/api/datasets.api";

export function useDatasets(filters: DatasetFilters, page: number) {
	return useQuery({
		queryKey: ["datasets", filters, page] as const,
		queryFn: () => fetchDatasetsPage({ filters, page }),
		placeholderData: keepPreviousData,
	});
}
