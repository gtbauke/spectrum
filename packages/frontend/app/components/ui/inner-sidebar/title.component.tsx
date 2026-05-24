import { Filter } from "lucide-react";
import type { PropsWithChildren } from "react";
import { cn } from "~/utils/classname.util";

type SidebarTitleProps = PropsWithChildren<{
	toggleFilter?: () => void;
	activeFilterCount?: number;
}>;

export function SidebarTitle({
	children,
	toggleFilter,
	activeFilterCount = 0,
}: SidebarTitleProps) {
	return (
		<div className="flex items-center justify-between">
			<span className="text-[10px] font-bold uppercase tracking-widest text-gray-500">
				{children}
			</span>
			<button
				type="button"
				className={cn(
					"relative p-1 rounded-md transition-colors cursor-pointer",
					activeFilterCount > 0
						? "text-primary-400 hover:bg-purple-500/10"
						: "text-gray-500 hover:bg-white/5 hover:text-gray-200",
				)}
				onClick={toggleFilter}
				aria-label="Toggle advanced filters"
				title="Advanced filters"
			>
				<Filter size={14} />

				{activeFilterCount > 0 && (
					<span className="absolute -top-0.5 -right-0.5 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-primary-500 text-[9px] font-bold text-white shadow-[0_0_0_2px_#111319]">
						{activeFilterCount}
					</span>
				)}
			</button>
		</div>
	);
}
