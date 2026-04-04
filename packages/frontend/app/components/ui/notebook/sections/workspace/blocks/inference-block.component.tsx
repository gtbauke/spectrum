import Editor, { useMonaco } from "@monaco-editor/react";
import { CheckCircle2 } from "lucide-react";
import { useEffect } from "react";
import * as katex from "react-katex";
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
		<div className="flex flex-col gap-6">
			<div className="relative group/editor">
				<div className="absolute -inset-1 bg-linear-to-r from-secondary/20 to-primary/20 rounded-xl blur opacity-25 transition duration-1000 group-hover/editor:duration-200" />
				<div className="relative rounded-xl border border-white/10 bg-background-surface/50 backdrop-blur-xl overflow-hidden ring-1 ring-white/5">
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
							padding: { top: 16, bottom: 16 },
							fontFamily: "'Fira Code', 'Cascadia Code', monospace",
						}}
					/>
				</div>
			</div>

			<ResultsPane />
		</div>
	);
}

function ResultsPane() {
	return (
		<div className="flex flex-col gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
			<div className="flex items-center gap-2 px-1">
				<CheckCircle2 className="w-4 h-4 text-secondary" />

				<span className="text-[10px] font-black uppercase tracking-[0.2em] text-secondary/80">
					Latest Result
				</span>

				<div className="h-px flex-1 bg-linear-to-r from-secondary/20 to-transparent ml-2" />
			</div>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
				<MetricCard label="R² Score" value="0.9842" accent="emerald" />
				<MetricCard label="MSE" value="0.00124" accent="emerald" />
				<MetricCard label="Complexity" value="14" accent="emerald" />
			</div>

			<div className="p-8 rounded-xl border border-white/5 bg-white/2 flex flex-col items-center justify-center gap-4 group/formula transition-colors hover:bg-white/4">
				<div className="text-[10px] uppercase tracking-widest text-gray-500 font-bold">
					Discovered Model
				</div>
				<div className="text-xl text-white/90 group-hover:text-white transition-colors">
					<katex.BlockMath math="f(x) = \sin(x) \cdot e^{-0.5x} + 0.1 x^2" />
				</div>
			</div>
		</div>
	);
}

function MetricCard({
	label,
	value,
	accent,
}: {
	label: string;
	value: string;
	accent: "emerald" | "purple";
}) {
	return (
		<div className="p-4 rounded-xl border border-white/5 bg-white/[0.02] flex flex-col gap-1 transition-all hover:border-white/10 hover:bg-white/[0.05]">
			<span className="text-[10px] font-bold uppercase tracking-widest text-gray-500">
				{label}
			</span>
			<span className="text-xl font-mono font-medium text-white/90">
				{value}
			</span>
		</div>
	);
}
