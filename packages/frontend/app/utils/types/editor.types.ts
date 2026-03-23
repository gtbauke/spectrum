import type { Profile } from "~/schemas/domain/profile.schema";
import type { ProfileMode } from "~/schemas/domain/enums.schema";
import type { Dataset } from "~/schemas/domain/dataset.schema";

export type MetadataData = {
	name: string;
	description: string | null | undefined;
	mode: ProfileMode;
};

export type DatasetData = {
	datasets: Dataset[];
};

export type JobsData = {
	profileId: string;
};

export type ResultsData = {
	metrics: Record<string, number>;
	formula?: string;
};

export type InferenceData = {
	code: string;
	isRunning?: boolean;
	results?: ResultsData;
};

export type MarkdownData = {
	value: string;
};

export type BlockDataMap = {
	metadata: MetadataData;
	datasets: DatasetData;
	jobs: JobsData;
	results: ResultsData;
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

export type EditorTabDataMap = {
	profile: ProfileTabData;
	upload: UploadTabData;
};

export type EditorTabType = keyof EditorTabDataMap;

export type EditorTab = {
	[K in EditorTabType]: {
		id: string;
		type: K;
		data: EditorTabDataMap[K];
	};
}[EditorTabType];
