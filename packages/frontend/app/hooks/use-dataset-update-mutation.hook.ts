import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateDataset } from "~/api/datasets/update-dataset.api";
import type { UpdateDatasetDto } from "~/api/datasets/update-dataset.api";

type UpdateDatasetParams = {
	datasetId: string;
	data: UpdateDatasetDto;
};

export function useDatasetUpdateMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async ({ datasetId, data }: UpdateDatasetParams) => {
			return await updateDataset(datasetId, data);
		},
		onSuccess: (updatedDataset) => {
			queryClient.invalidateQueries({ queryKey: ["datasets"] });
			queryClient.invalidateQueries({
				queryKey: ["dataset", updatedDataset.id],
			});
		},
		onError: (error) => {
			console.error("Failed to update dataset:", error);
		},
	});
}
