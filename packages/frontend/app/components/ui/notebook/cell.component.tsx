import { type DragControls, motion } from "framer-motion";
import { GripVertical, MoreHorizontal, Trash2 } from "lucide-react";
import { type BlockType, useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import { IconButton } from "../buttons/icon-button.component";

type NotebookCellProps = {
	id: string;
	type: BlockType;
	isActive: boolean;
	children: React.ReactNode;
	onClick: () => void;
	isDeletable?: boolean;
	moveable?: boolean;
	dragControls?: DragControls;
};

export function NotebookCell({
	id,
	type,
	isActive,
	onClick,
	children,
	isDeletable = true,
	moveable = true,
	dragControls,
}: NotebookCellProps) {
	const removeBlock = useEditorStore((state) => state.removeBlock);

	return (
		<motion.div
			layout
			initial={{ opacity: 0, y: 10 }}
			animate={{ opacity: 1, y: 0 }}
			exit={{
				opacity: 0,
				y: -10,
				transition: { duration: 0.1 },
			}}
			transition={{ duration: 0.1 }}
			className={cn(
				"group relative flex flex-col w-full bg-background border-l-2 transition-colors duration-100",
				isActive && "bg-background-surface ring-1 ring-white/5",
				isActive && type === "inference" && "border-secondary",
				isActive && type === "markdown" && "border-primary",
				!isActive && "border-transparent border-l-0",
			)}
			onClick={onClick}
			dragListener={false}
			dragControls={dragControls}
		>
			<div className="flex items-center justify-between px-4 py-2 bg-white/3 border-b border-border/50 opacity-40 group-hover:opacity-100 focus-within:opacity-100 transition-opacity">
				<div className="flex items-center gap-4">
					{moveable && (
						<IconButton
							Icon={GripVertical}
							className="p-1 text-gray-500 hover:text-white cursor-grab active:cursor-grabbing"
							onPointerDown={(e) => {
								e.preventDefault();
								dragControls?.start(e);
							}}
						/>
					)}

					<div className="flex items-center gap-2">
						<span
							className={cn(
								"text-[10px] font-bold uppercase tracking-[0.2em]",
								type === "inference"
									? "text-secondary-500"
									: "text-primary-500",
							)}
						>
							{type}
						</span>
						{isActive && (
							<div
								className={cn(
									"w-1 h-1 rounded-full",
									type === "inference" ? "bg-secondary" : "bg-primary",
								)}
							/>
						)}
					</div>
				</div>

				<div className="flex items-center gap-2">
					{isDeletable && (
						<IconButton
							Icon={Trash2}
							className="p-1.5 rounded text-gray-500 hover:bg-red-500/10 hover:text-red-500 transition-colors"
							title="Delete cell"
							onClick={(e) => {
								e.stopPropagation();
								removeBlock(id);
							}}
						/>
					)}
					<IconButton
						Icon={MoreHorizontal}
						className="p-1.5 rounded text-gray-500 hover:bg-white/5 transition-colors"
						title="More options"
					/>
				</div>
			</div>

			<div className="p-6 relative">
				<div className="absolute inset-0 bg-linear-to-b from-white/1 to-transparent pointer-events-none" />
				<div className="relative z-10">{children}</div>
			</div>
		</motion.div>
	);
}
