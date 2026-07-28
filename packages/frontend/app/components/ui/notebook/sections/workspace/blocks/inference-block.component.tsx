import Editor, { useMonaco } from "@monaco-editor/react";
import * as Tooltip from "@radix-ui/react-tooltip";
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
} from "@tanstack/react-table";
import {
	AlertCircle,
	AlertTriangle,
	Check,
	CheckCircle2,
	ChevronDown,
	ChevronUp,
	Code2,
	Copy,
	Cpu,
	Download,
	LayoutList,
	Loader2,
	Play,
	RefreshCw,
	Table2,
	Timer,
	WifiOff,
	Zap,
} from "lucide-react";
import { evaluate } from "mathjs";
import { useEffect, useMemo, useState } from "react";
import * as katex from "react-katex";
import { useInferenceStream } from "~/hooks/use-inference-stream.hook";
import { useLatestInferenceRun } from "~/hooks/use-latest-inference-run.hook";
import { useRunInferenceMutation } from "~/hooks/use-run-inference-mutation.hook";
import type { InferenceResult } from "~/schemas/domain/inference-result.schema";
import type { Model } from "~/schemas/domain/model.schema";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import {
	setupMonacoAutocomplete,
	updateAutocompleteModels,
} from "~/utils/monaco-autocomplete";
import type { InferenceData, InferenceErrorType } from "~/utils/types/editor.types";

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

	const { data: latestRun } = useLatestInferenceRun(profileId || "", id, {
		enabled: !!profileId && !data.activeRunId,
	});

	useEffect(() => {
		if (latestRun && !data.activeRunId) {
			updateBlock(
				id,
				{
					activeRunId: latestRun.id,
					status: latestRun.status,
				},
				{ recordHistory: false },
			);
		}
	}, [latestRun, data.activeRunId, id, updateBlock]);

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

			<ResultsPane
				data={data}
				onRetry={() =>
					runInference({
						order_index: orderIndex,
						data: {
							kind: "inference",
							data: data.code,
						},
					})
				}
			/>
		</div>
	);
}

function ResultsPane({
	data,
	onRetry,
}: {
	data: InferenceData;
	onRetry?: () => void;
}) {
	const { results, executionTimeMs, error, errorType, errorDetails } =
		data;
	const status = data.status || "idle";
	const [viewMode, setViewMode] = useState<"list" | "table">("list");

	const handleDownloadCSV = () => {
		if (!results || results.length === 0) return;

		const headers = [
			"id",
			"run_id",
			"expression",
			"latex",
			"fitness",
			"dl",
			"size",
			"frequency",
			"parameters",
			"prediction",
		];

		const escapeCsv = (val: any) => {
			if (val === null || val === undefined) return "";
			const str = typeof val === "object" ? JSON.stringify(val) : String(val);
			if (str.includes(",") || str.includes('"') || str.includes("\n")) {
				return `"${str.replace(/"/g, '""')}"`;
			}
			return str;
		};

		const rows = results.map((r) =>
			headers.map((h) => escapeCsv((r as any)[h])).join(","),
		);

		const csvContent = [headers.join(","), ...rows].join("\n");
		const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
		const url = URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = url;
		
		const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
		const runId = data.activeRunId || "unknown";
		link.download = `inference_results_${runId}_${timestamp}.csv`;
		
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(url);
	};

	if (status === "idle" && !results) return null;

	return (
		<div className="flex flex-col gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
			<div className="flex items-center gap-2 px-1">
				<div className="flex items-center gap-2">
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
				</div>

				{executionTimeMs !== undefined && (
					<div className="flex items-center gap-1.5 ml-4 px-2 py-0.5 rounded-full bg-white/5 border border-white/5">
						<Timer className="w-3 h-3 text-white/40" />
						<span className="text-[10px] font-mono text-white/60">
							{executionTimeMs}ms
						</span>
					</div>
				)}

				<div className="h-px flex-1 bg-linear-to-r from-white/10 to-transparent mx-2" />

				<div className="flex items-center gap-1 p-1 rounded-lg bg-black/20 border border-white/5">
					<button
						type="button"
						onClick={() => setViewMode("list")}
						className={cn(
							"p-1.5 rounded-md transition-all",
							viewMode === "list"
								? "bg-primary/20 text-primary shadow-xs"
								: "text-white/40 hover:text-white/60 hover:bg-white/5",
						)}
						title="List View"
					>
						<LayoutList className="w-3.5 h-3.5" />
					</button>
					<button
						type="button"
						onClick={() => setViewMode("table")}
						className={cn(
							"p-1.5 rounded-md transition-all",
							viewMode === "table"
								? "bg-primary/20 text-primary shadow-xs"
								: "text-white/40 hover:text-white/60 hover:bg-white/5",
						)}
						title="Table View"
					>
						<Table2 className="w-3.5 h-3.5" />
					</button>

					<div className="w-px h-4 bg-white/10 mx-1" />

					<button
						type="button"
						onClick={handleDownloadCSV}
						className="p-1.5 rounded-md transition-all text-white/40 hover:text-white/60 hover:bg-white/5"
						title="Export to CSV"
					>
						<Download className="w-3.5 h-3.5" />
					</button>
				</div>
			</div>

			{error && (
				<ErrorCard
					error={error}
					errorType={errorType}
					errorDetails={errorDetails}
					onRetry={onRetry}
				/>
			)}

			{results && results.length > 0 && (
				<div>
					{viewMode === "list" ? (
						<div className="flex flex-col gap-4">
							{results.map((result, idx) => (
								<ResultItem
									key={result.id}
									result={result}
									isPrimary={idx === 0}
								/>
							))}
						</div>
					) : (
						<ResultsTable results={results} />
					)}
				</div>
			)}
		</div>
	);
}

