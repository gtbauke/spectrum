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

	past: EditorBlock[][];
	future: EditorBlock[][];
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
		options?: { recordHistory: boolean },
	) => void;
	removeBlock: (id: string) => void;
	moveBlock: (id: string, direction: "up" | "down") => void;

	setActiveBlock: (id: string | null) => void;
	markClean: () => void;

	commit: () => void;
	undo: () => void;
	redo: () => void;
};

export type EditorStore = EditorState & EditorActions;

export const useEditorStore = create<EditorStore>((set, get) => ({
	profileId: null,
	versionId: null,
	isDirty: false,
	blocks: [],
	activeBlockId: null,
	past: [],
	future: [],

	commit: () => {
		const { blocks, past } = get();
		set({
			past: [...past.slice(-49), blocks],
			future: [],
			isDirty: true,
		});
	},

	undo: () => {
		const { past, blocks, future } = get();
		if (past.length === 0) return;

		const previous = past[past.length - 1];
		const newPast = past.slice(0, past.length - 1);

		set({
			blocks: previous,
			past: newPast,
			future: [blocks, ...future],
			activeBlockId: null,
		});
	},

	redo: () => {
		const { past, blocks, future } = get();
		if (future.length === 0) return;

		const next = future[0];
		const newFuture = future.slice(1);

		set({
			blocks: next,
			past: [...past, blocks],
			future: newFuture,
		});
	},

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

		get().commit();
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

	updateBlock: (id, newData, options = { recordHistory: true }) => {
		if (options.recordHistory) {
			get().commit();
		}

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

		get().commit();
		set((state) => ({
			blocks: state.blocks.filter((b) => b.id !== id),
			lastDeletedBlock: { block: blockToRemove, index },
			isDirty: true,
			activeBlockId: state.activeBlockId === id ? null : state.activeBlockId,
		}));
	},

	moveBlock: (id, direction) => {
		get().commit();
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
}));
