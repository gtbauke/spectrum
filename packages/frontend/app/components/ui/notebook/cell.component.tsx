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
			initial={{ opacity: 0, y: 20, scale: 0.95 }}
			animate={{ opacity: 1, y: 0, scale: 1 }}
			exit={{
				opacity: 0,
				scale: 0.9,
				y: -10,
				transition: { duration: 0.2 },
			}}
			transition={{
				type: "spring",
				stiffness: 400,
				damping: 30,
				opacity: { duration: 0.2 },
			}}
			className="group relative flex w-full max-w-4xl mx-auto mb-2"
			onMouseEnter={() => setIsHovered(true)}
			onMouseLeave={() => setIsHovered(false)}
			onKeyDown={handleOnKeyDown}
			onClick={onClick}
			dragListener={false}
			dragControls={dragControls}
		>
			<div
				className={cn(
					"w-12 shrink-0 flex flex-col items-center pt-3 transition-opacity duration-200",
					isHovered || isActive ? "opacity-100" : "opacity-0",
				)}
			>
				{moveable && (
					<button
						type="button"
						className="p-1 text-gray-600 hover:text-gray-300 cursor-grab"
						onPointerDown={(e) => {
							e.preventDefault();
							dragControls?.start(e);
						}}
					>
						<GripVertical size={16} />
					</button>
				)}

				{onRun && (
					<button
						type="button"
						onClick={(e) => {
							e.stopPropagation();
							onRun();
						}}
						className="mt-1 p-1.5 rounded-full bg-white/5 text-gray-400 hover:bg-emerald-500/20 hover:text-emerald-400 transition-colors"
						title="Run cell"
					>
						<Play size={14} className="ml-0.5" />
					</button>
				)}
			</div>

			<div
				className={cn(
					"flex-1 relative rounded-lg border transition-all duration-200 bg-black/20",
					isActive
						? "border-purple-500/50 shadow-[0_0_0_1px_rgba(168,85,247,0.2)]"
						: "border-white/5 hover:border-white/10",
				)}
			>
				{(isHovered || isActive) && (
					<div className="absolute -top-2.5 right-4 px-2 py-0.5 bg-[#111319] border border-white/10 rounded text-[9px] font-mono text-gray-500 uppercase tracking-wider z-10">
						{type}
					</div>
				)}

				<div className="p-4 outline-none">{children}</div>
			</div>

			<div
				className={cn(
					"w-10 shrink-0 flex flex-col items-center pt-3 transition-opacity duration-200",
					isHovered || isActive ? "opacity-100" : "opacity-0",
				)}
			>
				{isDeletable && (
					<button
						type="button"
						className="p-1.5 text-gray-600 hover:text-red-400 transition-colors cursor-pointer"
						onClick={() => removeBlock(id)}
					>
						<Trash2 size={14} />
					</button>
				)}
				<button
					type="button"
					className="mt-1 p-1.5 text-gray-600 hover:text-gray-300 transition-colors"
				>
					<MoreHorizontal size={14} />
				</button>
			</div>
		</motion.div>
	);
}
