import { type DragControls, motion } from "framer-motion";
import { GripVertical, MoreHorizontal, Play, Trash2 } from "lucide-react";
import { useState } from "react";
import { type BlockType, useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type NotebookCellProps = {
	id: string;
	type: BlockType;
	isActive: boolean;
	children: React.ReactNode;
	onClick: () => void;
	onRun?: () => void;
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
	onRun,
	isDeletable = true,
	moveable = true,
	dragControls,
}: NotebookCellProps) {
	const removeBlock = useEditorStore((state) => state.removeBlock);
	const [isHovered, setIsHovered] = useState(false);

	const handleOnKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
		if (e.key === "Enter") {
			onClick();
		}
	};

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
			transition={{ duration: 0.2 }}
			className={cn(
				"group relative flex flex-col w-full bg-background border-l-2 transition-colors duration-200",
				isActive ? "border-primary bg-background-surface" : "border-transparent",
			)}
			onClick={onClick}
			dragListener={false}
			dragControls={dragControls}
		>
			<div className="flex items-center justify-between px-4 py-2 bg-white/5 border-b border-border opacity-50 group-hover:opacity-100 transition-opacity">
				<div className="flex items-center gap-4">
					{moveable && (
						<button
							type="button"
							className="p-1 text-gray-500 hover:text-white cursor-grab active:cursor-grabbing"
							onPointerDown={(e) => {
								e.preventDefault();
								dragControls?.start(e);
							}}
						>
							<GripVertical size={14} />
						</button>
					)}
					<span className="text-[10px] font-mono text-gray-400 uppercase tracking-widest">
						{type}
					</span>
				</div>

				<div className="flex items-center gap-2">
					{onRun && (
						<button
							type="button"
							onClick={(e) => {
								e.stopPropagation();
								onRun();
							}}
							className="p-1.5 rounded transition-colors hover:bg-emerald-500/10 text-emerald-500/60 hover:text-emerald-500"
							title="Run cell"
						>
							<Play size={12} fill="currentColor" className="opacity-50" />
						</button>
					)}
					{isDeletable && (
						<button
							type="button"
							className="p-1.5 rounded text-gray-500 hover:bg-red-500/10 hover:text-red-500 transition-colors"
							onClick={(e) => {
								e.stopPropagation();
								removeBlock(id);
							}}
						>
							<Trash2 size={12} />
						</button>
					)}
					<button
						type="button"
						className="p-1.5 rounded text-gray-500 hover:bg-white/5 transition-colors"
					>
						<MoreHorizontal size={12} />
					</button>
				</div>
			</div>

			<div className="p-6">{children}</div>
		</motion.div>
	);
}
