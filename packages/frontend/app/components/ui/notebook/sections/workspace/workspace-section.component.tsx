import { Code2, type LucideIcon, Text } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";
import { InsertDivider } from "../../insert-divider.component";

export function ProfileWorkspaceSection() {
	const addBlock = useEditorStore((s) => s.addBlock);
	const editorBlocks = useEditorStore((s) => {
		if (!s.activeTabId) {
			return [];
		}

		const activeTab = s.tabs[s.activeTabId];
		if (!activeTab || activeTab.type !== "profile") {
			return [];
		}

		return activeTab.data.blocks;
	});

	const handleAddInferenceBlock = () => {
		addBlock("inference", {
			code: "-- Write your IQL code here",
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
			<div className="flex items-center justify-between">
				<div className="flex flex-col gap-1">
					<h2 className="text-xl font-bold text-foreground">Workspace</h2>
					<p className="text-xs text-muted-foreground">
						Create documentation and inference scripts to explore your models
						and jobs.
					</p>
				</div>
			</div>

			<div className="grid grid-cols-1 gap-3">
				{editorBlocks.length === 0 ? (
					<div className="col-span-full py-8 border border-dashed border-border rounded-lg flex flex-col items-center justify-center bg-white/5">
						<span className="text-sm text-gray-500 font-medium">
							No blocks created yet.
						</span>

						<div className="flex flex-col items-center gap-4">
							<span className="text-sm text-gray-500 font-medium">
								Start by adding inference scripts to run your models or markdown
							</span>
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
					</div>
				) : (
					editorBlocks.map((block, index) => (
						<div key={block.id} className="w-full">
							<div className="p-4 border border-border rounded-lg bg-background">
								BLOCK - {block.type} - {block.id}
							</div>

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
