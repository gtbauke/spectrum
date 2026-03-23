import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";

import type { User } from "~/schemas/domain/user.schema";
import { profileSchema, type Profile } from "~/schemas/domain/profile.schema";
import { jobSchema, type Job, type Run } from "~/schemas/domain/job.schema";
import { blockSchema, type Block } from "~/schemas/domain/block.schema";
import { modelSchema, type Model } from "~/schemas/domain/model.schema";

import { listProfiles } from "../api/profiles/list-profiles.api";
import { getProfile } from "../api/profiles/get-profile.api";
import { updateProfile } from "../api/profiles/update-profile.api";
import { createBlocks } from "../api/profiles/blocks/create-blocks.api";
import { updateBlock as updateBlockApi } from "../api/profiles/blocks/update-block.api";
import { bulkUpdateBlocks as bulkUpdateBlocksApi } from "../api/profiles/blocks/bulk-update-blocks.api";
import { deleteBlock as deleteBlockApi } from "../api/profiles/blocks/delete-block.api";
import { runJob } from "../api/profiles/jobs/run-job.api";
import { login, logout, me } from "../api/auth/auth.api";

import type {
	BlockDataMap,
	BlockType,
	EditorBlock,
	EditorTab,
	EditorTabDataMap,
	EditorTabType,
	InferenceData,
} from "~/utils/types/editor.types";

export type {
	BlockDataMap,
	BlockType,
	EditorBlock,
	EditorTab,
	EditorTabDataMap,
	EditorTabType,
	InferenceData,
};

const MAX_TAB_HISTORY = 20;
const MAX_BLOCKS_HISTORY = 50;

type EditorState = {
	tabs: Record<string, EditorTab>;
	activeTabId: string | null;
	tabIds: string[];

	pastTabs: EditorTab[];
};

type UpdateActionOptions = {
	recordHistory: boolean;
};

type EditorActions = {
	openTab: (tab: EditorTab) => void;
	closeTab: (id: string) => void;
	updateTab: <T extends EditorTabType>(
		id: string,
		type: T,
		data: Partial<EditorTabDataMap[T]>,
	) => void;
	setActiveTab: (id: string | null) => void;
	reopenTab: (id: string) => void;

	addBlock: <T extends BlockType>(
		type: T,
		data: BlockDataMap[T],
		index?: number,
	) => void;

	updateBlock: <T extends BlockType>(
		id: string,
		data: Partial<BlockDataMap[T]>,
		options: UpdateActionOptions,
	) => void;

	removeBlock: (id: string) => void;
	reorderBlocks: (newBlocksOrder: EditorBlock[]) => void;

	setActiveBlock: (id: string | null) => void;
	markClean: () => void;

	commit: () => void;
	undo: () => void;
	redo: () => void;

	runInference: (id: string) => Promise<void>;
	initializeProfileBlocks: (id: string, profile: Profile) => void;
};

export type EditorStore = EditorState & EditorActions;

