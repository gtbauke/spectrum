import { useMutation } from "@tanstack/react-query";
import { createInferenceRun } from "~/api/profiles/blocks/create-inference-run.api";
import { updateBlock } from "~/api/profiles/blocks/update-block.api";
import type { UpdateBlockDto } from "~/schemas/dtos/block.dto";
import { useEditorStore } from "~/stores/editor.store";

export function useRunInferenceMutation(profileId: string, blockId: string) {
	const updateEditorBlock = useEditorStore((state) => state.updateBlock);

	return useMutation({
		mutationFn: async (block: UpdateBlockDto) => {
			await updateBlock(profileId, blockId, block);
			return createInferenceRun(profileId, blockId);
		},
		onSuccess: (run) => {
			if (run) {
				updateEditorBlock(
					blockId,
					{
						status: run.status,
						activeRunId: run.id,
						error: undefined,
					},
					{ recordHistory: false },
				);
			}
		},
		onError: (error) => {
			updateEditorBlock(
				blockId,
				{
					status: "failed",
					error: error.message || "Failed to start inference run",
				},
				{ recordHistory: false },
			);
		},
	});
}
