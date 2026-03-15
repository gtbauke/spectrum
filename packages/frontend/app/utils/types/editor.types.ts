import type { ProfileDatasetAssociation } from "~/schemas/models/profile-dataset-association.schema";
import type { ProfileVisibility } from "~/schemas/models/profile-visibility.schema";

export type MetadataData = {
	name: string;
	description: string | null | undefined;
	visibility: ProfileVisibility;
};

export type DatasetData = {
	datasets: ProfileDatasetAssociation[];
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

	name: string;
	description: string | null;

	blocks: EditorBlock[];
	isDirty: boolean;

	activeBlockId: string | null;

	past: EditorBlock[][];
	future: EditorBlock[][];
};

export type UploadTabData = {
	name: "upload";
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