function ErrorCard({
	error,
	errorType = "unknown",
	errorDetails,
	onRetry,
}: {
	error: string;
	errorType?: InferenceErrorType;
	errorDetails?: string;
	onRetry?: () => void;
}) {
	const [copied, setCopied] = useState(false);
	const [showDetails, setShowDetails] = useState(false);

	const handleCopy = () => {
		const fullText = errorDetails
			? `${error}\n\nDetails:\n${errorDetails}`
			: error;
		navigator.clipboard.writeText(fullText);
		setCopied(true);
		setTimeout(() => setCopied(false), 2000);
	};

	const getCategoryBadge = () => {
		switch (errorType) {
			case "syntax":
				return {
					icon: Code2,
					label: "Query Syntax Error",
					badgeBg: "bg-amber-500/10 text-amber-400 border-amber-500/20",
				};
			case "network":
				return {
					icon: WifiOff,
					label: "Connection / Stream Error",
					badgeBg: "bg-rose-500/10 text-rose-400 border-rose-500/20",
				};
			case "execution":
				return {
					icon: Cpu,
					label: "Execution Error",
					badgeBg: "bg-red-500/10 text-red-400 border-red-500/20",
				};
			default:
				return {
					icon: AlertTriangle,
					label: "System Error",
					badgeBg: "bg-red-500/10 text-red-400 border-red-500/20",
				};
		}
	};

	const category = getCategoryBadge();
	const CategoryIcon = category.icon;

	return (
		<div className="rounded-xl border border-red-500/20 bg-red-950/20 backdrop-blur-xl p-4 flex flex-col gap-3 shadow-lg transition-all animate-in fade-in slide-in-from-top-2">
			<div className="flex items-center justify-between gap-2 border-b border-red-500/10 pb-2">
				<div className="flex items-center gap-2">
					<div
						className={cn(
							"px-2 py-0.5 rounded-full border text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5",
							category.badgeBg,
						)}
					>
						<CategoryIcon className="w-3 h-3" />
						<span>{category.label}</span>
					</div>
				</div>

				<div className="flex items-center gap-1.5">
					<button
						type="button"
						onClick={handleCopy}
						className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white text-xs border border-white/10 transition-all cursor-pointer"
						title="Copy error details"
					>
						{copied ? (
							<Check className="w-3.5 h-3.5 text-emerald-400" />
						) : (
							<Copy className="w-3.5 h-3.5 text-gray-400" />
						)}
						<span className="text-[11px] font-medium">
							{copied ? "Copied" : "Copy"}
						</span>
					</button>

					{onRetry && (
						<button
							type="button"
							onClick={onRetry}
							className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-primary/20 hover:bg-primary/30 text-primary text-xs border border-primary/30 transition-all font-medium cursor-pointer"
						>
							<RefreshCw className="w-3.5 h-3.5" />
							<span className="text-[11px]">Retry Run</span>
						</button>
					)}
				</div>
			</div>

			<div className="flex flex-col gap-2">
				<p className="text-xs text-red-200 font-mono leading-relaxed bg-black/30 p-3 rounded-lg border border-red-500/10 whitespace-pre-wrap break-words">
					{error}
				</p>

				{errorDetails && (
					<div className="flex flex-col gap-1 mt-1">
						<button
							type="button"
							onClick={() => setShowDetails(!showDetails)}
							className="flex items-center gap-1 text-[11px] text-gray-400 hover:text-gray-200 transition-colors w-fit font-medium cursor-pointer"
						>
							{showDetails ? (
								<ChevronUp className="w-3.5 h-3.5" />
							) : (
								<ChevronDown className="w-3.5 h-3.5" />
							)}
							<span>
								{showDetails ? "Hide Error Trace" : "Show Error Trace"}
							</span>
						</button>

						{showDetails && (
							<pre className="text-[11px] font-mono text-gray-300 bg-black/50 p-3 rounded-lg border border-white/5 overflow-x-auto max-h-48 whitespace-pre-wrap">
								{errorDetails}
							</pre>
						)}
					</div>
				)}
			</div>
		</div>
	);
}

