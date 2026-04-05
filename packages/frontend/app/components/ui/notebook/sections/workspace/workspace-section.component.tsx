import { Code2, type LucideIcon, Text } from "lucide-react";
import type { Model } from "~/schemas/domain/model.schema";
import { useEditorStore } from "~/stores/editor.store";
import { NotebookCell } from "../../cell.component";
import { InsertDivider } from "../../insert-divider.component";
import { InferenceBlock } from "./blocks/inference-block.component";
import { MarkdownBlock } from "./blocks/markdown-block.component";

type ProfileWorkspaceSectionProps = {
	models: Model[];
};

export function ProfileWorkspaceSection({
	models,
}: ProfileWorkspaceSectionProps) {
	const addBlock = useEditorStore((s) => s.addBlock);
	const setActiveBlock = useEditorStore((s) => s.setActiveBlock);

	const activeTab = useEditorStore((s) => {
		if (!s.activeTabId) return null;
		const tab = s.tabs[s.activeTabId];
		return tab?.type === "profile" ? tab : null;
	});

	const editorBlocks = activeTab?.data.blocks || [];
	const activeBlockId = activeTab?.data.activeBlockId || null;

	const handleAddInferenceBlock = () => {
		addBlock("inference", {
			code: "-- Write your IQL code here",
			status: "idle",
		});
	};

	const handleAddMarkdownBlock = () => {
		addBlock("markdown", {
			value:
				"## Write your markdown here\n### You can use markdown to document your profile, add instructions for your inference scripts, or anything else you can think of!",
		});
	};

	return (
		<div className="bg-background-surface border border-border rounded-lg p-5 shadow-sm space-y-4">
			<div className="flex items-center justify-between px-2">
				<div className="flex flex-col gap-1">
					<h2 className="text-xl font-bold text-foreground">Workspace</h2>
					<p className="text-xs text-muted-foreground">
						Create documentation and inference scripts to explore your models
						and jobs.
					</p>
				</div>

				<div className="flex gap-2">
					<InsertButton
						Icon={Code2}
						label="Inference"
						onClick={handleAddInferenceBlock}
					/>

					<InsertButton
						Icon={Text}
						label="Markdown"
						onClick={handleAddMarkdownBlock}
					/>
				</div>
			</div>

			<div className="grid grid-cols-1 gap-2">
				{editorBlocks.length === 0 ? (
					<div className="col-span-full py-12 border border-dashed border-border rounded-lg flex flex-col items-center justify-center bg-white/5 opacity-50">
						<span className="text-sm text-gray-500 font-medium">
							No blocks created yet.
						</span>
						<span className="text-[10px] text-gray-500/60 mt-1 uppercase tracking-widest font-bold">
							Start by adding inference scripts or markdown
						</span>
					</div>
				) : (
					editorBlocks.map((block, index) => (
						<div key={block.id} className="w-full">
							<NotebookCell
								id={block.id}
								type={block.type}
								isActive={activeBlockId === block.id}
								onClick={() => setActiveBlock(block.id)}
								onRun={
									block.type === "inference"
										? () => console.log("Run inference", block.id)
										: undefined
								}
							>
								{block.type === "inference" && (
									<InferenceBlock
										id={block.id}
										data={block.data}
										models={models}
										orderIndex={index}
									/>
								)}

								{block.type === "markdown" && (
									<MarkdownBlock
										id={block.id}
										data={block.data}
										isActive={activeBlockId === block.id}
									/>
								)}
							</NotebookCell>

							<InsertDivider index={index} />
						</div>
					))
				)}
			</div>
		</div>
	);
}

type InsertButtonProps = {
	Icon: LucideIcon;
	label: string;
	onClick: () => void;
};

function InsertButton({ Icon, label, onClick }: InsertButtonProps) {
	return (
		<button
			type="button"
			onClick={onClick}
			className="flex items-center gap-1.5 px-3 py-1 bg-[#1e2028] border border-white/10 rounded-full text-[10px] font-bold text-gray-400 hover:text-white hover:bg-primary-500/20 hover:border-primary-500/50 transition-all shadow-xl cursor-pointer"
		>
			<Icon size={12} /> {label}
		</button>
	);
}
