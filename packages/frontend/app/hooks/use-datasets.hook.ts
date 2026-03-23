import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import { listDatasets } from "~/api/datasets/list-datasets.api";
import type { DatasetFilterInput } from "~/schemas/dtos/dataset.dto";

export function useDatasets(filters: DatasetFilterInput = {}, pagination: { limit?: number; offset?: number } = {}) {
	return useQuery({
		queryKey: ["datasets", filters, pagination] as const,
		queryFn: () => listDatasets(filters, pagination),
	});
}

export function useInfiniteDatasets(filters: DatasetFilterInput = {}) {
  const limit = 20;

  return useInfiniteQuery({
    queryKey: ["datasets", filters],
    queryFn: ({ pageParam = 0 }) =>
      listDatasets(filters, {
        offset: pageParam as number,
        limit,
      }),
    getNextPageParam: (lastPage, allPages) => {
      const loadedCount = allPages.length * limit;
      return loadedCount < lastPage.total ? loadedCount : undefined;
    },
    initialPageParam: 0,
  });
}
