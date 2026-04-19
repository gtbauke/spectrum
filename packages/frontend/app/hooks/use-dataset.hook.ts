import { useQuery } from "@tanstack/react-query";
import { getDataset } from "~/api/datasets/get-dataset.api";

export function useDataset(id: string) {
	return useQuery({
		queryKey: ["dataset", id],
		queryFn: () => getDataset(id),
		enabled: !!id,
		staleTime: 1000 * 60 * 5,
	});
}
