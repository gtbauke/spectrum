import { motion } from "framer-motion";
import { Code2, type LucideIcon, Text } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";

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

type InsertDividerProps = {
	index: number;
};

export function InsertDivider({ index }: InsertDividerProps) {
	const addBlock = useEditorStore((state) => state.addBlock);

	return (
		<motion.div
			layout
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			className="group relative h-4 w-full flex items-center justify-center"
		>
			<div className="absolute inset-x-0 h-px bg-primary-500/0 group-hover:bg-primary-500/20 transition-colors mx-12" />

			<div className="z-10 flex gap-2 opacity-0 group-hover:opacity-100 transition-all scale-95 group-hover:scale-100">
				<InsertButton
					Icon={Code2}
					label="Inference"
					onClick={() =>
						addBlock("inference", { code: "-- New Script\n" }, index)
					}
				/>

				<InsertButton
					Icon={Text}
					label="Markdown"
					onClick={() => addBlock("markdown", { value: "" }, index)}
				/>
			</div>
		</motion.div>
	);
}
