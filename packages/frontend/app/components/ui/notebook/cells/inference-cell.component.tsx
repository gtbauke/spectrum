import Editor, { loader } from "@monaco-editor/react";
import { type InferenceData, useEditorStore } from "~/stores/editor.store";

loader.config({
    paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs" },
});

export function InferenceBlock({
    id,
    data,
}: {
    id: string;
    data: InferenceData;
}) {
    const updateBlock = useEditorStore((state) => state.updateBlock);

	const handleEditorChange = (value: string | undefined) => {
		updateBlock(id, { code: value || "" }, { recordHistory: true });
	};

	return (
		<div className="flex flex-col gap-4">
			<div className="rounded border border-border bg-[#0d0e12] overflow-hidden">
				<Editor
					height="240px"
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
					onMount={(_, monaco) => {
						monaco.editor.defineTheme("spectrum-flat", {
							base: "vs-dark",
							inherit: true,
							rules: [],
							colors: {
								"editor.background": "#0d0e12",
								"editor.lineHighlightBackground": "#ffffff03",
							},
						});
						monaco.editor.setTheme("spectrum-flat");
					}}
				/>
			</div>

			{data.isRunning && (
				<div className="flex items-center gap-3 py-4 px-2 opacity-60 animate-pulse">
					<div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
					<span className="text-[10px] font-mono uppercase tracking-widest text-emerald-500">
						Executing IQL Script...
					</span>
				</div>
			)}

			{data.results && !data.isRunning && (
				<div className="flex flex-col border border-border bg-background/50 rounded overflow-hidden">
					<div className="px-3 py-2 border-b border-border bg-white/5">
						<span className="text-[10px] font-mono text-gray-400 uppercase tracking-widest">
							Execution Results
						</span>
					</div>
					<div className="p-4 space-y-4">
						<div className="grid grid-cols-2 gap-4">
							{Object.entries((data.results.metrics as Record<string, number>)).map(([key, value]) => (
								<div key={key} className="flex flex-col gap-1">
									<span className="text-[9px] text-gray-500 uppercase font-mono">
										{key}
									</span>
									<span className="text-sm font-mono text-emerald-500">
										{(value as number).toFixed(4)}
									</span>
								</div>
							))}
						</div>
						{data.results.formula && (
							<div className="flex flex-col gap-2 pt-2 border-t border-border/50">
								<span className="text-[9px] text-gray-500 uppercase font-mono">
									Best Formula
								</span>
								<div className="p-3 bg-black/40 rounded font-mono text-xs text-primary-300">
									{data.results.formula}
								</div>
							</div>
						)}
					</div>
				</div>
			)}
		</div>
	);
}
