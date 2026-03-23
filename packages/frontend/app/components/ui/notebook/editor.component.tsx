import { AnimatePresence, type DragControls, Reorder } from "framer-motion";
import { NotebookCell } from "~/components/ui/notebook/cell.component";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import { type EditorBlock, useEditorStore } from "~/stores/editor.store";
import { DatasetsBlock } from "./cells/datasets-cell.component";
import { InferenceBlock } from "./cells/inference-cell.component";
import { JobsBlock } from "./cells/jobs-cell.component";
import { MarkdownBlock } from "./cells/markdown-cell.component";
import { MetadataBlock } from "./cells/metadata-cell.component";
import { DraggableItem } from "./draggable-item.component";
import { EditorToolbar } from "./editor-toolbar.component";

type ProfileEditorProps = {
	tabId: string;
};

export function ProfileEditor({ tabId }: ProfileEditorProps) {
	const tab = useEditorStore((state) => state.tabs[tabId]);

	const setActiveBlock = useEditorStore((state) => state.setActiveBlock);
	const reorderBlocks = useEditorStore((state) => state.reorderBlocks);

	const undo = useEditorStore((state) => state.undo);
	const redo = useEditorStore((state) => state.redo);

	useKeyboardShortcut("z", undo);
	useKeyboardShortcut("y", redo);

	if (!tab || tab.type !== "profile") {
		return null;
	}

	const { blocks, activeBlockId } = tab.data;

	const fixedBlocks = blocks.filter((b) =>
		["metadata", "datasets", "jobs"].includes(b.type),
	);

	const dynamicBlocks = blocks.filter(
		(b) => !["metadata", "datasets", "jobs"].includes(b.type),
	);

	const renderBlock = (
		block: EditorBlock,
		isActive: boolean,
		dragControls?: DragControls,
	) => {
		const onRun =
			block.type === "inference"
				? () => useEditorStore.getState().runInference(block.id)
				: undefined;

		return (
			<NotebookCell
				id={block.id}
				type={block.type}
				isActive={isActive}
				onClick={() => setActiveBlock(block.id)}
				onRun={onRun}
				isDeletable={!["metadata", "datasets", "jobs"].includes(block.type)}
				moveable={!["metadata", "datasets", "jobs"].includes(block.type)}
				dragControls={dragControls}
			>
				{block.type === "metadata" && (
					<MetadataBlock id={block.id} tabId={tabId} />
				)}
				{block.type === "datasets" && (
					<DatasetsBlock datasets={block.data.datasets} />
				)}
				{block.type === "inference" && (
					<InferenceBlock id={block.id} data={block.data} />
				)}
				{block.type === "markdown" && (
					<MarkdownBlock
						id={block.id}
						data={block.data}
						isActive={activeBlockId === block.id}
					/>
				)}
				{block.type === "jobs" && <JobsBlock id={block.id} data={block.data} />}
			</NotebookCell>
		);
	};

	return (
		<div className="flex-1 h-full overflow-y-auto custom-scrollbar bg-background">
			<div className="sticky top-0 z-40 w-full flex justify-center py-4 pointer-events-none">
				<div className="pointer-events-auto">
					<EditorToolbar />
				</div>
			</div>

			<div className="flex flex-col w-full divide-y divide-border">
				{fixedBlocks.map((block) => (
					<div key={block.id} className="w-full">
						{renderBlock(block, activeBlockId === block.id)}
					</div>
				))}

				<Reorder.Group
					axis="y"
					className="w-full divide-y divide-border"
					values={dynamicBlocks}
					onReorder={(newDynamicOrder) => {
						reorderBlocks([...fixedBlocks, ...newDynamicOrder]);
					}}
				>
					<AnimatePresence initial={false} mode="popLayout">
						{dynamicBlocks.map((block, index) => (
							<DraggableItem
								key={block.id}
								isLast={index === blocks.length - 1}
								isActive={activeBlockId === block.id}
								block={block}
								index={index}
								renderBlock={renderBlock}
							/>
						))}
					</AnimatePresence>
				</Reorder.Group>
			</div>

			<div className="h-64" />
		</div>
	);
}
