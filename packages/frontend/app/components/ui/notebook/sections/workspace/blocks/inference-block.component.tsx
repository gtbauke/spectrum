import Editor, { useMonaco } from "@monaco-editor/react";
import { useEffect } from "react";
import type { Model } from "~/schemas/domain/model.schema";
import { useEditorStore } from "~/stores/editor.store";
import {
	setupMonacoAutocomplete,
	updateAutocompleteModels,
} from "~/utils/monaco-autocomplete";

type InferenceBlockProps = {
	id: string;
	data: {
		code: string;
	};
	models: Model[];
};

export function InferenceBlock({ id, data, models }: InferenceBlockProps) {
	const updateBlock = useEditorStore((state) => state.updateBlock);
	const monaco = useMonaco();

	// Update global models for autocompletion
	useEffect(() => {
		updateAutocompleteModels(models);
	}, [models]);

	// Register completion provider once
	useEffect(() => {
		if (monaco) {
			setupMonacoAutocomplete(monaco);
		}
	}, [monaco]);

	const handleEditorChange = (value: string | undefined) => {
		updateBlock(id, { code: value || "" }, { recordHistory: true });
	};

	return (
		<div className="flex flex-col gap-4">
			<div className="rounded border border-border bg-[#0d0e12] overflow-hidden">
				<Editor
					height="200px"
					language="sql"
					theme="vs-dark"
					value={data.code}
					onChange={handleEditorChange}
					options={{
						minimap: { enabled: false },
						fontSize: 13,
						lineNumbers: "on",
						scrollBeyondLastLine: false,
						automaticLayout: true,
						padding: { top: 12, bottom: 12 },
						fontFamily: "'Fira Code', 'Cascadia Code', monospace",
					}}
				/>
			</div>
		</div>
	);
}
