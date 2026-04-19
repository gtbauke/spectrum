import type { InferenceRunStatus } from "~/schemas/domain/enums.schema";
import type { InferenceResult } from "~/schemas/domain/inference-result.schema";
import type { Profile } from "~/schemas/domain/profile.schema";

export type InferenceData = {
	code: string;
	status: InferenceRunStatus | "idle";
	activeRunId?: string;
	results?: InferenceResult[];
	executionTimeMs?: number;
	error?: string;
};

export type MarkdownData = {
	value: string;
};

export type BlockDataMap = {
	inference: InferenceData;
	markdown: MarkdownData;
};

export type BlockType = keyof BlockDataMap;

export type EditorBlock = {
	[K in BlockType]: {
		id: string;
		type: K;
		data: BlockDataMap[K];
	};
}[BlockType];

export type ProfileTabData = {
	tabId: string;

	profileId: string;
	versionId: string;

	profile?: Profile;

	blocks: EditorBlock[];
	isDirty: boolean;

	activeBlockId: string | null;

	past: EditorBlock[][];
	future: EditorBlock[][];
};

export type UploadTabData = {
	name: string;
	tabId: string;
	file: File | null;
};

export type DatasetTabData = {
	tabId: string;
	datasetId: string;
};

export type EditorTabDataMap = {
	profile: ProfileTabData;
	upload: UploadTabData;
	dataset: DatasetTabData;
};

export type EditorTabType = keyof EditorTabDataMap;

export type EditorTab = {
	[K in EditorTabType]: {
		id: string;
		type: K;
		data: EditorTabDataMap[K];
	};
}[EditorTabType];
