import type { Block } from "~/schemas/domain/block.schema";
import type { Profile } from "~/schemas/domain/profile.schema";
import type { EditorBlock } from "../types/editor.types";

type MapEditorBlockToProfileBlockParams = {
	block: EditorBlock;
	profile: Profile;
	index: number;
};

export function mapEditorBlockToProfileBlock(
	params: MapEditorBlockToProfileBlockParams,
): Block {
	if (params.block.type === "markdown") {
		const matchingExistingBlock = params.profile.blocks.find(
			(b) => b.id === params.block.id && b.kind === "markdown",
		);

		if (matchingExistingBlock) {
			return {
				...matchingExistingBlock,
				data: {
					kind: "markdown",
					data: params.block.data.value,
				},
			};
		}

		const createdAtDate = new Date();

		return {
			id: params.block.id,
			kind: "markdown",
			orderIndex: params.index,
			data: {
				kind: "markdown",
				data: params.block.data.value,
			},
			profileId: params.profile.id,
			createdAt: createdAtDate,
			updatedAt: createdAtDate,
		};
	}

	if (params.block.type === "inference") {
		const matchingExistingBlock = params.profile.blocks.find(
			(b) => b.id === params.block.id && b.kind === "inference",
		);

		if (matchingExistingBlock) {
			return {
				...matchingExistingBlock,
				data: {
					kind: "inference",
					data: params.block.data.code,
				},
			};
		}

		const createdAtDate = new Date();

		return {
			id: params.block.id,
			kind: "inference",
			orderIndex: params.index,
			data: {
				kind: "inference",
				data: params.block.data.code,
			},
			profileId: params.profile.id,
			createdAt: createdAtDate,
			updatedAt: createdAtDate,
		};
	}

	throw new Error(`Unsupported block type: ${params.block}`);
}
