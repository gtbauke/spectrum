import Editor from "@monaco-editor/react";
import { SplitSquareVertical } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type MarkdownBlockProps = {
	id: string;
	data: {
		value: string;
	};
	isActive: boolean;
};

export function MarkdownBlock({ id, data, isActive }: MarkdownBlockProps) {
	const updateBlock = useEditorStore((state) => state.updateBlock);
	const [isPreviewSideBySide, setIsPreviewSideBySide] = useState(false);

	const handleEditorChange = (value: string | undefined) => {
		updateBlock(id, { value: value || "" }, { recordHistory: true });
	};

	const renderMarkdown = () => (
		<div className="prose prose-invert prose-emerald max-w-none prose-p:text-sm prose-headings:mb-4 prose-p:leading-relaxed prose-code:text-secondary prose-a:text-secondary group-hover:prose-a:opacity-100 transition-all">
			<ReactMarkdown
				remarkPlugins={[remarkGfm, remarkMath]}
				rehypePlugins={[rehypeHighlight, rehypeKatex]}
			>
				{data.value}
			</ReactMarkdown>
		</div>
	);

	return (
		<div className="flex flex-col gap-4">
			<div className="flex items-center justify-between pb-2 border-b border-border/10 opacity-40 group-hover:opacity-100 focus-within:opacity-100 transition-opacity">
				<div className="flex items-center gap-2">
					<div className="w-1 h-3 bg-primary/40 rounded-full" />
					<span className="text-[10px] font-black uppercase tracking-[0.2em] text-primary-500">
						{isActive ? "Editor" : "Documentation"}
					</span>
				</div>

				<div className="flex items-center gap-1">
					<IconButton
						Icon={SplitSquareVertical}
						className={cn(
							"p-1.5 rounded-lg opacity-60 hover:opacity-100 transition-all",
							isPreviewSideBySide &&
								"text-primary-500 bg-primary/10 opacity-100",
						)}
						title="Side-by-side preview"
						onClick={() => setIsPreviewSideBySide(!isPreviewSideBySide)}
					/>
				</div>
			</div>

			<div
				className={cn(
					"grid gap-4",
					isPreviewSideBySide ? "grid-cols-2" : "grid-cols-1",
				)}
			>
				{(isActive || isPreviewSideBySide) && (
					<div className="relative group/markdown-editor">
						<div className="absolute -inset-0.5 bg-primary/10 rounded-xl blur opacity-0 group-hover/markdown-editor:opacity-30 transition duration-500" />
						<div className="relative rounded-xl border border-white/10 bg-background-surface/50 backdrop-blur-xl overflow-hidden ring-1 ring-white/5">
							<Editor
								height="250px"
								language="markdown"
								theme="vs-dark"
								value={data.value}
								onChange={handleEditorChange}
								options={{
									minimap: { enabled: false },
									fontSize: 13,
									wordWrap: "on",
									scrollBeyondLastLine: false,
									automaticLayout: true,
									padding: { top: 16, bottom: 16 },
									lineNumbers: "off",
									folding: false,
									fontFamily: "'Fira Code', 'Cascadia Code', monospace",
								}}
							/>
						</div>
					</div>
				)}

				{(!isActive || isPreviewSideBySide) && (
					<div
						className={cn(
							"rounded-xl border border-white/5 bg-white/1 p-8 transition-all duration-300",
							!isPreviewSideBySide &&
								"hover:border-white/10 hover:bg-white/3 cursor-pointer",
						)}
					>
						{renderMarkdown()}
					</div>
				)}
			</div>
		</div>
	);
}
