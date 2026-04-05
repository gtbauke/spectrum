import Editor, { useMonaco } from "@monaco-editor/react";
import {
	AlertCircle,
	CheckCircle2,
	Loader2,
	Play,
	Timer,
	Zap,
} from "lucide-react";
import { useEffect } from "react";
import * as katex from "react-katex";
import { useInferenceStream } from "~/hooks/use-inference-stream.hook";
import { useRunInferenceMutation } from "~/hooks/use-run-inference-mutation.hook";
import type { InferenceResult } from "~/schemas/domain/inference-result.schema";
import type { Model } from "~/schemas/domain/model.schema";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import {
	setupMonacoAutocomplete,
	updateAutocompleteModels,
} from "~/utils/monaco-autocomplete";
import type { InferenceData } from "~/utils/types/editor.types";

type InferenceBlockProps = {
	id: string;
	data: InferenceData;
	models: Model[];
	orderIndex: number;
};

export function InferenceBlock({
	id,
	data,
	models,
	orderIndex,
}: InferenceBlockProps) {
	const updateBlock = useEditorStore((state) => state.updateBlock);
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const tabs = useEditorStore((state) => state.tabs);
	const activeTab = activeTabId ? tabs[activeTabId] : null;
	const profileId =
		activeTab?.type === "profile" ? activeTab.data.profileId : null;

	const monaco = useMonaco();

	useInferenceStream(profileId || "", id, data.activeRunId);

	const { mutate: runInference, isPending: isStarting } =
		useRunInferenceMutation(profileId || "", id);

	useEffect(() => {
		updateAutocompleteModels(models);
	}, [models]);

	useEffect(() => {
		if (monaco) {
			setupMonacoAutocomplete(monaco);
		}
	}, [monaco]);

	const handleEditorChange = (value: string | undefined) => {
		updateBlock(id, { code: value || "" }, { recordHistory: true });
	};

	const isRunning =
		data.status !== "idle" &&
		data.status !== "completed" &&
		data.status !== "failed";

	return (
		<div className="flex flex-col gap-6">
			<div className="relative group/editor">
				<div className="absolute -inset-1 bg-linear-to-r from-secondary/20 to-primary/20 rounded-xl blur opacity-25 transition duration-1000 group-hover/editor:duration-200" />
				<div className="relative rounded-xl border border-white/10 bg-background-surface/50 backdrop-blur-xl overflow-hidden ring-1 ring-white/5">
					<div className="flex items-center justify-between px-4 py-2 border-b border-white/5 bg-white/2">
						<div className="flex items-center gap-2">
							<Zap className="w-3.5 h-3.5 text-primary" />
							<span className="text-[10px] font-bold uppercase tracking-widest text-gray-400">
								Inference Engine
							</span>
						</div>
						<button
							type="button"
							onClick={() =>
								runInference({
									order_index: orderIndex,
									data: {
										kind: "inference",
										data: data.code,
									},
								})
							}
							disabled={isRunning || isStarting || !profileId}
							className={cn(
								"flex items-center gap-2 px-3 py-1 rounded-md transition-all",
								isRunning || isStarting || !profileId
									? "bg-white/5 text-gray-500 cursor-not-allowed"
									: "bg-primary/20 text-primary hover:bg-primary/30 border border-primary/20 hover:border-primary/40",
							)}
						>
							{isRunning || isStarting ? (
								<Loader2 className="w-3 h-3 animate-spin" />
							) : (
								<Play className="w-3 h-3 fill-current" />
							)}
							<span className="text-[10px] font-bold uppercase tracking-widest leading-none mt-0.5">
								{isRunning ? "Running..." : isStarting ? "Starting..." : "Run"}
							</span>
						</button>
					</div>

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
							readOnly: isRunning,
						}}
					/>
				</div>
			</div>

			<ResultsPane data={data} />
		</div>
	);
}

function ResultsPane({ data }: { data: InferenceData }) {
	const { status, results, executionTimeMs, error } = data;

	if (status === "idle" && !results) return null;

	return (
		<div className="flex flex-col gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
			<div className="flex items-center gap-2 px-1">
				{status === "completed" ? (
					<CheckCircle2 className="w-4 h-4 text-emerald-500" />
				) : status === "failed" ? (
					<AlertCircle className="w-4 h-4 text-red-500" />
				) : (
					<Loader2 className="w-4 h-4 text-primary animate-spin" />
				)}

				<span className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50">
					{status === "completed"
						? "Execution Complete"
						: status === "failed"
							? "Execution Failed"
							: `Inference Stage: ${status.replace(/_/g, " ")}`}
				</span>

				{executionTimeMs !== undefined && (
					<div className="flex items-center gap-1.5 ml-4 px-2 py-0.5 rounded-full bg-white/5 border border-white/5">
						<Timer className="w-3 h-3 text-white/40" />
						<span className="text-[10px] font-mono text-white/60">
							{executionTimeMs}ms
						</span>
					</div>
				)}

				<div className="h-px flex-1 bg-linear-to-r from-white/10 to-transparent ml-2" />
			</div>

			{error && (
				<div className="p-4 rounded-xl border border-red-500/20 bg-red-500/5 flex items-center gap-3">
					<AlertCircle className="w-4 h-4 text-red-500 shrink-0" />
					<p className="text-xs text-red-400 font-medium">{error}</p>
				</div>
			)}

			{results && results.length > 0 && (
				<div className="flex flex-col gap-4">
					{results.map((result, idx) => (
						<ResultItem key={result.id} result={result} isPrimary={idx === 0} />
					))}
				</div>
			)}
		</div>
	);
}

function ResultItem({
	result,
	isPrimary,
}: {
	result: InferenceResult;
	isPrimary: boolean;
}) {
	return (
		<div
			className={cn(
				"p-6 rounded-xl border flex flex-col gap-6 transition-all group/result",
				isPrimary
					? "bg-primary/5 border-primary/20 hover:border-primary/40"
					: "bg-white/2 border-white/5 hover:bg-white/4 hover:border-white/10",
			)}
		>
			<div className="flex items-center justify-between">
				<div className="flex items-center gap-4">
					<div className="flex flex-col gap-0.5">
						<span className="text-[10px] font-bold uppercase tracking-widest text-white/40">
							{isPrimary
								? "Primary Discovery"
								: `Variant ${result.id.slice(0, 4)}`}
						</span>
					</div>
				</div>

				<div className="flex items-center gap-3">
					<MetricBadge label="R²" value={result.fitness?.toFixed(4) || "N/A"} />
					<MetricBadge label="DL" value={result.dl?.toFixed(2) || "N/A"} />
					<MetricBadge label="Size" value={result.size?.toString() || "N/A"} />
				</div>
			</div>

			<div className="flex flex-col gap-3 items-center justify-center py-4">
				<div className="text-[10px] uppercase tracking-widest text-white/30 font-bold">
					Mathematical Expression
				</div>
				<div className="text-xl text-white/90 group-hover/result:text-white transition-colors overflow-x-auto max-w-full">
					<katex.BlockMath math={result.latex || result.expression} />
				</div>
			</div>
		</div>
	);
}

function MetricBadge({ label, value }: { label: string; value: string }) {
	return (
		<div className="flex items-center gap-2 px-2 py-1 rounded-md bg-black/20 border border-white/5">
			<span className="text-[9px] font-black uppercase tracking-tighter text-white/40">
				{label}
			</span>
			<span className="text-xs font-mono font-bold text-white/80">{value}</span>
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