function ResultsTable({ results }: { results: InferenceResult[] }) {
	const columnHelper = createColumnHelper<InferenceResult>();

	const columns = useMemo(
		() => [
			columnHelper.accessor("id", {
				header: "ID",
				cell: (info) => (
					<span className="text-[10px] font-mono text-white/40">
						{info.getValue().slice(0, 4)}
					</span>
				),
			}),
			columnHelper.accessor("expression", {
				header: "Expression",
				cell: (info) => (
					<Tooltip.Root>
						<Tooltip.Trigger asChild>
							<div className="max-w-75 truncate font-mono text-xs text-white/70 cursor-help hover:text-white transition-colors">
								{info.getValue()}
							</div>
						</Tooltip.Trigger>
						<Tooltip.Portal>
							<Tooltip.Content
								className="z-50 p-4 rounded-xl border border-primary/20 bg-background-surface/90 backdrop-blur-xl shadow-2xl animate-in fade-in zoom-in-95 duration-200"
								sideOffset={5}
							>
								<div className="flex flex-col gap-2 pointer-events-none">
									<div className="text-[9px] uppercase tracking-widest text-white/30 font-bold border-b border-white/5 pb-2 mb-1">
										Mathematical Formula
									</div>
									<div className="text-lg">
										<katex.BlockMath
											math={info.row.original.latex || info.getValue()}
										/>
									</div>
								</div>
								<Tooltip.Arrow className="fill-background-surface border-t border-l border-primary/20" />
							</Tooltip.Content>
						</Tooltip.Portal>
					</Tooltip.Root>
				),
			}),
			columnHelper.accessor("fitness", {
				header: "Fitness",
				cell: (info) => {
					const val = info.getValue();
					return (
						<span className="font-mono text-xs font-bold text-emerald-400/90">
							{val !== null && val !== undefined ? val.toFixed(2) : "—"}
						</span>
					);
				},
			}),
			columnHelper.accessor("dl", {
				header: "DL",
				cell: (info) => {
					const val = info.getValue();
					return (
						<span className="font-mono text-xs font-bold text-primary/80">
							{val !== null && val !== undefined ? val.toFixed(2) : "—"}
						</span>
					);
				},
			}),
			columnHelper.accessor("size", {
				header: "Size",
				cell: (info) => (
					<span className="font-mono text-xs text-white/60">
						{info.getValue() ?? "—"}
					</span>
				),
			}),
			columnHelper.accessor("frequency", {
				header: "Freq",
				cell: (info) => {
					const val = info.getValue();
					return val ? (
						<span className="px-1.5 py-0.5 rounded-sm bg-primary/10 border border-primary/20 text-[10px] font-bold text-primary">
							{val}
						</span>
					) : (
						<span className="font-mono text-xs text-white/20">—</span>
					);
				},
			}),
			columnHelper.accessor("prediction", {
				header: "Prediction",
				cell: (info) => {
					const val = info.getValue();
					return val ? (
						<div className="flex flex-wrap gap-1">
							{val.map((v, i) => (
								<span
									key={i.toString()}
									className="px-2 py-1 rounded-sm bg-emerald-500/20 border border-emerald-500/30 text-[10px] font-bold text-emerald-400"
								>
									{v.toFixed(2)}
								</span>
							))}
						</div>
					) : (
						<span className="font-mono text-xs text-white/20">—</span>
					);
				},
			}),
		],
		[columnHelper],
	);

	const table = useReactTable({
		data: results,
		columns,
		getCoreRowModel: getCoreRowModel(),
	});

	return (
		<Tooltip.Provider delayDuration={200}>
			<div className="relative rounded-xl border border-white/5 bg-white/2 backdrop-blur-md overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-500">
				<div className="overflow-x-auto custom-scrollbar">
					<table className="w-full text-left border-collapse min-w-150">
						<thead className="bg-white/3 border-b border-white/5">
							{table.getHeaderGroups().map((headerGroup) => (
								<tr key={headerGroup.id}>
									{headerGroup.headers.map((header) => (
										<th
											key={header.id}
											className="px-4 py-3 text-[10px] font-black uppercase tracking-[0.2em] text-white/40"
										>
											{header.isPlaceholder
												? null
												: flexRender(
														header.column.columnDef.header,
														header.getContext(),
													)}
										</th>
									))}
								</tr>
							))}
						</thead>
						<tbody className="divide-y divide-white/5">
							{table.getRowModel().rows.map((row) => (
								<tr
									key={row.id}
									className={cn(
										"group/row hover:bg-primary/5 transition-all duration-200",
										row.index === 0 && "bg-primary/5",
									)}
								>
									{row.getVisibleCells().map((cell) => (
										<td key={cell.id} className="px-4 py-3 align-middle">
											{flexRender(
												cell.column.columnDef.cell,
												cell.getContext(),
											)}
										</td>
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</div>
		</Tooltip.Provider>
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
					{result.frequency !== undefined && result.frequency !== null && (
						<MetricBadge label="Freq" value={result.frequency.toString()} />
					)}

					{result.fitness !== undefined && result.fitness !== null && (
						<MetricBadge
							label="Fit"
							value={result.fitness.toFixed(2) || "N/A"}
						/>
					)}

					{result.dl !== undefined && result.dl !== null && (
						<MetricBadge label="DL" value={result.dl.toFixed(2) || "N/A"} />
					)}

					{result.size !== undefined && result.size !== null && (
						<MetricBadge label="Size" value={result.size.toString() || "N/A"} />
					)}
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

			{result.parameters && <TestVariables result={result} />}
		</div>
	);
}

function TestVariables({ result }: { result: InferenceResult }) {
	const [variables, setVariables] = useState<Record<string, string>>({});
	const [prediction, setPrediction] = useState<number | null>(null);

	const varNames = useMemo(() => {
		const match = (result.numpy || result.expression).match(/x\d+/g) || [];
		return Array.from(new Set(match)).sort();
	}, [result]);

	useEffect(() => {
		if (varNames.length === 0) {
			return;
		}

		try {
			const scope: Record<string, number> = {};
			for (const name of varNames) {
				scope[name] = parseFloat(variables[name] || "0");
			}

			if (result.parameters) {
				const parameters = Object.entries(result.parameters).reduce(
					(acc, [key, value]) => {
						const newKey = `t${key}`;
						acc[newKey] = value;

						return acc;
					},
					{} as Record<string, number>,
				);

				Object.assign(scope, parameters);
			}

			const expr = result.expression.replace(/\^/g, "^");
			const pred = evaluate(expr, scope);
			setPrediction(pred);
		} catch (error) {
			console.error("Error evaluating expression:", error);
			setPrediction(null);
		}
	}, [variables, varNames, result]);

	if (varNames.length === 0) return null;

	return (
		<div className="flex flex-col gap-3 mt-2 border-t border-white/5 pt-4">
			<div className="text-[10px] uppercase tracking-widest text-primary/70 font-bold flex items-center gap-1.5">
				<Zap className="w-3 h-3" />
				Test Input Variables
			</div>
			<div className="flex items-center gap-4 bg-black/20 p-3 rounded-lg border border-white/5 flex-wrap">
				{varNames.map((name) => (
					<div key={name} className="flex items-center gap-2">
						<span className="text-xs font-mono font-bold text-white/50">
							{name}
						</span>
						<span className="text-xs text-white/20">=</span>
						<input
							type="number"
							value={variables[name] || ""}
							onChange={(e) =>
								setVariables((v) => ({ ...v, [name]: e.target.value }))
							}
							placeholder="0"
							className="w-20 bg-white/5 border border-white/10 rounded px-2 py-1 text-xs font-mono text-white focus:outline-none focus:border-primary/50 transition-colors"
						/>
					</div>
				))}

				<div className="flex-1" />

				<div className="flex items-center gap-3 pl-4 border-l border-white/10">
					<span className="text-[10px] uppercase tracking-widest text-white/40 font-bold">
						Output
					</span>
					<span className="text-lg font-mono font-black text-emerald-400">
						{prediction !== null && !Number.isNaN(prediction)
							? Number(prediction.toFixed(6))
							: "—"}
					</span>
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
