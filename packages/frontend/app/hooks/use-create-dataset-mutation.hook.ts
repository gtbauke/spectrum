import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createDataset } from "~/api/datasets/upload.api";
import type { CreateDatasetWithMultipleArtifactsDto } from "~/schemas/dtos/dataset.dto";

export function useCreateDatasetMutation() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: ({
			files,
			data,
		}: {
			files: File[];
			data: CreateDatasetWithMultipleArtifactsDto;
		}) => createDataset(files, data),

		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["datasets"] });
		},
		onError: (error) => {
			console.error("Failed to upload dataset:", error);
		},
	});
}
