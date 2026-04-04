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
		<div className="prose prose-invert prose-emerald max-w-none prose-p:text-sm prose-headings:mb-4 prose-p:leading-relaxed">
			<ReactMarkdown
				remarkPlugins={[remarkGfm, remarkMath]}
				rehypePlugins={[rehypeHighlight, rehypeKatex]}
			>
				{data.value}
			</ReactMarkdown>
		</div>
	);

	return (
		<div className="flex flex-col gap-3">
			<div className="flex items-center justify-between pb-2 border-b border-border/20 opacity-0 group-hover:opacity-100 transition-opacity">
				<div className="flex items-center gap-2">
					<span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">
						{isActive ? "Editor" : "Documentation"}
					</span>
				</div>

				<div className="flex items-center gap-1">
					<IconButton
						Icon={SplitSquareVertical}
						className={cn(
							"p-1 rounded opacity-60 hover:opacity-100",
							isPreviewSideBySide && "text-primary bg-primary/10 opacity-100",
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
					<div className="rounded border border-border bg-[#0d0e12] overflow-hidden">
						<Editor
							height="200px"
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
								padding: { top: 12, bottom: 12 },
								lineNumbers: "off",
								folding: false,
								fontFamily: "'Fira Code', 'Cascadia Code', monospace",
							}}
						/>
					</div>
				)}

				{(!isActive || isPreviewSideBySide) && (
					<div
						className={cn(
							"rounded border border-border/50 bg-black/20 p-6",
							!isPreviewSideBySide &&
								"hover:border-border transition-colors cursor-pointer",
						)}
					>
						{renderMarkdown()}
					</div>
				)}
			</div>
		</div>
	);
}
