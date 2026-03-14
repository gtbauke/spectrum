import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";
import type { ProfileDatasetAssociation } from "~/schemas/generated/profile-dataset-association.schema";

export type MetadataData = {
	name: string;
	description: string | null | undefined;
};

export type DatasetData = {
	datasets: ProfileDatasetAssociation[];
};

export type JobsData = {
	activeJobs: string[];
	lastRunAt?: string;
};

export type ResultsData = {
	metrics: Record<string, number>;
	formula?: string;
};

export type InferenceData = {
	code: string;
};

export type BlockDataMap = {
	metadata: MetadataData;
	dataset: DatasetData;
	jobs: JobsData;
	results: ResultsData;
	inference: InferenceData;
};

export type BlockType = keyof BlockDataMap;

export type EditorBlock = {
	[K in BlockType]: {
		id: string;
		type: K;
		data: BlockDataMap[K];
	};
}[BlockType];

type EditorState = {
	profileId: string | null;
	versionId: string | null;
	isDirty: boolean;
	blocks: EditorBlock[];
	activeBlockId: string | null;
};

type EditorActions = {
	initEditor: (
		profileId: string,
		versionId: string,
		initialBlocks: EditorBlock[],
	) => void;

	addBlock: <T extends BlockType>(
		type: T,
		data: BlockDataMap[T],
		index?: number,
	) => void;
	updateBlock: <T extends BlockType>(
		id: string,
		data: Partial<BlockDataMap[T]>,
	) => void;
	removeBlock: (id: string) => void;
	undoDelete: () => void;
	clearLastDeletedBlock: () => void;
	moveBlock: (id: string, direction: "up" | "down") => void;

	setActiveBlock: (id: string | null) => void;
	markClean: () => void;

	lastDeletedBlock: { block: EditorBlock; index: number } | null;
};

export type EditorStore = EditorState & EditorActions;

export const useEditorStore = create<EditorStore>((set, get) => ({
	profileId: null,
	versionId: null,
	isDirty: false,
	blocks: [],
	activeBlockId: null,
	lastDeletedBlock: null,

	initEditor: (profileId, versionId, initialBlocks) => {
		set({
			profileId,
			versionId,
			blocks: initialBlocks,
			isDirty: false,
			activeBlockId: initialBlocks[0]?.id || null,
		});
	},

	addBlock: <T extends BlockType>(
		type: T,
		data: BlockDataMap[T],
		index?: number,
	) => {
		const newBlock: EditorBlock = { id: uuidv4(), type, data } as EditorBlock;

		set((state) => {
			const newBlocks = [...state.blocks];

			let targetIndex = index;
			if (targetIndex === undefined) {
				const activeIndex = state.blocks.findIndex(
					(b) => b.id === state.activeBlockId,
				);
				targetIndex = activeIndex >= 0 ? activeIndex + 1 : state.blocks.length;
			}

			newBlocks.splice(targetIndex, 0, newBlock);

			return {
				blocks: newBlocks,
				isDirty: true,
				activeBlockId: newBlock.id,
			};
		});
	},

	updateBlock: (id, newData) => {
		set((state) => ({
			blocks: state.blocks.map((block) =>
				block.id === id
					? ({ ...block, data: { ...block.data, ...newData } } as EditorBlock)
					: block,
			),
			isDirty: true,
		}));
	},

	removeBlock: (id) => {
		const state = get();
		const index = state.blocks.findIndex((b) => b.id === id);
		if (index === -1) return;

		const blockToRemove = state.blocks[index];

		set((state) => ({
			blocks: state.blocks.filter((b) => b.id !== id),
			lastDeletedBlock: { block: blockToRemove, index },
			isDirty: true,
			activeBlockId: state.activeBlockId === id ? null : state.activeBlockId,
		}));
	},

	moveBlock: (id, direction) => {
		set((state) => {
			const index = state.blocks.findIndex((b) => b.id === id);
			if (index < 0) return state;
			if (direction === "up" && index === 0) return state;
			if (direction === "down" && index === state.blocks.length - 1)
				return state;

			const newBlocks = [...state.blocks];
			const targetIndex = direction === "up" ? index - 1 : index + 1;

			[newBlocks[index], newBlocks[targetIndex]] = [
				newBlocks[targetIndex],
				newBlocks[index],
			];

			return { blocks: newBlocks, isDirty: true };
		});
	},

	setActiveBlock: (id) => set({ activeBlockId: id }),

	markClean: () => set({ isDirty: false }),

	undoDelete: () => {
		const { lastDeletedBlock, blocks } = get();
		if (!lastDeletedBlock) return;

		set((state) => {
			const newBlocks = [...state.blocks];
			newBlocks.splice(lastDeletedBlock.index, 0, lastDeletedBlock.block);
			return {
				blocks: newBlocks,
				lastDeletedBlock: null, // Clear after undo
				activeBlockId: lastDeletedBlock.block.id,
			};
		});
	},

	clearLastDeletedBlock: () => {
		set({ lastDeletedBlock: null });
	},
}));
