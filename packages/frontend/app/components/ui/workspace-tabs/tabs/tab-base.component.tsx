import { X } from "lucide-react";
import type React from "react";
import { cn } from "~/utils/classname.util";

export type TabBaseProps = {
	isActive: boolean;
	isDirty?: boolean;
	icon?: React.ReactNode;
	children: React.ReactNode;
	onClick: () => void;
	onClose: () => void;
};

export function TabBase({
	isActive,
	isDirty = false,
	icon,
	children,
	onClick,
	onClose,
}: TabBaseProps) {
	const handleKeyDown = (e: React.KeyboardEvent) => {
		if (e.key === "Enter") {
			e.preventDefault();
			onClick();
		}
	};

	const handleCloseClick = (e: React.MouseEvent) => {
		e.stopPropagation();
		onClose();
	};

	return (
		// biome-ignore lint/a11y/useSemanticElements: Cannot have nested buttons
		<div
			role="button"
			tabIndex={0}
			className="h-full cursor-pointer outline-none focus-visible:ring-1 focus-visible:ring-primary-500 inset-0"
			onClick={onClick}
			onKeyDown={handleKeyDown}
		>
			<div
				className={cn(
					"flex items-center px-4 h-full text-sm cursor-pointer group gap-2 transition-colors",
					isActive
						? "border-t-2 border-primary-500 bg-background"
						: "bg-background-surface hover:bg-background/50 border-t-2 border-transparent",
				)}
			>
				<div className="flex items-center gap-2 cursor-pointer max-w-37.5">
					{icon && <span className="text-primary-400 shrink-0">{icon}</span>}
					{children}
				</div>

				<div className="relative flex items-center justify-center w-6 h-6 ml-2 cursor-pointer shrink-0">
					<div
						className={cn(
							"absolute w-2 h-2 rounded-full bg-white transition-opacity duration-200",
							isDirty ? "opacity-100 group-hover:opacity-0" : "opacity-0",
						)}
					/>

					<button
						type="button"
						className={cn(
							"absolute p-1 text-gray-400 hover:text-red-400 cursor-pointer rounded-md transition-opacity duration-200",
							"opacity-0 group-hover:opacity-100 focus-visible:opacity-100 outline-none focus-visible:ring-1 focus-visible:ring-red-500",
							isActive && !isDirty ? "opacity-100" : "",
							isActive ? "hover:bg-background-surface" : "hover:bg-background",
						)}
						onClick={handleCloseClick}
						title="Close Tab"
					>
						<X size={14} />
					</button>
				</div>
			</div>
		</div>
	);
}