export const useEditorStore = create<EditorStore>((set, get) => ({
	tabs: {},
	activeTabId: null,
	pastTabs: [],
	tabIds: [],

	openTab: (tab) =>
		set((state) => {
			if (state.tabs[tab.id]) {
				return { activeTabId: tab.id };
			}

			const newPastTabs = state.pastTabs.filter((t) => t.id !== tab.id);
			return {
				tabs: { ...state.tabs, [tab.id]: tab },
				tabIds: [...state.tabIds, tab.id],
				activeTabId: tab.id,
				pastTabs: newPastTabs,
			};
		}),

	closeTab: (id) =>
		set((state) => {
			if (!state.tabs[id]) {
				return state;
			}

			const tabToClose = state.tabs[id];
			const currentTabIndex = state.tabIds.indexOf(id);

			const newTabs = { ...state.tabs };
			delete newTabs[id];

			const newTabIds = state.tabIds.filter((tabId) => tabId !== id);
			let newActiveId = state.activeTabId;

			if (state.activeTabId === id) {
				if (newTabIds.length === 0) {
					newActiveId = null;
				} else {
					const fallbackIndex =
						currentTabIndex >= newTabIds.length
							? newTabIds.length - 1
							: currentTabIndex;

					newActiveId = newTabIds[fallbackIndex];
				}
			}

			const newPastTabs = [...state.pastTabs, tabToClose].slice(
				-MAX_TAB_HISTORY,
			);

			return {
				tabs: newTabs,
				tabIds: newTabIds,
				activeTabId: newActiveId,
				pastTabs: newPastTabs,
			};
		}),

	updateTab: (id, type, newData) =>
		set((state) => {
			const tab = state.tabs[id];

			if (!tab) {
				return state;
			}

			if (tab.type !== type) {
				console.warn(
					`[EditorStore] Failed to update tab ${id}: Type mismatch. Expected '${type}', got '${tab.type}'.`,
				);
				return state;
			}

			return {
				tabs: {
					...state.tabs,
					[id]: {
						...tab,
						data: {
							...tab.data,
							...newData,
							isDirty: true,
						},
					} as EditorTab,
				},
			};
		}),

	setActiveTab: (id) =>
		set((state) => {
			if (id === null) {
				return { activeTabId: null };
			}

			if (!state.tabs[id]) {
				return state;
			}

			return { activeTabId: id };
		}),

	reopenTab: (id) =>
		set((state) => {
			const tabToReopen = state.pastTabs.find((t) => t.id === id);
			if (!tabToReopen) {
				return state;
			}

			const newPastTabs = state.pastTabs.filter((t) => t.id !== id);
			return {
				pastTabs: newPastTabs,
				tabs: { ...state.tabs, [id]: tabToReopen },
				tabIds: [...state.tabIds, id],
				activeTabId: id,
			};
		}),

	commit: () =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			const newPast = [
				...tab.data.past.slice(-(MAX_BLOCKS_HISTORY - 1)),
				tab.data.blocks,
			];

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: {
							...tab.data,
							past: newPast,
							future: [],
							isDirty: true,
						},
					},
				},
			};
		}),

	undo: () =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile" || tab.data.past.length === 0) {
				return state;
			}

			const previous = tab.data.past[tab.data.past.length - 1];
			const newPast = tab.data.past.slice(0, -1);

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: {
							...tab.data,
							blocks: previous,
							past: newPast,
							future: [tab.data.blocks, ...tab.data.future],
							activeBlockId: null,
						},
					},
				},
			};
		}),

	redo: () =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile" || tab.data.future.length === 0) {
				return state;
			}

			const next = tab.data.future[0];
			const newFuture = tab.data.future.slice(1);

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: {
							...tab.data,
							blocks: next,
							past: [...tab.data.past, tab.data.blocks],
							future: newFuture,
						},
					},
				},
			};
		}),

	addBlock: (type, data, index) => {
		const newBlock = { id: uuidv4(), type, data } as EditorBlock;

		get().commit();
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			const blocks = [...tab.data.blocks];
			let targetIndex = index;

			if (targetIndex === undefined) {
				const activeIndex = blocks.findIndex(
					(b) => b.id === tab.data.activeBlockId,
				);
				targetIndex = activeIndex >= 0 ? activeIndex + 1 : blocks.length;
			}

			blocks.splice(targetIndex, 0, newBlock);

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: {
							...tab.data,
							blocks,
							isDirty: true,
							activeBlockId: newBlock.id,
						},
					},
				},
			};
		});
	},

	updateBlock: (id, newData, options = { recordHistory: true }) => {
		if (options.recordHistory) {
			get().commit();
		}

		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			const newBlocks = tab.data.blocks.map((block) =>
				block.id === id
					? ({ ...block, data: { ...block.data, ...newData } } as EditorBlock)
					: block,
			);

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: { ...tab.data, blocks: newBlocks, isDirty: true },
					},
				},
			};
		});
	},

	removeBlock: (id) => {
		get().commit();

		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			const newBlocks = tab.data.blocks.filter((b) => b.id !== id);

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: {
							...tab.data,
							blocks: newBlocks,
							isDirty: true,
							activeBlockId:
								tab.data.activeBlockId === id ? null : tab.data.activeBlockId,
						},
					},
				},
			};
		});
	},

	reorderBlocks: (newBlocksOrder) =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: { ...tab.data, blocks: newBlocksOrder, isDirty: true },
					},
				},
			};
		}),

	setActiveBlock: (id) =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: { ...tab.data, activeBlockId: id },
					},
				},
			};
		}),

	markClean: () =>
		set((state) => {
			const tabId = state.activeTabId;
			if (!tabId) {
				return state;
			}

			const tab = state.tabs[tabId];
			if (tab.type !== "profile") {
				return state;
			}

			return {
				tabs: {
					...state.tabs,
					[tabId]: {
						...tab,
						data: { ...tab.data, isDirty: false },
					},
				},
			};
		}),

	runInference: async (id) => {
		const updateBlock = get().updateBlock;
		const activeTabId = get().activeTabId;
		if (!activeTabId) return;

		const tab = get().tabs[activeTabId];
		if (tab.type !== "profile") return;

		// Find the job associated with this inference block
		// For now, we assume one-to-one or we find the right job by name/metadata
		// In a real scenario, the block data would hold the job_id
		const block = tab.data.blocks.find(b => b.id === id);
		if (!block || block.type !== "inference") return;

		updateBlock(id, { isRunning: true }, { recordHistory: false });

		try {
			// Find the job in the profile that matches this block (or just use the first one for now)
			const job = tab.data.profile?.jobs?.[0];
			if (!job) throw new Error("No job found for inference");

			const run = await runJob(tab.data.profileId, job.id);

			// Update block with run info
			updateBlock(
				id,
				{
					isRunning: false,
					results: {
						metrics: {
							rmse: 0, // Will be updated by worker
							mae: 0,
						},
						formula: "Running...", // Will be updated by worker
					},
				},
				{ recordHistory: true },
			);
		} catch (error) {
			console.error("Inference failed:", error);
			updateBlock(id, { isRunning: false }, { recordHistory: false });
		}
	},
	initializeProfileBlocks: (id: string, profile) =>
		set((state) => {
			const tab = state.tabs[id];
			if (!tab || tab.type !== "profile") return state;

			const fixedBlocks: EditorBlock[] = [
				{
					id: `${id}-metadata`,
					type: "metadata",
					data: {
						name: profile.name,
						description: profile.description,
						mode: profile.mode,
					},
				},
				{
					id: `${id}-datasets`,
					type: "datasets",
					data: { datasets: profile.datasets || [] },
				},
				{
					id: `${id}-jobs`,
					type: "jobs",
					data: { profileId: profile.id },
				},
			];

			// Map dynamic blocks from the backend profile
			const dynamicBlocks: EditorBlock[] = (profile.blocks || []).map((b) => {
				if (b.kind === "markdown") {
					return {
						id: b.id,
						type: "markdown",
						data: { value: b.data.data },
					} as EditorBlock;
				}
				return {
					id: b.id,
					type: "inference",
					data: { code: b.data.data },
				} as EditorBlock;
			});

			// If no dynamic blocks, add a default markdown block
			if (dynamicBlocks.length === 0) {
				dynamicBlocks.push({
					id: uuidv4(),
					type: "markdown",
					data: { value: "# Getting Started\n\nWrite your analysis here..." },
				});
			}

			return {
				tabs: {
					...state.tabs,
					[id]: {
						...tab,
						data: {
							...tab.data,
							profile,
							blocks: [...fixedBlocks, ...dynamicBlocks],
							isDirty: false,
						},
					},
				},
			};
		}),
}));
