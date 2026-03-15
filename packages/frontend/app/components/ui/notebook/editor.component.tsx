import { AnimatePresence, type DragControls, Reorder } from "framer-motion";
import { useEffect } from "react";
import { NotebookCell } from "~/components/ui/notebook/cell.component";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import type { ProfileVersion } from "~/schemas/models/profile-version.schema";
import { type EditorBlock, useEditorStore } from "~/stores/editor.store";
import { DatasetsBlock } from "./cells/datasets-cell.component";
import { InferenceBlock } from "./cells/inference-cell.component";
import { JobsBlock } from "./cells/jobs-cell.component";
import { MarkdownBlock } from "./cells/markdown-cell.component";
import { MetadataBlock } from "./cells/metadata-cell.component";
import { DraggableItem } from "./draggable-item.component";
import { EditorToolbar } from "./editor-toolbar.component";
import { InsertDivider } from "./insert-divider.component";

type ProfileEditorProps = {
	version: ProfileVersion;
};

export function ProfileEditor({ version }: ProfileEditorProps) {
	const initEditor = useEditorStore((state) => state.initEditor);
	const blocks = useEditorStore((state) => state.blocks);
	const activeBlockId = useEditorStore((state) => state.activeBlockId);
	const setActiveBlock = useEditorStore((state) => state.setActiveBlock);
	const reorderBlocks = useEditorStore((state) => state.reorderBlocks);

	const undo = useEditorStore((state) => state.undo);
	const redo = useEditorStore((state) => state.redo);

	const storeProfileId = useEditorStore((state) => state.profileId);

	useKeyboardShortcut("z", undo);
	useKeyboardShortcut("y", redo);

	useEffect(() => {
		const dynamic_blocks: EditorBlock[] = [];

		for (const block of version.blocks) {
			dynamic_blocks.push({
				id: block.id,
				type: block.type,
				// biome-ignore lint/suspicious/noExplicitAny: Value is dynamic
				data: block.data as any,
			});
		}

		const blocks: EditorBlock[] = [
			{
				id: `metadata-${version.profile_id}`,
				type: "metadata",
				data: {
					name: version.name,
					description: version.description,
					visibility: version.visibility,
				},
			},
			{
				id: `datasets-${version.profile_id}`,
				type: "datasets",
				data: {
					datasets: version.datasets,
				},
			},
			{
				id: `jobs-${version.profile_id}`,
				type: "jobs",
				data: {
					profileId: version.profile_id,
				},
			},
			...dynamic_blocks,
		];

		initEditor(version.profile_id, version.id, blocks);
	}, [version, initEditor]);

	if (!blocks.length) {
		return null;
	}

	if (storeProfileId !== version.profile_id) {
		return <div className="flex-1 h-full bg-[#111319] animate-pulse" />;
	}

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
		return (
			<NotebookCell
				id={block.id}
				type={block.type}
				isActive={isActive}
				onClick={() => setActiveBlock(block.id)}
				isDeletable={!["metadata", "datasets", "jobs"].includes(block.type)}
				moveable={!["metadata", "datasets", "jobs"].includes(block.type)}
				dragControls={dragControls}
			>
				{block.type === "metadata" && (
					<MetadataBlock id={block.id} data={block.data} />
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
		<div className="flex-1 h-full overflow-y-auto custom-scrollbar bg-[#111319] py-8 px-4">
			<div className="sticky top-0 z-40 w-full flex justify-center py-4 pointer-events-none">
				<div className="pointer-events-auto">
					<EditorToolbar />
				</div>
			</div>

			<div className="max-w-4xl mx-auto mb-8 pl-12">
				<h1 className="text-2xl font-bold text-gray-200">{version.name}</h1>
				<p className="text-xs text-gray-500 mt-1">
					Version {version.version} • {version.status}
				</p>
			</div>

			{fixedBlocks.map((block) => (
				<div key={block.id}>
					{renderBlock(block, activeBlockId === block.id)}
					<InsertDivider index={0} />
				</div>
			))}

			<Reorder.Group
				axis="y"
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

			<div className="h-64" />
		</div>
	);
}
