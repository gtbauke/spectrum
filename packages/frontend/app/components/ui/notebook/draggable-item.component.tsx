import { type DragControls, Reorder, useDragControls } from "framer-motion";
import type { JSX } from "react";
import type { EditorBlock } from "~/stores/editor.store";
import { InsertDivider } from "./insert-divider.component";

type DraggableItemProps = {
	renderBlock(
		block: EditorBlock,
		isActive: boolean,
		dragControls?: DragControls,
	): JSX.Element;
	block: EditorBlock;
	index: number;
	isLast: boolean;
	isActive: boolean;
};

export function DraggableItem({
	block,
	index,
	isLast,
	isActive,
	renderBlock,
}: DraggableItemProps) {
	const dragControls = useDragControls();

	return (
		<Reorder.Item
			layout
			initial={{ opacity: 0, height: 0 }}
			animate={{ opacity: 1, height: "auto" }}
			exit={{
				opacity: 0,
				height: 0,
				scale: 0.95,
				transition: { opacity: { duration: 0.1 } },
			}}
			transition={{ opacity: { duration: 0.1 } }}
			value={block}
			dragListener={false}
			dragControls={dragControls}
		>
			{renderBlock(block, isActive, dragControls)}
			{isLast && <InsertDivider index={index + 1} />}
		</Reorder.Item>
	);
}
